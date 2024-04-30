import pdb
import requests

from io import BytesIO
from urllib3 import HTTPResponse
from typing import TypedDict, Union

from stoobly_agent.app.models.helpers.create_request_params_service import build_params_from_python
from stoobly_agent.app.models.request_model import RequestModel
from stoobly_agent.app.proxy.replay.body_parser_service import encode_response
from stoobly_agent.app.settings import Settings

class RequestProperties(TypedDict):
  url: str
  method: str
  request_body: bytes
  request_headers: dict
  response_body: bytes
  response_headers: bytes
  status_code: int

class RequestBuilder():

  def __init__(self, **properties: RequestProperties):
    self.__properties = properties
    self.__settings = None

  def with_settings(self, settings: Settings):
    self.__settings = settings
    return self

  @property
  def method(self):
    return self.__properties.get('method').upper()

  @property
  def request_body(self):
    return self.__properties.get('request_body') or b''

  @property
  def request_headers(self):
    return self.__properties.get('request_headers') or {}

  @property
  def response_body(self):
    return self.__properties.get('response_body')

  @property
  def response_headers(self):
    return self.__properties.get('response_headers') or {}

  @property
  def settings(self):
    return self.__settings or Settings.instance()

  @property
  def status_code(self):
    return self.__properties.get('status_code') or 0

  @property
  def url(self):
    return self.__properties.get('url')

  def build(self):
    req = requests.Request(
      method=self.method,
      url=self.url,
      headers=self.request_headers,
      data=self.serialized_request_body(self.request_headers_value('content-type')),
    )
    
    res = requests.Response()
    res.headers = self.response_headers
    res.raw = HTTPResponse(
        body=BytesIO(
          self.serialized_response_body(self.response_headers_value('content-type')),
        ),
        decode_content=False,
        headers=self.response_headers,
        preload_content=False
    ) 
    res.status_code = self.status_code

    params = build_params_from_python(req, res)

    model = RequestModel(self.settings)
    return model.create(**params)

  def request_headers_value(self, header_name: str):
    headers = self.request_headers
    return self.__header_value(header_name, headers)

  def response_headers_value(self, header_name: str):
    headers = self.response_headers
    return self.__header_value(header_name, headers)

  def serialized_request_body(self, content_type: str):
    body = self.request_body
    return self.__serialize_body(body, content_type)

  def serialized_response_body(self, content_type: str):
    body = self.response_body
    return self.__serialize_body(body, content_type)

  def __header_value(self, header_name: str, headers: dict):
    for k in headers:
      if header_name.lower() == k.lower():
        return headers[k]

  def __serialize_body(self, body: Union[bytes, str], content_type: str):
    if not isinstance(body, bytes) or not isinstance(body, str): 
      body = encode_response(body, content_type)
    return body if isinstance(body, bytes) else body.encode()

