from stoobly_orator.orm import belongs_to

from .base import Base


class ResponseChunk(Base):
  __fillable__ = ['payload', 'response_id', 'sequence']

  @belongs_to
  def response(self):
    from .response import Response
    return Response
