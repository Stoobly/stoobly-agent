import base64
import pdb

from urllib.parse import urlencode, urlparse
from stoobly_agent.lib.api.interfaces.endpoints import RequestComponentName
from typing import List

from stoobly_agent.lib.api.interfaces.request_show_response import RequestShowResponse

class Request():

  def __init__(self, request: RequestShowResponse):
    self.request = request
    self.__url = urlparse(request.get('url'))

  @property
  def id(self):
    return self.request.get('id')

  @property
  def endpoint_id(self):
    return self.request.get('endpoint_id')

  @property
  def url(self) -> str:
    url = self.__url._replace(path=self.path, query=urlencode(self.query_params))
    return url.geturl()

  @property
  def path(self) -> str:
    return self.request.get('path') or ''

  @path.setter
  def path(self, v):
    self.request['path'] = v

  @property
  def path_segment_strings(self):
    segment_strings = self.path.split('/')
    if len(segment_strings) == 0:
      return segment_strings

    if segment_strings[0] == '':
      segment_strings.pop(0)

    return segment_strings

  @property
  def method(self) -> str:
    return self.request['method']

  @property
  def headers(self) -> dict:
    headers = {}

    for header in (self.request['headers'] or []):
      headers[header['name']] = header['value']

    return headers 

  @headers.setter
  def headers(self, v):
    self.__set_dict('headers', v)

  @property
  def query_params(self) -> dict:
    query_params = {}

    for query_param in (self.request['query_params'] or []):
      query_params[query_param['name']] = query_param['value']

    return query_params

  @query_params.setter
  def query_params(self, v: dict):
    self.__set_dict('query_params', v) 
  
  @property
  def body(self):
    encoded_body = self.request.get('body')
    if not encoded_body:
      return ''

    return base64.b64decode(encoded_body)

  def __set_dict(self, component_name_str, v):
    component_names: List[RequestComponentName] = self.request[component_name_str] or []

    for component_name in component_names:
      name = component_name['name']
      if name in v:
        component_name['value'] = v[name]