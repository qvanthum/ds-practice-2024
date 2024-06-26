import asyncio
from concurrent import futures
import uuid

from utils.vectorclock.vectorclock import timestamp_to_str
from utils.pb.bookstore import order_pb2 as order
from utils.pb.bookstore import userdata_pb2 as userdata
from utils.pb.bookstore.fraud_detection_pb2_grpc import FraudDetectionServiceStub
from utils.pb.bookstore.transaction_verification_pb2_grpc import TransactionServiceStub
from utils.pb.bookstore.suggestions_pb2_grpc import SuggestionServiceStub
from utils.pb.bookstore import suggestions_pb2 as suggestions
from utils.pb.bookstore.order_queue_pb2_grpc import OrderQueueServiceStub

import grpc

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
    SERVICE_NAME: "orchestrator"
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

tracer = trace.get_tracer("orchestrator.tracer")
meter = metrics.get_meter("orchestrator.meter")
order_counter = meter.create_counter(
    "total_orders", description="The number of orders", unit="1"
)


# Import Flask.
# Flask is a web framework for Python.
# It allows you to build a web application quickly.
# For more information, see https://flask.palletsprojects.com/en/latest/
from flask import Flask, request
from flask_cors import CORS

# Create a simple Flask app.
app = Flask(__name__)
# Enable CORS for the app.
CORS(app)
# Create ThreadPoolExecutor for handling gRPC requests.
executor = futures.ThreadPoolExecutor(max_workers=10)


def init_fraud_detection(request: order.OrderData):
    """Initializes the fraud detection."""
    with grpc.insecure_channel('fraud_detection:50051') as channel:
        stub = FraudDetectionServiceStub(channel)
        stub.InitDetectFraud(request)
    

def init_transaction_verification(request: order.OrderData):
    """Initializes the transaction verification."""
    with grpc.insecure_channel('transaction_verification:50052') as channel:
        stub = TransactionServiceStub(channel)
        stub.InitVerifyTransaction(request)
    

def init_suggestions(request: suggestions.InitSuggestBooksRequest):
    """Initializes the book suggestions."""
    with grpc.insecure_channel('suggestions:50053') as channel:
        stub = SuggestionServiceStub(channel)
        stub.InitSuggestBooks(request)


def clear_fraud_detection_data(order_id: str, timestamp: order.Timestamp):
    with grpc.insecure_channel('fraud_detection:50051') as channel:
        stub = FraudDetectionServiceStub(channel)
        stub.ClearData(order.OrderInfo(id=order_id, timestamp=timestamp))


def clear_transaction_verification_data(order_id: str, timestamp: order.Timestamp):
    with grpc.insecure_channel('transaction_verification:50052') as channel:
        stub = TransactionServiceStub(channel)
        stub.ClearData(order.OrderInfo(id=order_id, timestamp=timestamp))


def clear_suggestions_data(order_id: str, timestamp: order.Timestamp):
    with grpc.insecure_channel('suggestions:50053') as channel:
        stub = SuggestionServiceStub(channel)
        stub.ClearData(order.OrderInfo(id=order_id, timestamp=timestamp))


async def clear_data(order_id: str, timestamp: order.Timestamp):
    loop = asyncio.get_event_loop()
    await asyncio.gather(
        loop.run_in_executor(executor, clear_fraud_detection_data, order_id, timestamp),
        loop.run_in_executor(executor, clear_transaction_verification_data, order_id, timestamp),
        loop.run_in_executor(executor, clear_suggestions_data, order_id, timestamp)
    )


async def send_order_data(order_data: order.OrderData):
    """
    Sends all relevant order data to the different microservices.
    """
    suggestion_request = suggestions.InitSuggestBooksRequest(
        orderId=order_data.orderId, bookTitles=[item.name for item in order_data.items]
    )
    loop = asyncio.get_event_loop()
    await asyncio.gather(
        loop.run_in_executor(executor, init_transaction_verification, order_data),
        loop.run_in_executor(executor, init_fraud_detection, order_data),
        loop.run_in_executor(executor, init_suggestions, suggestion_request)
    )


def enqueue_order(order_data: order.OrderData):
    """Sends the order to the order queue."""
    with grpc.insecure_channel('order_queue:50054') as channel:
        stub = OrderQueueServiceStub(channel)
        stub.EnqueueOrder(order_data)


def prepare_order(order_id: str) -> order.OrderResponse:
    """Validates the order with the given ID and returns an OrderResponse with suggestions"""
    with grpc.insecure_channel('transaction_verification:50052') as channel:
        stub = TransactionServiceStub(channel)
        response: order.OrderResponse = stub.VerifyItems(order.OrderInfo(id=order_id))
        return response


@app.route('/checkout', methods=['POST'])
async def checkout():
    """ 
    Responds with a JSON object containing the order ID, status, and suggested books.
    """
    with tracer.start_as_current_span("checkout"):
        loop = asyncio.get_event_loop()
        print("--- receiving new checkout request ---")
        order_counter.add(1)

        # --- read input data and prepare microservice requests ---
        with tracer.start_as_current_span("parse_request"):
            print("Parsing request...")
            try:
                # just using the spread operator for creating the data objects
                # is hacky and shouldl not be done in production
                user_data = userdata.UserData(
                    name=request.json['user']['name'],
                    contact=request.json['user']['contact'],
                    address=userdata.Address(**request.json['billingAddress'])
                )
                credit_card = userdata.CreditCard(**request.json['creditCard'])
                items = [order.Item(**item) for item in request.json['items']]
            except (KeyError, TypeError) as e:
                print(repr(e))
                return {
                    'code': "400",
                    'message': "Invalid request",
                }, 400

        # --- prepare order ---
        with tracer.start_as_current_span("send_order_data"):
            order_id = str(uuid.uuid1())
            order_data = order.OrderData(
                orderId=order_id, userData=user_data, creditCard=credit_card, items=items
            )
            print(f"{order_id}: sending order data to microservices...")
            await send_order_data(order_data)
        trace.get_current_span().set_attribute("order_id", order_id)

        with tracer.start_as_current_span("prepare_order"):
            print(f"{order_id}: executing order...")
            order_response = await loop.run_in_executor(executor, prepare_order, order_id)
            order_approved = order_response.success
            print(
                f"Order {order_id} was executed and is {'approved' if order_approved else 'rejected'}\n"
                f"Final timestamp: {timestamp_to_str(order_response.timestamp)}"
            )

        with tracer.start_as_current_span("clear_data"):
            print(f"{order_id}: asking services to clear data...")
            await clear_data(order_id, order_response.timestamp)

        # --- add order to queue ---
        if order_approved:
            with tracer.start_as_current_span("enqueue_order"):
                print(f"{order_id}: sending order to queue...")
                await loop.run_in_executor(executor, enqueue_order, order_data)

        # --- send response ---
        with tracer.start_as_current_span("send_response"):
            order_status_response = {
                'orderId': order_id,
                'status': 'Order Approved' if order_approved else 'Order Rejected',
                'suggestedBooks': [
                    {
                        'id': book.id,
                        'title': book.title,
                        'author': book.author
                    }
                    for book in order_response.suggestions
                ]
            }

        return order_status_response


if __name__ == '__main__':
    # Run the app in debug mode to enable hot reloading.
    # This is useful for development.
    # The default port is 5000.
    app.run(host='0.0.0.0')
