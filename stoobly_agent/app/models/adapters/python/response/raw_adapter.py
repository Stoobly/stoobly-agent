import pdb

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from requests import Response

from stoobly_agent.app.proxy.mitmproxy.response_facade import MitmproxyResponseFacade
from stoobly_agent.app.proxy.record.response_string import ResponseString

from .mitmproxy_adapter import MitmproxyResponseAdapter

class RawResponseAdapter():

  def __init__(self, response: 'Response'):
    self.__response = response

  def adapt(self):
    mitmproxy_response = MitmproxyResponseAdapter(self.__response).adapt()
    adapted_response = MitmproxyResponseFacade(mitmproxy_response)
    response_string = ResponseString(adapted_response, None) 
    return response_string.get()