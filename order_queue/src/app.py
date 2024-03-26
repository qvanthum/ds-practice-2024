from utils.pb.bookstore import order_pb2 as order
from utils.pb.bookstore import order_queue_pb2 as order_queue
from utils.pb.bookstore import order_queue_pb2_grpc as order_queue_grpc
from google.protobuf.empty_pb2 import Empty

import grpc
from concurrent import futures
import heapq


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
        print(f"Enqueueing order: {request.orderId}")
        heapq.heappush(self.orders, (self.get_priority(request), request))
        return Empty()
    
    def DequeueOrder(self, request: Empty, context):
        """Pops the highest priority order from the queue."""
        if len(self.orders) == 0:
            return order_queue.OptionalOrder(None)
        _, order_data = heapq.heappop(self.orders)
        print(f"Dequeueing order: {order_data.orderId}")
        return order_queue.OptionalOrder(order_data)
    
    
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