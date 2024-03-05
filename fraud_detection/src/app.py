import sys
import os

# This set of lines are needed to import the gRPC stubs.
# The path of the stubs is relative to the current file, or absolute inside the container.
# Change these lines only if strictly needed.
FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/fraud_detection'))
sys.path.insert(0, utils_path)
import fraud_detection_pb2 as fraud_detection
import fraud_detection_pb2_grpc as fraud_detection_grpc

import grpc
from concurrent import futures


class FraudDetectionService(fraud_detection_grpc.FraudDetectionServiceServicer):
    """
    Concrete implementation of the fraud detection service.
    Currently, it just makes some very simple dummy checks on the user name and credit card.
    """

    def DetectFraud(self, request, context):
        """Dummy implementation of the fraud detection function"""

        print("Received detect fraud request")
        user_fraudulent = self.is_user_fraudulent(request.userName)
        credit_card_fraudulent = self.is_creditcard_fraudulent(request.creditCard)
        is_fraud = user_fraudulent or credit_card_fraudulent
        if user_fraudulent:
            print("User is fraudulent")
        if credit_card_fraudulent:
            print("Credit card is fraudulent")
        print(f"User is {'fraudulent' if is_fraud else 'not fraudulent'}")
        return fraud_detection.DetectFraudResponse(isFraud=is_fraud)

    @staticmethod
    def is_user_fraudulent(username):
        blacklist = ["James"]
        return username in blacklist
    
    @staticmethod
    def is_creditcard_fraudulent(creditcard):
        return creditcard.cvv == "123"
    
def serve():
    # Create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor())
    fraud_detection_grpc.add_FraudDetectionServiceServicer_to_server(FraudDetectionService(), server)
    port = "50051"
    server.add_insecure_port("[::]:" + port)
    server.start()
    print(f"Server started. Listening on port {port}.")
    # Keep thread alive
    server.wait_for_termination()

if __name__ == '__main__':
    serve()