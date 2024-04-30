import grpc
from concurrent import futures
from utils.pb.bookstore import books_pb2_grpc
from utils.pb.bookstore import books_pb2
from google.protobuf.empty_pb2 import Empty

class BooksDatabaseService(books_pb2_grpc.BooksDatabaseServiceServicer):
    def __init__(self):
        # I have to create the database here
        self.database = {}  # Basic key-value store

    def Read(self, request, context):
        if request.key in self.database:
            return books_pb2.ReadResponse(value=self.database[request.key])
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Key not found")
            return books_pb2.ReadResponse()

    def Write(self, request, context):
        self.database[request.key] = request.value
        return Empty()

    def Init(self, request, context):
        self.database.clear()
        return Empty()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor())
    books_pb2_grpc.add_BooksDatabaseServiceServicer_to_server(BooksDatabaseService(), server)
    port = "50052"  #Not sure which one to use since there are three instances and I have to make head and tail as well
    server.add_insecure_port("[::]:" + port)
    server.start()
    print(f"Books Database Service started. Listening on port {port}.")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
