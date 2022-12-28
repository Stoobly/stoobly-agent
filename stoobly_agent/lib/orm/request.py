from argparse import ONE_OR_MORE
from orator.orm import has_one

from .base import Base
from .response import Response

class Request(Base):
  __fillable__ = [
    'body_params_hash', 
    'body_text_hash', 
    'committed_at',
    'control',
    'headers_hash', 
    'host', 
    'is_deleted',
    'latency',
    'method', 
    'password',
    'path', 
    'port', 
    'query',
    'query_params_hash', 
    'raw', 
    'scheme', 
    'starred',
    'status',
    'user',
  ]

  @has_one
  def response(self):
    return Response