# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: bookstore/books_service.proto
# Protobuf Python Version: 4.25.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1d\x62ookstore/books_service.proto\"\x1a\n\x0bReadRequest\x12\x0b\n\x03key\x18\x01 \x01(\t\"\x1d\n\x0cReadResponse\x12\r\n\x05value\x18\x01 \x01(\t\"*\n\x0cWriteRequest\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t\" \n\rWriteResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x32\\\n\rBooksDatabase\x12#\n\x04Read\x12\x0c.ReadRequest\x1a\r.ReadResponse\x12&\n\x05Write\x12\r.WriteRequest\x1a\x0e.WriteResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'bookstore.books_service_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_READREQUEST']._serialized_start=33
  _globals['_READREQUEST']._serialized_end=59
  _globals['_READRESPONSE']._serialized_start=61
  _globals['_READRESPONSE']._serialized_end=90
  _globals['_WRITEREQUEST']._serialized_start=92
  _globals['_WRITEREQUEST']._serialized_end=134
  _globals['_WRITERESPONSE']._serialized_start=136
  _globals['_WRITERESPONSE']._serialized_end=168
  _globals['_BOOKSDATABASE']._serialized_start=170
  _globals['_BOOKSDATABASE']._serialized_end=262
# @@protoc_insertion_point(module_scope)
