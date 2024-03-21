import userdata_pb2 as _userdata_pb2
import order_pb2 as _order_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class InitDetectFraudRequest(_message.Message):
    __slots__ = ("orderId", "userData", "creditCard")
    ORDERID_FIELD_NUMBER: _ClassVar[int]
    USERDATA_FIELD_NUMBER: _ClassVar[int]
    CREDITCARD_FIELD_NUMBER: _ClassVar[int]
    orderId: str
    userData: _userdata_pb2.UserData
    creditCard: _userdata_pb2.CreditCard
    def __init__(self, orderId: _Optional[str] = ..., userData: _Optional[_Union[_userdata_pb2.UserData, _Mapping]] = ..., creditCard: _Optional[_Union[_userdata_pb2.CreditCard, _Mapping]] = ...) -> None: ...
