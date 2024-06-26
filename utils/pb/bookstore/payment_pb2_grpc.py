# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
import payment_pb2 as payment__pb2


class PaymentServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.PreparePayment = channel.unary_unary(
                '/bookstore.PaymentService/PreparePayment',
                request_serializer=payment__pb2.PreparePaymentRequest.SerializeToString,
                response_deserializer=payment__pb2.PreparePaymentResponse.FromString,
                )
        self.FinalizePayment = channel.unary_unary(
                '/bookstore.PaymentService/FinalizePayment',
                request_serializer=payment__pb2.FinalizePaymentRequest.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )


class PaymentServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def PreparePayment(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def FinalizePayment(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_PaymentServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'PreparePayment': grpc.unary_unary_rpc_method_handler(
                    servicer.PreparePayment,
                    request_deserializer=payment__pb2.PreparePaymentRequest.FromString,
                    response_serializer=payment__pb2.PreparePaymentResponse.SerializeToString,
            ),
            'FinalizePayment': grpc.unary_unary_rpc_method_handler(
                    servicer.FinalizePayment,
                    request_deserializer=payment__pb2.FinalizePaymentRequest.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'bookstore.PaymentService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class PaymentService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def PreparePayment(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/bookstore.PaymentService/PreparePayment',
            payment__pb2.PreparePaymentRequest.SerializeToString,
            payment__pb2.PreparePaymentResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def FinalizePayment(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/bookstore.PaymentService/FinalizePayment',
            payment__pb2.FinalizePaymentRequest.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
