from concurrent import futures
import random
from utils.pb.bookstore import payment_pb2 as payment
from utils.pb.bookstore import payment_pb2_grpc as payment_grpc
from google.protobuf.empty_pb2 import Empty

import grpc


class PaymentService(payment_grpc.PaymentServiceServicer):
    """
    Dummy implementation of the payment service.
    It supports the 2PC protocol for payment processing.
    """

    def __init__(self):
        self.payments: dict[str, payment.PreparePaymentRequest] = {}

    def PreparePayment(self, request: payment.PreparePaymentRequest, context):
        """Checks if payment is possible and stores the data for future execution."""
        # dummy implementation of payment preparation
        # randomly reject 10% of payments
        is_possible = random.random() > 0.1
        print(f"Payment request {request.id} for {request.userData.name} {'accepted' if is_possible else 'rejected'}")
        self.payments[request.id] = request
        return payment.PreparePaymentResponse(ready=is_possible)
        
    def FinalizePayment(self, request: payment.FinalizePaymentRequest, context):
        """Executes the payment of the ID given in the request."""
        payment_request = self.payments.pop(request.id)
        print(f"Payment request {request.id} for {payment_request.userData.name} {'aborted' if request.abort else 'executed'}")
        return Empty()
    
def serve():
    # Create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor())
    payment_grpc.add_PaymentServiceServicer_to_server(PaymentService(), server)
    port = "50055"
    server.add_insecure_port("[::]:" + port)
    server.start()
    print(f"Server started. Listening on port {port}.")
    # Keep thread alive
    server.wait_for_termination()

if __name__ == '__main__':
    serve()