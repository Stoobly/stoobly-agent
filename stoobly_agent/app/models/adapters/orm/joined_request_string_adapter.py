from stoobly_agent.lib.orm.request import Request
from stoobly_agent.app.proxy.upload import REQUEST_DELIMITTER, RequestString, ResponseString

class JoinedRequestStringAdapter():

  def __init__(self, request: Request):
    self.__request = request

  def adapt(self, base: str = None):
    request_string = RequestString(None) 
    request_string.control = self.__request.control
    request_string.set(self.__request.raw)

    response = self.__request.response
    response_string = ResponseString(None, None)
    response_string.control = response.control
    response_string.set(response.raw)

    toks = [request_string.get(control=True), response_string.get(control=True)]
    if base:
      return REQUEST_DELIMITTER.join([base] + toks)
    else:
      return REQUEST_DELIMITTER.join(toks)