from concurrent import futures
import grpc

from utils.vectorclock.vectorclock import ClockService
from utils.pb.bookstore import order_pb2 as order
from utils.pb.bookstore import transaction_verification_pb2 as transaction_verification
from utils.pb.bookstore import transaction_verification_pb2_grpc as transaction_verification_grpc
from utils.pb.bookstore import fraud_detection_pb2_grpc as fraud_detection_grpc


class TransactionService(ClockService, transaction_verification_grpc.TransactionServiceServicer):
    """
    Concrete implementation of the transaction verification service.
    Currently, it just makes some very simple dummy checks on the credit card and items.
    """

    # The name of the service, used for the vector clock.
    service_name = "transactionVerification"

    def __init__(self):
        super().__init__()
        self.order_data: dict[str, order.OrderData] = {}

    def InitVerifyTransaction(self, request: order.OrderData, context):
        """Stores order data but doesn't do anything yet."""
        order_id = request.orderId
        self.inc_clock(order_id, message="received order data")
        self.order_data[order_id] = request
        return order.EmptyMessage()

    def VerifyItems(self, request: order.OrderInfo, context):
        """Dummy implementation of the item verification function"""
        order_id = request.id
        self.update_clock(order_id, request.timestamp, message="received item verification request")

        items = self.order_data[order_id].items
        items_valid = len(items) > 0
        timestamp = self.inc_clock(order_id, message=f"verified items: {'valid' if items_valid else 'invalid'}")

        if not items_valid:
            return order.OrderResponse(timestamp=timestamp, success=False)
        
        return self.VerifyUserData(order.OrderInfo(id=order_id, timestamp=timestamp), None)

    def VerifyUserData(self, request: order.OrderInfo, context):
        order_id = request.id
        self.update_clock(order_id, request.timestamp, message="received user data verification request")

        user_data = self.order_data[order_id].userData
        data_valid = user_data.name != "" and user_data.address != "" and user_data.contact != ""
        timestamp = self.inc_clock(order_id, message=f"verified user data: {'valid' if data_valid else 'invalid'}")

        if not data_valid:
            return order.OrderResponse(timestamp=timestamp, success=False)
    
        with grpc.insecure_channel("fraud_detection:50051") as channel:
            stub = fraud_detection_grpc.FraudDetectionServiceStub(channel)
            return stub.DetectUserFraud(order.OrderInfo(id=order_id, timestamp=timestamp), None)

    def VerifyCreditCard(self, request: order.OrderInfo, context):
        order_id = request.id
        self.update_clock(order_id, request.timestamp, message="received credit card verification request")

        credit_card = self.order_data[order_id].creditCard
        card_valid = 8 <= len(credit_card.number.replace(" ", "")) <= 19
        card_valid &= 1 <= int(credit_card.expirationDate.split("/")[0]) <= 12
        card_valid &= 0 <= int(credit_card.expirationDate.split("/")[1]) <= 99
        card_valid &= len(credit_card.cvv) == 3
        timestamp = self.inc_clock(order_id, message=f"verified credit card: {'valid' if card_valid else 'invalid'}")

        if not card_valid:
            return order.OrderResponse(timestamp=timestamp, success=False)
        
        with grpc.insecure_channel("fraud_detection:50051") as channel:
            stub = fraud_detection_grpc.FraudDetectionServiceStub(channel)
            return stub.DetectCreditCardFraud(order.OrderInfo(id=order_id, timestamp=timestamp), None)
        
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
    transaction_verification_grpc.add_TransactionServiceServicer_to_server(TransactionService(), server)
    port = "50052"
    server.add_insecure_port("[::]:" + port)
    server.start()
    print(f"Server started. Listening on port {port}.")
    # Keep thread alive
    server.wait_for_termination()

if __name__ == '__main__':
    serve()