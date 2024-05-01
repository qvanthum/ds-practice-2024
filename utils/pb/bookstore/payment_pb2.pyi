import userdata_pb2 as _userdata_pb2
from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PreparePaymentRequest(_message.Message):
    __slots__ = ("id", "userData", "creditCard", "price")
    ID_FIELD_NUMBER: _ClassVar[int]
    USERDATA_FIELD_NUMBER: _ClassVar[int]
    CREDITCARD_FIELD_NUMBER: _ClassVar[int]
    PRICE_FIELD_NUMBER: _ClassVar[int]
    id: str
    userData: _userdata_pb2.UserData
    creditCard: _userdata_pb2.CreditCard
    price: float
    def __init__(self, id: _Optional[str] = ..., userData: _Optional[_Union[_userdata_pb2.UserData, _Mapping]] = ..., creditCard: _Optional[_Union[_userdata_pb2.CreditCard, _Mapping]] = ..., price: _Optional[float] = ...) -> None: ...

class PreparePaymentResponse(_message.Message):
    __slots__ = ("ready",)
    READY_FIELD_NUMBER: _ClassVar[int]
    ready: bool
    def __init__(self, ready: bool = ...) -> None: ...

class FinalizePaymentRequest(_message.Message):
    __slots__ = ("id", "abort")
    ID_FIELD_NUMBER: _ClassVar[int]
    ABORT_FIELD_NUMBER: _ClassVar[int]
    id: str
    abort: bool
    def __init__(self, id: _Optional[str] = ..., abort: bool = ...) -> None: ...
