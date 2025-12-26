from stoobly_orator.orm import belongs_to

from .base import Base

class Response(Base):
  __fillable__ = ['control', 'http_version', 'request_id', 'raw']

  @belongs_to
  def request(self):
    from .request import Request
    return Request