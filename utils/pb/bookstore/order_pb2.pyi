import userdata_pb2 as _userdata_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class OrderInfo(_message.Message):
    __slots__ = ("id", "timestamp")
    ID_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    id: str
    timestamp: Timestamp
    def __init__(self, id: _Optional[str] = ..., timestamp: _Optional[_Union[Timestamp, _Mapping]] = ...) -> None: ...

class Item(_message.Message):
    __slots__ = ("name", "quantity")
    NAME_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_FIELD_NUMBER: _ClassVar[int]
    name: str
    quantity: int
    def __init__(self, name: _Optional[str] = ..., quantity: _Optional[int] = ...) -> None: ...

class OrderData(_message.Message):
    __slots__ = ("orderId", "userData", "creditCard", "items")
    ORDERID_FIELD_NUMBER: _ClassVar[int]
    USERDATA_FIELD_NUMBER: _ClassVar[int]
    CREDITCARD_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    orderId: str
    userData: _userdata_pb2.UserData
    creditCard: _userdata_pb2.CreditCard
    items: _containers.RepeatedCompositeFieldContainer[Item]
    def __init__(self, orderId: _Optional[str] = ..., userData: _Optional[_Union[_userdata_pb2.UserData, _Mapping]] = ..., creditCard: _Optional[_Union[_userdata_pb2.CreditCard, _Mapping]] = ..., items: _Optional[_Iterable[_Union[Item, _Mapping]]] = ...) -> None: ...

class Timestamp(_message.Message):
    __slots__ = ("transactionVerification", "fraudDetection", "suggestions")
    TRANSACTIONVERIFICATION_FIELD_NUMBER: _ClassVar[int]
    FRAUDDETECTION_FIELD_NUMBER: _ClassVar[int]
    SUGGESTIONS_FIELD_NUMBER: _ClassVar[int]
    transactionVerification: int
    fraudDetection: int
    suggestions: int
    def __init__(self, transactionVerification: _Optional[int] = ..., fraudDetection: _Optional[int] = ..., suggestions: _Optional[int] = ...) -> None: ...

class BookSuggestion(_message.Message):
    __slots__ = ("id", "title", "author")
    ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    AUTHOR_FIELD_NUMBER: _ClassVar[int]
    id: str
    title: str
    author: str
    def __init__(self, id: _Optional[str] = ..., title: _Optional[str] = ..., author: _Optional[str] = ...) -> None: ...

class ClearDataResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class OrderResponse(_message.Message):
    __slots__ = ("timestamp", "success", "suggestions")
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    SUGGESTIONS_FIELD_NUMBER: _ClassVar[int]
    timestamp: Timestamp
    success: bool
    suggestions: _containers.RepeatedCompositeFieldContainer[BookSuggestion]
    def __init__(self, timestamp: _Optional[_Union[Timestamp, _Mapping]] = ..., success: bool = ..., suggestions: _Optional[_Iterable[_Union[BookSuggestion, _Mapping]]] = ...) -> None: ...
