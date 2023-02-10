from orator.orm import belongs_to

from stoobly_agent.app.models.schemas.request import Request

from .base import Base

class Response(Base):
  __fillable__ = ['control','request_id', 'raw']

  @belongs_to
  def request(self):
    return Request