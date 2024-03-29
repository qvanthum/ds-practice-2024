from dataclasses import dataclass
from utils.pb.bookstore import order_pb2 as order
from utils.pb.bookstore import order_queue_pb2 as order_queue
from utils.pb.bookstore import order_queue_pb2_grpc as order_queue_grpc
from google.protobuf.empty_pb2 import Empty

import grpc
from concurrent import futures
import heapq


class OrderEntry:
    def __init__(self, order_data: order.OrderData):
        self.order_data = order_data
        self.size = sum(item.quantity for item in order_data.items)

    def __lt__(self, other):
        return self.size < other.size


class OrderQueueService(order_queue_grpc.OrderQueueServiceServicer):
    """
    Concrete implementation of the order queue service.
    It supports adding orders to the queue and popping the highest priority order.
    """

    def __init__(self):
        super().__init__()
        self.orders: list[order.OrderData] = []

    @staticmethod
    def get_priority(order: order.OrderData):
        # execute small orders quickly
        return sum(item.quantity for item in order.items)

    def EnqueueOrder(self, request: order.OrderData, context):
        """Adds an order to the queue."""
        order_entry = OrderEntry(request)
        print(f"Enqueueing order: {request.orderId} ({order_entry.size} items)")
        heapq.heappush(self.orders, OrderEntry(request))
        return Empty()
    
    def DequeueOrder(self, request: Empty, context):
        """Pops the highest priority order from the queue."""
        if len(self.orders) == 0:
            return order_queue.OptionalOrder()
        order_entry = heapq.heappop(self.orders)
        order_data = order_entry.order_data
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