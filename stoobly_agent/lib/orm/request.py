from argparse import ONE_OR_MORE
from orator.orm import has_one

from .base import Base
from .response import Response

class Request(Base):
  __fillable__ = [
    'control',
    'scheme', 
    'method', 
    'host', 
    'path', 
    'port', 
    'headers_hash', 
    'body_text_hash', 
    'query_params_hash', 
    'body_params_hash', 
    'raw', 
    'committed_at'
  ]

  @has_one
  def response(self):
    return Response