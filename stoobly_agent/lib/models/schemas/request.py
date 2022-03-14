import base64

from stoobly_agent.lib.api.interfaces.request_show_response import RequestShowResponse

class Request():

  def __init__(self, response: RequestShowResponse):
    self.response = response

  @property
  def id(self):
    return self.response.get('id')

  @property
  def url(self) -> str:
    return self.response['url']

  @property
  def method(self) -> str:
    return self.response['method']

  @property
  def headers(self) -> dict:
    headers = {}

    for header in (self.response['headers'] or []):
      headers[header['name']] = header['value']

    return headers 

  @property
  def query_params(self) -> dict:
    query_params = {}

    for query_param in (self.response['query_params'] or []):
      query_params[query_param['name']] = query_param['value']

    return query_params
  
  @property
  def body(self):
    encoded_body = self.response.get('body')
    if not encoded_body:
      return ''

    return base64.b64decode(encoded_body)