import order_pb2 as _order_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class OptionalOrder(_message.Message):
    __slots__ = ("order",)
    ORDER_FIELD_NUMBER: _ClassVar[int]
    order: _order_pb2.OrderData
    def __init__(self, order: _Optional[_Union[_order_pb2.OrderData, _Mapping]] = ...) -> None: ...
