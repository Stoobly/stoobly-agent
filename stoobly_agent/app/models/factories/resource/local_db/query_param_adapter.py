import base64
import json
import pdb
import requests

from typing import List
from urllib.parse import parse_qs, urlencode, urlparse

from stoobly_agent.lib.api.interfaces import QueryParam, QueryParamShowResponse
from stoobly_agent.lib.orm.request import Request

from .request_adapter import LocalDBRequestAdapter

class LocalDBQueryParamAdapter():
  __request_orm = None

  def __init__(self, request_orm: Request.__class__ = Request):
    self.__request_orm = request_orm

  def create(self, request_id, **params: QueryParam):
    request = self.__request_orm.find(request_id)
    
    if not request:
      return None

    parsed_url = urlparse(request.url)

    _query_params = parse_qs(parsed_url.query)
    if not params['name'] in _query_params:
      _query_params[params['name']] = []

    if params['value'] not in _query_params[params['name']]:
      _query_params[params['name']].append(params['value'])
      parsed_url = parsed_url._replace(query=urlencode(_query_params, True))

    request = LocalDBRequestAdapter(self.__request_orm).update(request_id, url=parsed_url.geturl())

    return {
      'name': params['name'],
      'value': params['value'],
    }

  def update(self, request_id, query_param_id, **params: QueryParam) -> QueryParamShowResponse:
    request = self.__request_orm.find(request_id)
    
    if not request:
      return None

    decoded_id = self.__decode_id(query_param_id)
    if not decoded_id:
      return None

    name = params['name']
    value = params['value']
    parsed_url = urlparse(request.url)

    _query_params = parse_qs(parsed_url.query)
    if not name in _query_params:
      _query_params[name] = []

    try:
      index = _query_params[name].index(decoded_id['value'])
    except ValueError as e:
      return None

    _query_params[name][index] = value
    parsed_url = parsed_url._replace(query=urlencode(_query_params, True))

    request = LocalDBRequestAdapter(self.__request_orm).update(request_id, url=parsed_url.geturl())

    return {
      'name': name,
      'value': value,
    }

  def index(self, request_id, **query_params) -> List[QueryParamShowResponse]:
    request = self.__request_orm.find(request_id)

    if not request:
      return []

    request_dict = request.to_dict()
    parsed_query = parse_qs(request_dict['query'])

    query_params = []
    for key, params in parsed_query.items():
      for param in params:
        query_params.append({
          'name': key,
          'value': param,
        })

    return query_params

  def destroy(self, request_id, id):
    request = self.__request_orm.find(request_id)
    
    if not request:
      return None

    decoded_id = self.__decode_id(id)
    if not decoded_id or not decoded_id.get('value'):
      return None

    parsed_url = urlparse(request.url)
    _query_params = parse_qs(parsed_url.query)

    name = decoded_id['name']
    value = decoded_id['value']

    try:
      index = _query_params[name].index(value)
    except ValueError as e:
      return None

    del _query_params[name][index]

    parsed_url = parsed_url._replace(query=urlencode(_query_params, True))
    request = LocalDBRequestAdapter(self.__request_orm).update(request_id, url=parsed_url.geturl())

    return {
      'name': name,
      'value': value,
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

    if not id.get('value'):
      return None

    return id