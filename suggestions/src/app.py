from concurrent import futures
import random
import grpc

from utils.vectorclock.vectorclock import ClockService
from utils.pb.bookstore import order_pb2 as order
from utils.pb.bookstore import suggestions_pb2 as suggestions
from utils.pb.bookstore import suggestions_pb2_grpc as suggestions_grpc
from utils.pb.bookstore.order_pb2 import BookSuggestion


class SuggestionService(ClockService, suggestions_grpc.SuggestionServiceServicer):
    """
    Concrete implementation of the book suggestion service.
    Currently, it just suggests 3 random books out of a static list.
    """

    # The name of the service, used for the vector clock.
    service_name = "suggestions"

    all_suggestions = [
        BookSuggestion(id='1', title="The Great Gatsby", author="F. Scott Fitzgerald"),
        BookSuggestion(id='2', title="To Kill a Mockingbird", author="Harper Lee"),
        BookSuggestion(id='3', title="1984", author="George Orwell"),
        BookSuggestion(id='4', title="Pride and Prejudice", author="Jane Austen"),
        BookSuggestion(id='5', title="The Catcher in the Rye", author="J.D. Salinger"),
        BookSuggestion(id='6', title="To the Lighthouse", author="Virginia Woolf"),
        BookSuggestion(id='7', title="Moby Dick", author="Herman Melville"),
        BookSuggestion(id='8', title="The Lord of the Rings", author="J.R.R. Tolkien"),
        BookSuggestion(id='9', title="Harry Potter and the Sorcerer's Stone", author="J.K. Rowling"),
        BookSuggestion(id='10', title="The Chronicles of Narnia", author="C.S. Lewis"),
        BookSuggestion(id='11', title="The Hobbit", author="J.R.R. Tolkien"),
        BookSuggestion(id='12', title="The Da Vinci Code", author="Dan Brown"),
        BookSuggestion(id='13', title="The Alchemist", author="Paulo Coelho"),
        BookSuggestion(id='14', title="The Hunger Games", author="Suzanne Collins"),
        BookSuggestion(id='15', title="The Kite Runner", author="Khaled Hosseini"),
        BookSuggestion(id='16', title="The Fault in Our Stars", author="John Green"),
        BookSuggestion(id='17', title="The Girl with the Dragon Tattoo", author="Stieg Larsson"),
        BookSuggestion(id='18', title="The Shining", author="Stephen King"),
        BookSuggestion(id='19', title="The Catch-22", author="Joseph Heller"),
        BookSuggestion(id='20', title="The Grapes of Wrath", author="John Steinbeck"),
        BookSuggestion(id='21', title="The Picture of Dorian Gray", author="Oscar Wilde"),
        BookSuggestion(id='22', title="The Adventures of Huckleberry Finn", author="Mark Twain"),
        BookSuggestion(id='23', title="The Little Prince", author="Antoine de Saint-Exupéry"),
        BookSuggestion(id='24', title="The Scarlet Letter", author="Nathaniel Hawthorne"),
        BookSuggestion(id='25', title="The Count of Monte Cristo", author="Alexandre Dumas"),
        BookSuggestion(id='26', title="The Odyssey", author="Homer"),
        BookSuggestion(id='27', title="The Divine Comedy", author="Dante Alighieri"),
        BookSuggestion(id='28', title="The War and Peace", author="Leo Tolstoy"),
        BookSuggestion(id='29', title="The Brothers Karamazov", author="Fyodor Dostoevsky"),
        BookSuggestion(id='30', title="The Adventures of Sherlock Holmes", author="Arthur Conan Doyle"),
    ]

    def __init__(self):
        super().__init__()
        self.order_data: dict[str, suggestions.InitSuggestBooksRequest] = {}

    def InitSuggestBooks(self, request: suggestions.InitSuggestBooksRequest, context):
        """Stores order data but doesn't do anything yet."""
        order_id = request.orderId
        self.inc_clock(order_id, message="received order data")
        self.order_data[order_id] = request
        return order.InitResponse()

    def SuggestBooks(self, request: order.OrderInfo, context):
        """Dummy implementation of the book suggestion function."""
        order_id = request.id
        self.update_clock(order_id, request.timestamp, message="received book suggestion request")
        books = random.choices(self.all_suggestions, k=3)
        timestamp = self.inc_clock(order_id, message="picked book suggestions")

        response = order.OrderResponse(timestamp=timestamp, success=True)
        response.suggestions.extend(books)
        return response
    
    def ClearData(self, request: order.OrderInfo, context):
        """Clears data for the given order."""
        order_id = request.id
        if self.is_timestamp_valid(order_id, request.timestamp):
            print(f"{order_id}: clearing data")
            self.order_data.pop(order_id, None)
        return order.ClearDataResponse()
    

def serve():
    # Create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor())
    suggestions_grpc.add_SuggestionServiceServicer_to_server(SuggestionService(), server)
    port = "50053"
    server.add_insecure_port("[::]:" + port)
    server.start()
    print(f"Server started. Listening on port {port}.")
    # Keep thread alive
    server.wait_for_termination()

if __name__ == '__main__':
    serve()