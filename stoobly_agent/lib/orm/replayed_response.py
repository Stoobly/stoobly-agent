import pdb
import requests

from orator.orm import belongs_to

from stoobly_agent.app.models.schemas.request import Request
from stoobly_agent.app.proxy.mitmproxy.response_facade import MitmproxyResponseFacade
from stoobly_agent.app.proxy.upload.response_string import ResponseString
from stoobly_agent.app.models.adapters.mitmproxy_response_adapter import MitmproxyResponseAdapter

from .base import Base

class ReplayedResponse(Base):
  __fillable__ = ['latency', 'timestamp', 'raw', 'status', 'request_id']

  def with_python_response(self, response: requests.Response):
    http_version = f"HTTP/{response.raw.version / 10.0}"
    mitmproxy_response = MitmproxyResponseAdapter(http_version, response).adapt()
    adapted_response = MitmproxyResponseFacade(mitmproxy_response)
    response_string = ResponseString(adapted_response, None) 
    self.raw = response_string.get()
    self.status = response.status_code

  @belongs_to
  def request(self):
    return Request