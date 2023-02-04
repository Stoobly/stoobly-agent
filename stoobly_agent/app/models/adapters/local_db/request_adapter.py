import pdb
from urllib.parse import urlparse
import requests

from mitmproxy.http import HTTPFlow as MitmproxyHTTPFlow, Request as MitmproxyRequest
from typing import List

from stoobly_agent.app.proxy.mock.custom_not_found_response_builder import CustomNotFoundResponseBuilder
from stoobly_agent.app.proxy.mock.hashed_request_decorator import HashedRequestDecorator
from stoobly_agent.app.proxy.mitmproxy.request_facade import MitmproxyRequestFacade
from stoobly_agent.app.proxy.upload.joined_request import JoinedRequest

from stoobly_agent.lib.orm import ORM
from stoobly_agent.lib.orm.request import Request
from stoobly_agent.lib.orm.response import Response
from stoobly_agent.lib.orm.transformers.orm_to_stoobly_request_transformer import ORMToStooblyRequestTransformer
from stoobly_agent.lib.orm.types.request_columns import RequestColumns
from stoobly_agent.lib.orm.types.response_columns import ResponseColumns
from stoobly_agent.lib.orm.transformers import ORMToRequestsResponseTransformer, ORMToStooblyResponseTransformer
from stoobly_agent.lib.api.interfaces import RequestsIndexQueryParams, RequestsIndexResponse, RequestShowResponse

from ..types import RequestCreateParams, RequestShowParams

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
    request_facade = MitmproxyRequestFacade(request)
    hashed_request = HashedRequestDecorator(request_facade)

    with ORM.instance().db.transaction():
      request_columns: RequestColumns = {
        'body_params_hash': hashed_request.body_params_hash(),
        'body_text_hash': hashed_request.body_text_hash(),
        'control': joined_request.request_string.control, 
        'headers_hash': hashed_request.headers_hash(),
        'host': request.host,
        'latency': joined_request.response_string.latency,
        'method': request.method,
        'path': request_facade.path,
        'port': request.port,
        'query': request_facade.query_string,
        'query_params_hash': hashed_request.query_params_hash(),
        'raw': joined_request.request_string.get(),
        'scenario_id': int(params['scenario_id']) if params.get('scenario_id') else None,
        'scheme': request.scheme,
        'status': flow.response.status_code,
      }
      request_record = self.__request_orm.create(**request_columns)

      response_columns: ResponseColumns = {
        'control': joined_request.response_string.control,
        'raw': joined_request.response_string.get(),
        'request_id': request_record.id,
      }

      self.__response_orm.create(**response_columns)

      return {
        'list': [ORMToStooblyRequestTransformer(request_record, {}).transform()],
        'total': 1,
      }

  def show(self, request_id: str, **options: RequestShowParams) -> RequestShowResponse:
    request = self.__request_orm.find(request_id)

    return ORMToStooblyRequestTransformer(request, options).transform()

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
    scenario_id = query_params.get('scenario_id')
    page = int(query_params.get('page') or 0)
    query = query_params.get('q')
    size = int(query_params.get('size') or 20)
    sort_by = query_params.get('sort_by') or 'id'
    sort_order = query_params.get('sort_order') or 'desc'

    is_deleted = query_params.get('filter') == 'is_deleted'
    starred = query_params.get('filter') == 'starred'

    requests = Request.where('is_deleted', is_deleted)

    if scenario_id: 
      requests = requests.where('scenario_id', int(scenario_id))

    if starred:
      requests = requests.where('starred', starred)

    if query:
      requests = self.__search(requests, query)

    total = requests.count()
    requests = requests.offset(page * size).limit(size).order_by(sort_by, sort_order).get()

    return {
      'list': list(map(lambda request: ORMToStooblyRequestTransformer(request, {}).transform(), requests)),
      'total': total,
    }

  def update(self, request_id: int,  **params: RequestShowResponse):
    request = Request.find(request_id)

    if not request:
      return

    if request.update(params):
      return ORMToStooblyRequestTransformer(request, {}).transform()

  def destroy(self, request_id: int):
    request = Request.find(request_id)

    if not request:
      return

    if request.is_deleted:
      request.delete()
    else:
      request.update({'is_deleted': True})

    return ORMToStooblyRequestTransformer(request, {}).transform()

  def __filter_request_response_columns(self, request_columns: RequestCreateParams):
    if request_columns.get('project_id'):
      del request_columns['project_id']

  def __search(self, base_model: Request, query: str) -> Request:
    uri = urlparse(query)

    if uri.hostname:
      return base_model.where('host', uri.hostname).where('path', uri.path)
    else:
      return base_model.where('path', 'like', f"%{query}%")