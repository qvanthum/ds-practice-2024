import socket
import xxhash
import os
from concurrent import futures
import threading
from utils.pb.bookstore import books_service_pb2_grpc as books_service_grpc
from utils.pb.bookstore import books_service_pb2 as books_service

import grpc


class BooksDatabaseService(books_service_grpc.BooksDatabaseServicer):
    """
    Concrete implementation of the books database service.
    It provides basic read and write operations for a key-value store.
    """

    def __init__(self):
        # really hacky way to get own ID but I didn't find a better one
        self.replica_count = int(os.getenv("BOOKS_SERVICE_REPLICAS"))
        myip = socket.gethostbyname(socket.gethostname())
        self.id = next(i for i in range(1, self.replica_count + 1) if socket.gethostbyname(self._book_service_address(i)) == myip)

        # prepopulate the database with some initial values
        # in a production environment the keys should be IDs not book names
        self.database = {
            "Learning Python": 10,
            "JavaScript - The Good Parts": 15,
            "Domain-Driven Design: Tackling Complexity in the Heart of Software": 15,
            "Design Patterns: Elements of Reusable Object-Oriented Software": 15,
        }
        self.lock = threading.Lock()

    def Read(self, request: books_service.ReadRequest, context):
        """Returns the locally stored value"""
        print(f"Reading key '{request.key}' from local")
        if request.key in self.database:
            return books_service.ReadResponse(value=self.database[request.key])
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Key not found")
            return books_service.ReadResponse()

    def Write(self, request: books_service.WriteRequest, context):
        """
        Determines the primary replica for the key using hashing.
        If the primary replica is this instance, it writes the value locally and updates the backups.
        Otherwise, it forwards the request to the primary replica.
        """
        primary_id = self._primary(request.key)
        if primary_id == self.id:
            self._write_local(request)
            success = self._update_backups(request)
            return books_service.WriteRequest(success=success)
        print(f"Forwarding write request for key '{request.key}' to database {primary_id}")
        with grpc.insecure_channel(self._book_service_address(primary_id, with_port=True)) as channel:
            stub = books_service_grpc.BooksDatabaseStub(channel)
            return stub.Write(request)

    def Exists(self, request: books_service.ReadRequest, context):
        """Returns whether the key exists locally"""
        return books_service.ExistsResponse(exists=request.key in self.database)
    
    def Increment(self, request: books_service.AdjustRequest, context):
        """
        Atomic operation to increment the value of a key.
        This can be used by clients to avoid race conditions for updating values.
        """
        primary_id = self._primary(request.key)
        if primary_id == self.id:
            success = self._adjust_local(request)
            if success:
                success = self._update_backups(books_service.WriteRequest(key=request.key, value=self.database[request.key]))
            return books_service.WriteResponse(success=success)
        print(f"Forwarding adjustment request for key '{request.key}' to database {primary_id}")
        with grpc.insecure_channel(self._book_service_address(primary_id, with_port=True)) as channel:
            stub = books_service_grpc.BooksDatabaseStub(channel)
            return stub.Increment(request)
        
    def Decrement(self, request: books_service.AdjustRequest, context):
        """
        Atomic operation to decrement the value of a key.
        This can be used by clients to avoid race conditions for updating values.
        """
        return self.Increment(books_service.AdjustRequest(
            key=request.key, amount=-request.amount, allowNegativeResult=request.allowNegativeResult), context
        )

    def Update(self, request: books_service.WriteRequest, context):
        """Updates the value of a key in the local database (called by primary)"""
        self._write_local(request)
        return books_service.WriteResponse(success=True)
    
    def _primary(self, key: str) -> int:
        return xxhash.xxh64(key).intdigest() % self.replica_count + 1
    
    def _write_local(self, request: books_service.WriteRequest):
        print(f"Writing key '{request.key}' to local database. New value: {request.value}")
        # avoid multiple writes at the same time
        with self.lock:
            self.database[request.key] = request.value

    def _adjust_local(self, request: books_service.AdjustRequest) -> bool:
        # avoid multiple writes at the same time
        with self.lock:
            if request.key not in self.database:
                print(f"Key '{request.key}' not found in local database")
                return False
            result = self.database[request.key] + request.amount
            if result < 0 and not request.allow_negative:
                print(f"Key '{request.key}' would become negative in local database")
                return False
            print(f"Adjusting key '{request.key}' by {request.amount} in local database. New value: {result}")
            self.database[request.key] = result
            return True

    def _update_backups(self, request: books_service.WriteRequest) -> bool:
        print(f"Updating backups for key '{request.key}'")
        # In a production environment this would be parallelized
        success = True
        for i in range(1, self.replica_count):
            if i == self.id:
                continue
            with grpc.insecure_channel(self._book_service_address(i, with_port=True)) as channel:
                stub = books_service_grpc.BooksDatabaseStub(channel)
                success |= stub.Update(request).success
        return success

    @staticmethod
    def _book_service_address(book_service_id: int, with_port=False) -> str:
        return f"bookstore-books_service-{book_service_id}" + (":50065" if with_port else "")


def serve():
    server = grpc.server(futures.ThreadPoolExecutor())
    books_service_grpc.add_BooksDatabaseServicer_to_server(BooksDatabaseService(), server)
    port = "50065"
    server.add_insecure_port("[::]:" + port)
    server.start()
    print(f"Books Database Service started. Listening on port {port}.")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
