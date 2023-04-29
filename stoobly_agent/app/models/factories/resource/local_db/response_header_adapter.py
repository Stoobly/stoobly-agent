import base64
import json
import pdb
import requests

from typing import List, Tuple

from stoobly_agent.app.models.adapters.raw_http_response_adapter import RawHttpResponseAdapter
from stoobly_agent.lib.api.interfaces import Header, HeaderShowResponse
from stoobly_agent.lib.orm.request import Request

from .local_db_adapter import LocalDBAdapter
from .response_adapter import LocalDBResponseAdapter

class LocalDBResponseHeaderAdapter(LocalDBAdapter):
  __request_orm = None

  def __init__(self, request_orm: Request.__class__ = Request):
    self.__request_orm = request_orm

  def create(self, request_id, **header: Header):
    return self.update(request_id, **header)

  def update(self, request_id, **header: Header):
    request = self.__request_orm.find(request_id)
    
    if not request:
      return self.__request_not_found()

    response = request.response

    if not response:
      return self.__response_not_found()

    name = header['name']
    value = header['value']

    python_response: requests.Response = RawHttpResponseAdapter(response.raw).to_response()
    headers = python_response.headers
    headers[name] = value

    LocalDBResponseAdapter(self.__request_orm).update(request_id, headers=headers)

    return self.success({
      'name': name,
      'value': value,
    })

  def index(self, response_id, **query_params) -> Tuple[List[HeaderShowResponse], int]:
    request = self.__request_orm.find(response_id)

    if not request:
      return self.__request_not_found()

    response = request.response
    if not response:
      return self.__response_not_found()

    response: requests.Response = RawHttpResponseAdapter(response.raw).to_response()

    headers = []
    for key, val in response.headers.items():
      headers.append({
        'name': key,
        'value': val,
      })

    return self.success(headers)

  def destroy(self, request_id, id):
    request = self.__request_orm.find(request_id)
    
    if not request:
      return self.__request_not_found()

    response = request.response
    if not response:
      return self.__response_not_found()

    decoded_id = self.__decode_id(id)
    if not decoded_id:
      return self.bad_request('Invalid id')

    response: requests.Request = RawHttpResponseAdapter(response.raw).to_response()
    headers = response.headers

    header_name = decoded_id['name'] 
    if not header_name in headers:
      return self.not_found('Response header not found')

    del headers[header_name]

    LocalDBResponseAdapter(self.__request_orm).update(request_id, headers=headers)

    return self.success({
      'name': decoded_id['name'],
    })

  def __decode_id(self, id: str):
    id = base64.b64decode(id)

    try:
      id = json.loads(id)
    except Exception as e:
      return None

    if not isinstance(id, dict):
      return None

    if not id.get('name'):
      return None

    return id

  def __request_not_found(self):
    return self.not_found('Request not found')

  def __response_not_found(self):
    return self.not_found('Response not found')