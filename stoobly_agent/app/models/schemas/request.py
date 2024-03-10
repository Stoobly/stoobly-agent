import base64
import copy
import pdb

from mitmproxy.net.http.url import encode as urlencode
from mitmproxy.coretypes.multidict import MultiDict
from urllib.parse import urlparse
from typing import List, Union

from stoobly_agent.app.proxy.replay.body_parser_service import decode_response, encode_response, is_traversable
from stoobly_agent.lib.api.interfaces.endpoints import RequestComponentName
from stoobly_agent.lib.api.interfaces import RequestShowResponse

class Request():

  def __init__(self, request: RequestShowResponse):
    self.request = request
    self.__url = urlparse(request.get('url'))

  def clone(self):
    return Request(copy.deepcopy(self.request))

  @property
  def host(self):
    return self.__url.netloc

  @host.setter
  def host(self, v):
    self.__url = self.__url._replace(netloc=v)

  @property
  def http_version(self):
    return self.request.get('http_version')

  @property
  def key(self):
    return self.request.get('key')

  @property
  def scheme(self):
    return self.__url.scheme

  @scheme.setter
  def scheme(self, v):
    self.__url = self.__url._replace(scheme=v)

  @property
  def id(self):
    return self.request.get('id')

  @property
  def endpoint_id(self):
    return self.request.get('endpoint_id')

  @property
  def url(self) -> str:
    query_params = self.query_params

    query_tuples = []
    for key in query_params:
      for value in query_params.get_all(key):
        if not isinstance(value, list):
          query_tuples.append((key, value))
        else:
          for v in value:
            query_tuples.append((key, v))

    url = self.__url._replace(path=self.path, query=urlencode(query_tuples))
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
  def headers(self) -> MultiDict:
    headers = MultiDict()

    for header in (self.request.get('headers') or []):
      headers.add(header['name'], header['value'])

    return headers 

  @headers.setter
  def headers(self, v: MultiDict):
    self.__set_dict('headers', v)

  @property
  def query(self) -> str:
    return urlencode(self.query_params)

  @property
  def query_params(self) -> MultiDict:
    query_params = MultiDict()

    for query_param in (self.request.get('query_params') or []):
      query_params.add(query_param['name'], query_param['value'])

    return query_params

  @query_params.setter
  def query_params(self, v: MultiDict):
    self.__set_dict('query_params', v) 
  
  @property
  def body(self):
    encoded_body = self.request.get('body')
    if not encoded_body:
      return ''

    try:
      return base64.b64decode(encoded_body)
    except Exception as e:
      return encoded_body

  @body.setter
  def body(self, v: Union[bytes, str]):
    if not 'body' in self.request:
      return

    text = v if isinstance(v, bytes) else v.encode()
    self.request['body'] = base64.b64encode(text)

    headers = self.headers
    if 'content-length' in headers:
      headers['content-length'] = str(len(text))
      self.headers = headers

  @property
  def body_params(self):
    _body = self.body
    return decode_response(_body, self.headers.get('content-type'))

  @body_params.setter
  def body_params(self, v):
    if not is_traversable(v):
      self.body = v
    else:
      content_type = self.headers.get('content-type')
      if content_type:
        self.body = encode_response(v, content_type)

  def __set_dict(self, component_name_str, v: MultiDict):
    component_names: List[RequestComponentName] = self.request[component_name_str] or []

    indexes = {}
    new_component_names = []
    for component_name in component_names:
      name = component_name['name']
      if name in v:
        value = v.get_all(name)

        if isinstance(value, list):
          if name not in indexes:
            indexes[name] = 0
          else:
            indexes[name] += 1

          index = indexes[name]

          if len(value) <= index:
            continue

          component_name['value'] = value[index]
        else:
          component_name['value'] = value

      new_component_names.append(component_name)

    # If a component was set that doesn't exist in the request template, add it
    for key in v:
      if key in indexes:
        continue
      
      value = v.get_all(key)

      if isinstance(value, list):
        for val in value:
          new_component_names.append({
            'name': key,
            'value': val,
          })
      else:
        new_component_names.append({
          'name': key,
          'value': value,
        })

    self.request[component_name_str] = new_component_names