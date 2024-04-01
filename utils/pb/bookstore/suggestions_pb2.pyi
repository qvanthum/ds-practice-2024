import order_pb2 as _order_pb2
from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class InitSuggestBooksRequest(_message.Message):
    __slots__ = ("orderId", "bookTitles")
    ORDERID_FIELD_NUMBER: _ClassVar[int]
    BOOKTITLES_FIELD_NUMBER: _ClassVar[int]
    orderId: str
    bookTitles: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, orderId: _Optional[str] = ..., bookTitles: _Optional[_Iterable[str]] = ...) -> None: ...
