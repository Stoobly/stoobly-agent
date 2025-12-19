import pdb

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from requests import Response

from stoobly_orator.orm import belongs_to

from stoobly_agent.app.proxy.mitmproxy.response_facade import MitmproxyResponseFacade
from stoobly_agent.app.proxy.record.response_string import ResponseString
from stoobly_agent.app.models.adapters.python import PythonResponseAdapterFactory

from .base import Base

class ReplayedResponse(Base):
  __fillable__ = ['latency', 'timestamp', 'raw', 'status', 'request_id']

  def with_python_response(self, response: 'Response'):
    mitmproxy_response = PythonResponseAdapterFactory(response).mitmproxy_response()
    adapted_response = MitmproxyResponseFacade(mitmproxy_response)
    response_string = ResponseString(adapted_response, None) 
    self.raw = response_string.get()

    self.status = response.status_code

  @belongs_to
  def request(self):
    from .request import Request
    return Request

  # Override
  def to_dict(self):
    return super().attributes_to_dict()