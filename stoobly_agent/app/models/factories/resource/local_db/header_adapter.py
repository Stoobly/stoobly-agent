import base64
import json
import pdb
import requests

from typing import List, Tuple

from stoobly_agent.app.models.adapters.raw_http_request_adapter import RawHttpRequestAdapter
from stoobly_agent.lib.api.interfaces import Header, HeaderShowResponse
from stoobly_agent.lib.orm.request import Request

from .local_db_adapter import LocalDBAdapter
from .request_adapter import LocalDBRequestAdapter

class LocalDBHeaderAdapter(LocalDBAdapter):
  __request_orm = None

  def __init__(self, request_orm: Request.__class__ = Request):
    self.__request_orm = request_orm

  def create(self, request_id, **header: Header):
    return self.update(request_id, **header)

  def update(self, request_id, **header: Header):
    request = self.__request_orm.find(request_id)
    
    if not request:
      return self.__request_not_found()

    name = header['name']
    value = header['value']

    request: requests.Request = RawHttpRequestAdapter(request.raw).to_request()
    headers = request.headers
    headers[name] = value

    LocalDBRequestAdapter(self.__request_orm).update(request_id, headers=headers)

    return self.success({
      'name': name,
      'value': value,
    })

  def index(self, request_id, **query_params) -> Tuple[List[HeaderShowResponse], int]:
    request = self.__request_orm.find(request_id)

    if not request:
      return self.__request_not_found()

    request: requests.Request = RawHttpRequestAdapter(request.raw).to_request()

    headers = []
    for key, val in request.headers.items():
      headers.append({
        'name': key,
        'value': val,
      })

    return self.success(headers)

  def destroy(self, request_id, id):
    request = self.__request_orm.find(request_id)
    
    if not request:
      return self.__request_not_found()

    decoded_id = self.__decode_id(id)
    if not decoded_id:
      return self.bad_request('Invalid id')

    python_request: requests.Request = RawHttpRequestAdapter(request.raw).to_request()
    headers = python_request.headers

    header_name = decoded_id['name']
    if not header_name in headers:
      return self.not_found()

    del headers[header_name]

    LocalDBRequestAdapter(self.__request_orm).update(request_id, headers=headers)

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