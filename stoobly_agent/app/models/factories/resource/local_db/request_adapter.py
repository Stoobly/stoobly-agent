import pdb
import requests

from mitmproxy.http import HTTPFlow as MitmproxyHTTPFlow, Request as MitmproxyRequest
from urllib.parse import urlparse

from stoobly_agent.app.models.adapters.python import PythonRequestAdapterFactory
from stoobly_agent.app.models.types import RequestCreateParams, RequestShowParams
from stoobly_agent.app.proxy.mock.custom_not_found_response_builder import CustomNotFoundResponseBuilder
from stoobly_agent.app.proxy.upload.joined_request import JoinedRequest
from stoobly_agent.lib.orm import ORM
from stoobly_agent.lib.orm.request import Request
from stoobly_agent.lib.orm.response import Response
from stoobly_agent.lib.orm.transformers.orm_to_stoobly_request_transformer import ORMToStooblyRequestTransformer
from stoobly_agent.lib.orm.types.request_columns import RequestColumns
from stoobly_agent.lib.orm.types.response_columns import ResponseColumns
from stoobly_agent.lib.orm.transformers import ORMToRequestTransformer, ORMToRequestsResponseTransformer
from stoobly_agent.lib.api.interfaces import RequestsIndexQueryParams, RequestsIndexResponse, RequestShowResponse

from .orm_request_builder import ORMRequestBuilder
from .response_adapter import LocalDBResponseAdapter

class LocalDBRequestAdapter():
  __request_orm = None
  __response_orm = None

  def __init__(self, request_orm: Request.__class__ = Request, response_orm: Response.__class__ = Response):
    self.__request_orm = request_orm
    self.__response_orm = response_orm

  def create(self, **params: RequestCreateParams) -> RequestShowResponse:
    flow: MitmproxyHTTPFlow = params['flow']
    joined_request: JoinedRequest = params['joined_request']

    with ORM.instance().db.transaction():
      builder = ORMRequestBuilder()
      request_columns = builder.columns_from_mitmproxy_request(flow.request)
      response_columns = builder.columns_from_mitmproxy_response(flow.response)

      request_columns: RequestColumns = {
        **request_columns,
        **response_columns,
        'control': joined_request.request_string.control, 
        'latency': joined_request.response_string.latency,
        'raw': joined_request.request_string.get(),
        'scenario_id': int(params['scenario_id']) if params.get('scenario_id') else None,
        'status': flow.response.status_code,
      }
      request_record = self.__request_orm.create(**request_columns)

      response_columns: ResponseColumns = {
        'control': joined_request.response_string.control,
        'http_version': self.__http_version(flow.response.http_version),
        'raw': joined_request.response_string.get(),
        'request_id': request_record.id,
      }

      response_record = self.__response_orm.create(**response_columns)

      return {
        'list': [ORMToStooblyRequestTransformer(request_record, {}).transform()],
        'total': 1,
      }

  def show(self, request_id: str, **options: RequestShowParams) -> RequestShowResponse:
    request = self.__request_orm.find(request_id)

    if not request:
      return CustomNotFoundResponseBuilder().build()

    return ORMToStooblyRequestTransformer(request, options).transform()

  def response(self, **query_params: RequestColumns) -> requests.Response:
    request = None

    if not query_params.get('request_id'):
      request_columns = { **query_params }

      self.__filter_request_response_columns(request_columns)

      # Find most recent matching record
      request = self.__request_orm.where_for(**request_columns).get().last()
    else:
      request = self.__request_orm.find(query_params.get('request_id'))

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
    unassigned = query_params.get('filter') == 'unassigned'

    requests = Request.where('is_deleted', is_deleted)

    if unassigned:
      requests = requests.where('scenario_id', None)
    elif scenario_id: 
      requests = requests.where('scenario_id', int(scenario_id))
      sort_order = query_params.get('sort_order') or 'asc' 

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

    transformer = ORMToRequestTransformer(request)

    if params.get('method'):
      transformer.with_method(params['method'])

    if params.get('url'):
      transformer.with_url(params['url'])
      del params['url']

    if params.get('headers'):
      transformer.with_headers(params['headers'])
      del params['headers']

    if params.get('body'):
      transformer.with_body(params['body'])
      del params['body']

    if transformer.dirty:
      python_request = transformer.transform()
      adapter_factory = PythonRequestAdapterFactory(python_request) 

      builder = ORMRequestBuilder()
      columns = builder.columns_from_mitmproxy_request(adapter_factory.mitmproxy_request())
      params = {
        'raw': adapter_factory.raw_request(),
        **params,
        **columns,
      }

    # Some params need to be reflected in response record
    response_params = {}

    if params.get('latency'):
      latency = int(params['latency'])
      latency = latency = 0 if latency < 0 else latency
      params['latency'] = latency
      response_params['latency'] = latency

    if params.get('status'):
      response_params['status'] = params['status']

    if request.update(params):

      if len(response_params.keys()) != 0:
        response = request.response
        LocalDBResponseAdapter(self.__request_orm).update(response.id, **response_params)

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
      pattern = f"%{query}%"
      return base_model.where('path', 'like', pattern).or_where('host', 'like', pattern)

  def __http_version(self, http_version: str):
    if not isinstance(http_version, str):
      return http_version
    _version = http_version.split('/')[1]
    return float(_version)