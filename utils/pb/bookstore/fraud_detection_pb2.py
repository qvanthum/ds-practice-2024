# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: fraud_detection.proto
# Protobuf Python Version: 4.25.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import order_pb2 as order__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x15\x66raud_detection.proto\x12\tbookstore\x1a\x0border.proto2\xa6\x02\n\x15\x46raudDetectionService\x12@\n\x0fInitDetectFraud\x12\x14.bookstore.OrderData\x1a\x17.bookstore.EmptyMessage\x12\x41\n\x0f\x44\x65tectUserFraud\x12\x14.bookstore.OrderInfo\x1a\x18.bookstore.OrderResponse\x12G\n\x15\x44\x65tectCreditCardFraud\x12\x14.bookstore.OrderInfo\x1a\x18.bookstore.OrderResponse\x12?\n\tClearData\x12\x14.bookstore.OrderInfo\x1a\x1c.bookstore.ClearDataResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'fraud_detection_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_FRAUDDETECTIONSERVICE']._serialized_start=50
  _globals['_FRAUDDETECTIONSERVICE']._serialized_end=344
# @@protoc_insertion_point(module_scope)
