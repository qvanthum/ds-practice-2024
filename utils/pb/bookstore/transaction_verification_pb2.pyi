import userdata_pb2 as _userdata_pb2
import order_pb2 as _order_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Item(_message.Message):
    __slots__ = ("name", "quantity")
    NAME_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_FIELD_NUMBER: _ClassVar[int]
    name: str
    quantity: int
    def __init__(self, name: _Optional[str] = ..., quantity: _Optional[int] = ...) -> None: ...

class InitVerificationRequest(_message.Message):
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
