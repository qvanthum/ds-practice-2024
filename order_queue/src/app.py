import time
from utils.pb.bookstore import order_pb2 as order
from utils.pb.bookstore import order_queue_pb2 as order_queue
from utils.pb.bookstore import order_queue_pb2_grpc as order_queue_grpc
from google.protobuf.empty_pb2 import Empty

import grpc
from concurrent import futures
import heapq

from opentelemetry.sdk.resources import SERVICE_NAME, Resource

from opentelemetry import metrics
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader

resource = Resource(attributes={
    SERVICE_NAME: "order_queue"
})

reader = PeriodicExportingMetricReader(
    OTLPMetricExporter(endpoint="http://observability:4318/v1/metrics"),
)
meterProvider = MeterProvider(resource=resource, metric_readers=[reader])
metrics.set_meter_provider(meterProvider)

meter = metrics.get_meter("order_queue.meter")
queue_size = meter.create_up_down_counter(
    "queue_size", description="The size of the order queue", unit="1"
)
wait_time = meter.create_histogram(
    "wait_time", description="The time an order waits in the queue", unit="s",
)



class OrderEntry:
    def __init__(self, order_data: order.OrderData):
        self.order_data = order_data
        self.size = sum(item.quantity for item in order_data.items)
        self.insert_time = time.perf_counter()

    def __lt__(self, other):
        return self.size < other.size


class OrderQueueService(order_queue_grpc.OrderQueueServiceServicer):
    """
    Concrete implementation of the order queue service.
    It supports adding orders to the queue and popping the highest priority order.
    """

    def __init__(self):
        super().__init__()
        self.orders: list[OrderEntry] = []

    @staticmethod
    def get_priority(order: order.OrderData):
        # execute small orders quickly
        return sum(item.quantity for item in order.items)

    def EnqueueOrder(self, request: order.OrderData, context):
        """Adds an order to the queue."""
        order_entry = OrderEntry(request)
        print(f"Enqueueing order: {request.orderId} ({order_entry.size} items)")
        heapq.heappush(self.orders, order_entry)
        queue_size.add(1)
        return Empty()
    
    def DequeueOrder(self, request: Empty, context):
        """Pops the highest priority order from the queue."""
        if len(self.orders) == 0:
            return order_queue.OptionalOrder()
        order_entry = heapq.heappop(self.orders)
        queue_size.add(-1)
        order_data = order_entry.order_data
        wait_time.record(time.perf_counter() - order_entry.insert_time, {"orderId": order_data.orderId})
        print(f"Dequeueing order: {order_data.orderId} ({order_entry.size} items)")
        return order_queue.OptionalOrder(order=order_data)
    
    
def serve():
    # Create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor())
    order_queue_grpc.add_OrderQueueServiceServicer_to_server(OrderQueueService(), server)
    port = "50054"
    server.add_insecure_port("[::]:" + port)
    server.start()
    print(f"Server started. Listening on port {port}.")
    # Keep thread alive
    server.wait_for_termination()

if __name__ == '__main__':
    serve()