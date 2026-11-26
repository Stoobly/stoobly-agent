from stoobly_orator.orm import belongs_to, has_many

from .base import Base

class Response(Base):
  __fillable__ = ['control', 'http_version', 'request_id', 'raw', 'stream_status']

  @belongs_to
  def request(self):
    from .request import Request
    return Request

  @has_many
  def chunks(self):
    from .response_chunk import ResponseChunk
    return ResponseChunk

def handle_deleting(response):
  from .response_chunk import ResponseChunk
  for chunk in ResponseChunk.where('response_id', response.id).get():
    chunk.delete()

Response.deleting(handle_deleting)
