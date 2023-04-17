import base64
import json
import pdb
import requests

from typing import List

from stoobly_agent.app.models.adapters.raw_http_response_adapter import RawHttpResponseAdapter
from stoobly_agent.lib.api.interfaces import Header, HeaderShowResponse
from stoobly_agent.lib.orm.request import Request

from .response_adapter import LocalDBResponseAdapter

class LocalDBResponseHeaderAdapter():
  __request_orm = None

  def __init__(self, request_orm: Request.__class__ = Request):
    self.__request_orm = request_orm

  def create(self, request_id, **header: Header):
    return self.update(request_id, **header)

  def update(self, request_id, **header: Header):
    request = self.__request_orm.find(request_id)
    
    if not request:
      return None

    response = request.response

    if not response:
      return None

    name = header['name']
    value = header['value']

    python_response: requests.Response = RawHttpResponseAdapter(response.raw).to_response()
    headers = python_response.headers
    headers[name] = value

    LocalDBResponseAdapter(self.__request_orm).update(request_id, headers=headers)

    return {
      'name': name,
      'value': value,
    }

  def index(self, response_id, **query_params) -> List[HeaderShowResponse]:
    request = self.__request_orm.find(response_id)

    if not request:
      return []

    response = request.response

    if not response:
      return []

    response: requests.Response = RawHttpResponseAdapter(response.raw).to_response()

    headers = []
    for key, val in response.headers.items():
      headers.append({
        'name': key,
        'value': val,
      })

    return headers

  def destroy(self, request_id, id):
    request = self.__request_orm.find(request_id)
    
    if not request:
      return None

    response = request.response

    if not response:
      return None

    decoded_id = self.__decode_id(id)
    if not decoded_id:
      return None

    response: requests.Request = RawHttpResponseAdapter(response.raw).to_response()
    headers = response.headers
    del headers[decoded_id['name']]

    LocalDBResponseAdapter(self.__request_orm).update(request_id, headers=headers)

    return {
      'name': decoded_id['name'],
    }

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