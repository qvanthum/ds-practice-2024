from utils.vectorclock.vectorclock import ClockService
from utils.pb.bookstore import order_pb2 as order
from utils.pb.bookstore import fraud_detection_pb2 as fraud_detection
from utils.pb.bookstore import fraud_detection_pb2_grpc as fraud_detection_grpc
from utils.pb.bookstore import transaction_verification_pb2_grpc as transaction_verification_grpc
from utils.pb.bookstore import suggestions_pb2_grpc as suggestions_grpc
from google.protobuf.empty_pb2 import Empty

import grpc
from concurrent import futures

from opentelemetry.sdk.resources import SERVICE_NAME, Resource

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from opentelemetry import metrics
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader

resource = Resource(attributes={
    SERVICE_NAME: "fraud_detection"
})

traceProvider = TracerProvider(resource=resource)
processor = BatchSpanProcessor(OTLPSpanExporter(endpoint="http://observability:4318/v1/traces"))
traceProvider.add_span_processor(processor)
trace.set_tracer_provider(traceProvider)

reader = PeriodicExportingMetricReader(
    OTLPMetricExporter(endpoint="http://observability:4318/v1/metrics"),
)
meterProvider = MeterProvider(resource=resource, metric_readers=[reader])
metrics.set_meter_provider(meterProvider)

tracer = trace.get_tracer("fraud_detection.tracer")
meter = metrics.get_meter("fraud_detection.meter")
fraudulent_orders = meter.create_counter(
    "fraudulent_orders", description="The number of fraudulent orders", unit="1"
)
non_fraudulent_orders = meter.create_counter(
    "non_fraudulent_orders", description="The number of non-fraudulent orders", unit="1"
)


class FraudDetectionService(ClockService, fraud_detection_grpc.FraudDetectionServiceServicer):
    """
    Concrete implementation of the fraud detection service.
    Currently, it just makes some very simple dummy checks on the user name and credit card.
    """

    # The name of the service, used for the vector clock.
    service_name = "fraudDetection"

    def __init__(self):
        super().__init__()
        self.order_data: dict[str, order.OrderData] = {}

    def InitDetectFraud(self, request: order.OrderData, context):
        """Stores order data but doesn't do anything yet."""
        order_id = request.orderId
        self.inc_clock(order_id, message="received order data")
        self.order_data[order_id] = request
        return Empty()
    
    def DetectUserFraud(self, request: order.OrderInfo, context):
        """Dummy implementation of user fraud detection"""
        order_id = request.id
        self.update_clock(order_id, request.timestamp, message="received user fraud detection request")

        with tracer.start_as_current_span("detect_user_fraud") as span:
            span.set_attribute("order_id", order_id)
            blacklist = ["James"]
            user_data = self.order_data[order_id].userData
            user_fraudulent = user_data.name in blacklist

        timestamp = self.inc_clock(order_id, message=f"verified user data: {'trusted' if not user_fraudulent else 'fraudulent'}")

        if user_fraudulent:
            fraudulent_orders.add(1)
            return order.OrderResponse(timestamp=timestamp, success=False)
        
        with grpc.insecure_channel("transaction_verification:50052") as channel:
            stub = transaction_verification_grpc.TransactionServiceStub(channel)
            return stub.VerifyCreditCard(order.OrderInfo(id=order_id, timestamp=timestamp))
        
    def DetectCreditCardFraud(self, request: order.OrderInfo, context):
        """Dummy implementation of credit card fraud detection"""
        order_id = request.id
        self.update_clock(order_id, request.timestamp, message="received credit card fraud detection request")

        with tracer.start_as_current_span("detect_credit_card_fraud") as span:
            span.set_attribute("order_id", order_id)
            credit_card = self.order_data[order_id].creditCard
            credit_card_fraudulent = credit_card.cvv == "123"
            timestamp = self.inc_clock(order_id, message=f"verified credit card: {'trusted' if not credit_card_fraudulent else 'fraudulent'}")

        if credit_card_fraudulent:
            fraudulent_orders.add(1)
            return order.OrderResponse(timestamp=timestamp, success=False)
        
        non_fraudulent_orders.add(1)
        
        # query book suggestion service
        with grpc.insecure_channel("suggestions:50053") as channel:
            stub = suggestions_grpc.SuggestionServiceStub(channel)
            return stub.SuggestBooks(order.OrderInfo(id=order_id, timestamp=timestamp))
        
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
    fraud_detection_grpc.add_FraudDetectionServiceServicer_to_server(FraudDetectionService(), server)
    port = "50051"
    server.add_insecure_port("[::]:" + port)
    server.start()
    print(f"Server started. Listening on port {port}.")
    # Keep thread alive
    server.wait_for_termination()

if __name__ == '__main__':
    serve()