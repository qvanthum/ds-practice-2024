import os
import socket
import threading
import time
from utils.pb.bookstore import order_pb2 as order
from utils.pb.bookstore import order_queue_pb2 as order_queue
from utils.pb.bookstore import order_queue_pb2_grpc as order_queue_grpc
from utils.pb.bookstore import order_executor_pb2_grpc as order_executor_grpc
from utils.pb.bookstore import books_service_pb2 as books_service
from utils.pb.bookstore import books_service_pb2_grpc as books_service_grpc
from google.protobuf.empty_pb2 import Empty

import grpc
from concurrent import futures


thread_pool = futures.ThreadPoolExecutor()


class OrderExecutorService(order_executor_grpc.OrderExecutorServiceServicer):
    """
    Concrete implementation of the order executor service.
    It periodically fetches new orders from the order queue and executes them.
    It also implements a leadership election algorithm to ensure only one instance is active at a time.
    """

    def __init__(self):
        # really hacky way to get own ID but I didn't find a better one
        replica_count = int(os.getenv("ORDER_EXECUTOR_REPLICAS"))
        myip = socket.gethostbyname(socket.gethostname())
        self.id = next(i for i in range(1, replica_count + 1) if socket.gethostbyname(self._executor_address(i)) == myip)
        self.predecessor = self.id - 1 if self.id > 1 else replica_count
        self.successor = self.id + 1 if self.id < replica_count else 1
        self.db_id = (self.id - 1) % int(os.getenv("BOOKS_SERVICE_REPLICAS")) + 1

        def start_token_ring():
            # Wait for all instances to start
            time.sleep(5)
            self.SendToken(Empty(), None)

        if self.id == 1:
            # I am the first instance, so I will start the token ring
            print("I am the first order executor!")
            thread_pool.submit(start_token_ring)

    @staticmethod
    def _executor_address(executor_id: int, with_port=False) -> str:
        return f"bookstore-order_executor-{executor_id}" + (":50060" if with_port else "")

    @staticmethod
    def _book_service_address(book_service_id: int, with_port=False) -> str:
        return f"bookstore-books_service-{book_service_id}" + (":50065" if with_port else "")

    def SendToken(self, request, context):
        # get next order from queue
        print("Checking for new orders")
        with grpc.insecure_channel("order_queue:50054") as channel:
            stub = order_queue_grpc.OrderQueueServiceStub(channel)
            response: order_queue.OptionalOrder = stub.DequeueOrder(Empty())

        if not response.HasField("order"):
            print("No new orders")
            # wait for a while before checking again (to avoid busy waiting and not spam log)
            time.sleep(2)
        else:
            # execute order processing in a separate thread so we can return immediately
            thread_pool.submit(self._process_order, response.order)

        thread_pool.submit(self._hand_over_token)
        return Empty()
    
    def _process_order(self, order_data: order.OrderData):
        print(f"Executing order {order_data.orderId}")
        # simulate order processing
        time.sleep(2)
        with grpc.insecure_channel(self._book_service_address(self.db_id, with_port=True)) as channel:
            stub = books_service_grpc.BooksDatabaseStub(channel)
            for item in order_data.items:
                stub.Decrement(books_service.AdjustRequest(key=item.name, amount=item.quantity))
        time.sleep(2)
        print(f"Order {order_data.orderId} executed")

    def _hand_over_token(self):
        print(f"Handing token to executor {self.successor}")
        with grpc.insecure_channel(self._executor_address(self.successor, with_port=True)) as channel:
            stub = order_executor_grpc.OrderExecutorServiceStub(channel)
            stub.SendToken(Empty())

    
def serve():
    # Create a gRPC server
    server = grpc.server(thread_pool)
    order_executor_grpc.add_OrderExecutorServiceServicer_to_server(OrderExecutorService(), server)
    port = "50060"
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    print(f"Server started. Listening on port {port}")
    # Keep thread alive
    server.wait_for_termination()

if __name__ == '__main__':
    serve()