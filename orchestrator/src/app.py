import asyncio
from concurrent import futures
import uuid

from utils.vectorclock.vectorclock import timestamp_to_str
from utils.pb.bookstore import order_pb2 as order
from utils.pb.bookstore import userdata_pb2 as userdata
from utils.pb.bookstore.fraud_detection_pb2_grpc import FraudDetectionServiceStub
from utils.pb.bookstore import fraud_detection_pb2 as fraud_detection
from utils.pb.bookstore.transaction_verification_pb2_grpc import TransactionServiceStub
from utils.pb.bookstore import transaction_verification_pb2 as transaction_verification
from utils.pb.bookstore.suggestions_pb2_grpc import SuggestionServiceStub
from utils.pb.bookstore import suggestions_pb2 as suggestions

import grpc


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


def init_fraud_detection(request: fraud_detection.InitDetectFraudRequest):
    """Initializes the fraud detection."""
    with grpc.insecure_channel('fraud_detection:50051') as channel:
        stub = FraudDetectionServiceStub(channel)
        stub.InitDetectFraud(request)
    

def init_transaction_verification(request: transaction_verification.InitVerificationRequest):
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


async def send_order_data(order_id: str, user_data: userdata.UserData, credit_card: userdata.CreditCard, items: list[transaction_verification.Item]):
    """
    Sends all relevant order data to the different microservices.
    """
    transaction_verification_request = transaction_verification.InitVerificationRequest(
        orderId=order_id, userData=user_data, creditCard=credit_card, items=items
    )
    fraud_detection_request = fraud_detection.InitDetectFraudRequest(
        orderId=order_id, userData=user_data, creditCard=credit_card
    )
    suggestion_request = suggestions.InitSuggestBooksRequest(
        orderId=order_id, bookTitles=[item.name for item in items]
    )
    loop = asyncio.get_event_loop()
    await asyncio.gather(
        loop.run_in_executor(executor, init_transaction_verification, transaction_verification_request),
        loop.run_in_executor(executor, init_fraud_detection, fraud_detection_request),
        loop.run_in_executor(executor, init_suggestions, suggestion_request)
    )


def execute_order_sync(order_id: str) -> order.OrderResponse:
    """Executes the order with the given ID and returns an OrderResponse"""
    with grpc.insecure_channel('transaction_verification:50052') as channel:
        stub = TransactionServiceStub(channel)
        response: order.OrderResponse = stub.VerifyItems(order.OrderInfo(id=order_id))
        return response
    

async def execute_order(order_id: str) -> order.OrderResponse:
    """Executes the order with the given ID and returns an OrderResponse"""
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, execute_order_sync, order_id)


@app.route('/checkout', methods=['POST'])
async def checkout():
    """
    Responds with a JSON object containing the order ID, status, and suggested books.
    """
    print("--- receiving new checkout request ---")

    # --- read input data and prepare microservice requests ---
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
        items = [transaction_verification.Item(**item) for item in request.json['items']]
    except (KeyError, TypeError) as e:
        print(repr(e))
        return {
            'code': "400",
            'message': "Invalid request",
        }, 400

    # --- execute order workflow ---
    order_id = str(uuid.uuid1())
    print(f"{order_id}: sending order data to microservices...")
    await send_order_data(order_id, user_data, credit_card, items)

    print(f"{order_id}: executing order...")
    order_response = await execute_order(order_id)
    order_approved = order_response.success
    print(
        f"Order {order_id} was executed and is {'approved' if order_approved else 'rejected'}\n"
        f"Final timestamp: {timestamp_to_str(order_response.timestamp)}"
    )

    # --- clear data ---
    print(f"{order_id}: asking services to clear data...")
    await clear_data(order_id, order_response.timestamp)

    # --- send response ---
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
