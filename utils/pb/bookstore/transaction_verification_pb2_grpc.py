# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import order_pb2 as order__pb2
import transaction_verification_pb2 as transaction__verification__pb2


class TransactionServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.InitVerifyTransaction = channel.unary_unary(
                '/bookstore.TransactionService/InitVerifyTransaction',
                request_serializer=transaction__verification__pb2.InitVerificationRequest.SerializeToString,
                response_deserializer=order__pb2.InitResponse.FromString,
                )
        self.VerifyItems = channel.unary_unary(
                '/bookstore.TransactionService/VerifyItems',
                request_serializer=order__pb2.OrderInfo.SerializeToString,
                response_deserializer=order__pb2.OrderResponse.FromString,
                )
        self.VerifyUserData = channel.unary_unary(
                '/bookstore.TransactionService/VerifyUserData',
                request_serializer=order__pb2.OrderInfo.SerializeToString,
                response_deserializer=order__pb2.OrderResponse.FromString,
                )
        self.VerifyCreditCard = channel.unary_unary(
                '/bookstore.TransactionService/VerifyCreditCard',
                request_serializer=order__pb2.OrderInfo.SerializeToString,
                response_deserializer=order__pb2.OrderResponse.FromString,
                )


class TransactionServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def InitVerifyTransaction(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def VerifyItems(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def VerifyUserData(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def VerifyCreditCard(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_TransactionServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'InitVerifyTransaction': grpc.unary_unary_rpc_method_handler(
                    servicer.InitVerifyTransaction,
                    request_deserializer=transaction__verification__pb2.InitVerificationRequest.FromString,
                    response_serializer=order__pb2.InitResponse.SerializeToString,
            ),
            'VerifyItems': grpc.unary_unary_rpc_method_handler(
                    servicer.VerifyItems,
                    request_deserializer=order__pb2.OrderInfo.FromString,
                    response_serializer=order__pb2.OrderResponse.SerializeToString,
            ),
            'VerifyUserData': grpc.unary_unary_rpc_method_handler(
                    servicer.VerifyUserData,
                    request_deserializer=order__pb2.OrderInfo.FromString,
                    response_serializer=order__pb2.OrderResponse.SerializeToString,
            ),
            'VerifyCreditCard': grpc.unary_unary_rpc_method_handler(
                    servicer.VerifyCreditCard,
                    request_deserializer=order__pb2.OrderInfo.FromString,
                    response_serializer=order__pb2.OrderResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'bookstore.TransactionService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class TransactionService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def InitVerifyTransaction(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/bookstore.TransactionService/InitVerifyTransaction',
            transaction__verification__pb2.InitVerificationRequest.SerializeToString,
            order__pb2.InitResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def VerifyItems(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/bookstore.TransactionService/VerifyItems',
            order__pb2.OrderInfo.SerializeToString,
            order__pb2.OrderResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def VerifyUserData(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/bookstore.TransactionService/VerifyUserData',
            order__pb2.OrderInfo.SerializeToString,
            order__pb2.OrderResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def VerifyCreditCard(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/bookstore.TransactionService/VerifyCreditCard',
            order__pb2.OrderInfo.SerializeToString,
            order__pb2.OrderResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)