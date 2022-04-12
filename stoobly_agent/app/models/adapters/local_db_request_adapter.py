import pdb
import requests

from mitmproxy.http import HTTPFlow as MitmproxyHTTPFlow, HTTPRequest as MitmproxyRequest, HTTPResponse as MitmproxyResponse
from typing import List

from stoobly_agent.app.proxy.mock.custom_not_found_response_builder import CustomNotFoundResponseBuilder
from stoobly_agent.app.proxy.mock.hashed_request_decorator import HashedRequestDecorator
from stoobly_agent.app.proxy.mitmproxy.request_facade import MitmproxyRequestFacade
from stoobly_agent.app.proxy.upload.joined_request import JoinedRequest

from stoobly_agent.lib.api.keys.request_key import RequestKey
from stoobly_agent.lib.orm import ORM
from stoobly_agent.lib.orm.request import Request
from stoobly_agent.lib.orm.response import Response
from stoobly_agent.lib.orm.transformers.orm_to_stoobly_request_transformer import ORMTOStooblyRequestTransformer
from stoobly_agent.lib.orm.types.request_columns import RequestColumns
from stoobly_agent.lib.orm.types.response_columns import ResponseColumns
from stoobly_agent.lib.orm.transformers import ORMToRequestsResponseTransformer, ORMTOStooblyResponseTransformer
from stoobly_agent.lib.api.interfaces import RequestsIndexQueryParams, RequestsIndexResponse, RequestShowResponse

from .types import RequestCreateParams, RequestShowParams

class LocalDBRequestAdapter():
  __request_orm = None
  __response_orm = None

  def __init__(self, request_orm: Request.__class__ = Request, response_orm: Response.__class__ = Response):
    self.__request_orm = request_orm
    self.__response_orm = response_orm

  def create(self, **params: RequestCreateParams) -> RequestShowResponse:
    flow: MitmproxyHTTPFlow = params['flow']
    joined_request: JoinedRequest = params['joined_request']

    request: MitmproxyRequest = flow.request
    hashed_request = HashedRequestDecorator(MitmproxyRequestFacade(request))

    with ORM.instance().db.transaction():
      request_columns: RequestColumns = {
        'body_params_hash': hashed_request.body_params_hash(),
        'body_text_hash': hashed_request.body_text_hash(),
        'control': joined_request.request_string.control(), 
        'headers_hash': hashed_request.headers_hash(),
        'host': request.host,
        'method': request.method,
        'path': request.path,
        'port': request.port,
        'query_params_hash': hashed_request.query_params_hash(),
        'raw': joined_request.request_string.get(),
        'scheme': request.scheme,
      }
      request_record = self.__request_orm.create(**request_columns)

      response_columns: ResponseColumns = {
        'control': joined_request.response_string.control(),
        'raw': joined_request.response_string.get(),
        'request_id': request_record.id,
      }

      self.__response_orm.create(**response_columns)

      return request_record.to_dict()

  def show(self, request_id: str, **options: RequestShowParams) -> RequestShowResponse:
    request = self.__request_orm.find(request_id)

    return ORMTOStooblyRequestTransformer(request, options).transform()

  def response(self, **query_params: RequestColumns) -> requests.Response:
    request_columns = { **query_params }
    self.__filter_request_response_columns(request_columns)

    # Find most recent matching record
    request = self.__request_orm.where_for(**request_columns).get().last()

    if not request:
      return CustomNotFoundResponseBuilder().build()

    response_record = request.response 

    if not response_record:
      return CustomNotFoundResponseBuilder().build()

    return ORMToRequestsResponseTransformer(response_record).transform()

  def index(self, **query_params: RequestsIndexQueryParams) -> RequestsIndexResponse:
    page = query_params.get('page') or 0
    size = query_params.get('size') or 20

    total = Request.count()
    
    requests = Request.offset(page).limit(size).get()

    return {
      'list': self.__transform_index_list(requests.items),
      'total': total,
    }

  def __filter_request_response_columns(self, request_columns: RequestCreateParams):
    del request_columns['project_id']
    del request_columns['scenario_id']
    del request_columns['headers_hash']

  def __transform_index_list(self, records: List[Request]):
    allowed_keys = list(RequestShowResponse.__annotations__.keys())
    filter_keys = lambda request: dict((key, value) for key, value in request.items() if key in allowed_keys)
    requests = list(map(lambda request: filter_keys(request.to_dict()), records))
    for request in requests:
      request['key'] = RequestKey.encode(None, request['id'])
    return requests
