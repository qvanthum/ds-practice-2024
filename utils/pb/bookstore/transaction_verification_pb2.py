# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: transaction_verification.proto
# Protobuf Python Version: 4.25.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import userdata_pb2 as userdata__pb2
import order_pb2 as order__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1etransaction_verification.proto\x12\tbookstore\x1a\x0euserdata.proto\x1a\x0border.proto\"&\n\x04Item\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x10\n\x08quantity\x18\x02 \x01(\x05\"\x9c\x01\n\x17InitVerificationRequest\x12\x0f\n\x07orderId\x18\x01 \x01(\t\x12%\n\x08userData\x18\x02 \x01(\x0b\x32\x13.bookstore.UserData\x12)\n\ncreditCard\x18\x03 \x01(\x0b\x32\x15.bookstore.CreditCard\x12\x1e\n\x05items\x18\x04 \x03(\x0b\x32\x0f.bookstore.Item2\xf0\x02\n\x12TransactionService\x12T\n\x15InitVerifyTransaction\x12\".bookstore.InitVerificationRequest\x1a\x17.bookstore.InitResponse\x12=\n\x0bVerifyItems\x12\x14.bookstore.OrderInfo\x1a\x18.bookstore.OrderResponse\x12@\n\x0eVerifyUserData\x12\x14.bookstore.OrderInfo\x1a\x18.bookstore.OrderResponse\x12\x42\n\x10VerifyCreditCard\x12\x14.bookstore.OrderInfo\x1a\x18.bookstore.OrderResponse\x12?\n\tClearData\x12\x14.bookstore.OrderInfo\x1a\x1c.bookstore.ClearDataResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'transaction_verification_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_ITEM']._serialized_start=74
  _globals['_ITEM']._serialized_end=112
  _globals['_INITVERIFICATIONREQUEST']._serialized_start=115
  _globals['_INITVERIFICATIONREQUEST']._serialized_end=271
  _globals['_TRANSACTIONSERVICE']._serialized_start=274
  _globals['_TRANSACTIONSERVICE']._serialized_end=642
# @@protoc_insertion_point(module_scope)
