import pdb
import requests

from mitmproxy.http import HTTPFlow as MitmproxyHTTPFlow
from typing import Tuple

from stoobly_agent.app.models.adapters.python import PythonRequestAdapterFactory
from stoobly_agent.app.models.helpers.create_request_params_service import build_params
from stoobly_agent.app.models.types import RequestCreateParams, RequestDestroyParams, RequestDestroyAllParams, RequestIndexSimilarParams, RequestShowParams
from stoobly_agent.app.proxy.mock.custom_not_found_response_builder import CustomNotFoundResponseBuilder
from stoobly_agent.app.proxy.mock.ignored_components_response_builder import IgnoreComponentsResponseBuilder
from stoobly_agent.app.proxy.record.joined_request import JoinedRequest
from stoobly_agent.config.constants import custom_headers
from stoobly_agent.lib.orm import ORM
from stoobly_agent.lib.orm.request import Request
from stoobly_agent.lib.orm.response import Response
from stoobly_agent.lib.orm.scenario import Scenario
from stoobly_agent.lib.orm.transformers.orm_to_stoobly_request_transformer import ORMToStooblyRequestTransformer
from stoobly_agent.lib.orm.types.request_columns import RequestColumns
from stoobly_agent.lib.orm.transformers import ORMToRequestTransformer, ORMToRequestsResponseTransformer
from stoobly_agent.lib.api.interfaces import RequestsIndexQueryParams, RequestsIndexResponse, RequestShowResponse

from .helpers.create_request_columns_service import build_request_columns, build_response_columns
from .helpers.search import search_request
from .helpers.snapshot_service import snapshot_request
from .helpers.tiebreak_scenario_request import access_request, generate_session_id, tiebreak_scenario_request
from .local_db_adapter import LocalDBAdapter
from .orm_request_builder import ORMRequestBuilder
from .response_adapter import LocalDBResponseAdapter

class LocalDBRequestAdapter(LocalDBAdapter):
  __request_orm = None
  __response_orm = None

  def __init__(self, request_orm: Request.__class__ = Request, response_orm: Response.__class__ = Response, scenario_orm: Scenario.__class__ = Scenario):
    self.__request_orm: Request = request_orm
    self.__response_orm: Response = response_orm
    self.__scenario_orm: Scenario = scenario_orm

  def create(self, **params: RequestCreateParams) -> Tuple[RequestShowResponse, int]:
    self.__adapt_scenario_id(params)

    flow: MitmproxyHTTPFlow = params['flow']
    joined_request: JoinedRequest = params['joined_request']
    scenario_id = params.get('scenario_id')
    uuid = params.get('uuid')

    request_columns = build_request_columns(flow, joined_request, is_deleted=False, scenario_id=scenario_id, uuid=uuid)

    with ORM.instance().db.transaction():
      request_record = self.__request_orm.create(**request_columns)

      response_columns = {
        'request_id': request_record.id,
        **build_response_columns(flow, joined_request),
      }

      self.__response_orm.create(**response_columns)

      return self.success({
        'list': [ORMToStooblyRequestTransformer(request_record, {}).transform()],
        'total': 1,
      })

  def show(self, request_id: str, **options: RequestShowParams) -> Tuple[RequestShowResponse, int]:
    request = self.__request(request_id)

    if not request:
      return self.__request_not_found()

    return self.success(ORMToStooblyRequestTransformer(request, options).transform())

  def response(self, **query_params: RequestColumns) -> requests.Response:
    self.__adapt_scenario_id(query_params)

    endpoint_promise = query_params.get('endpoint_promise')
    request = None

    if not query_params.get('request_id'):
      request_columns = { 'is_deleted': False, **query_params }

      self.__filter_request_response_columns(request_columns)

      # Find most recent matching record
      requests = self.__request_orm.where_for(**request_columns).get()

      if 'scenario_id' in query_params:
        # TODO: Would need an additional ID to distinguish different scenario sessions
        session_id = generate_session_id(request_columns) 

        if len(requests) > 1:
          request = tiebreak_scenario_request(session_id, requests)
        else:
          request = requests.last()

        if request:
          access_request(session_id, request.id)
      else:
        request = requests.last()
    else:
      request = self.__request_orm.find(query_params.get('request_id'))
      
      if request and request.is_deleted:
        request = None

    if not request:
      return self.__handle_request_not_found(endpoint_promise) 

    response_record = request.response
    if not response_record:
      return CustomNotFoundResponseBuilder().build()

    headers = {}
    headers[custom_headers.MOCK_REQUEST_ID] = str(request.id)
    headers[custom_headers.MOCK_REQUEST_KEY] = request.key()
    headers[custom_headers.RESPONSE_LATENCY] = str(request.latency)

    return (
      ORMToRequestsResponseTransformer(response_record)
        .with_headers(headers)
        .transform()
    )

  def __handle_request_not_found(self, endpoint_promise):
    if endpoint_promise:
      ignored_components = self.__ignored_components(endpoint_promise)

      if ignored_components:
        return IgnoreComponentsResponseBuilder().build(ignored_components)

    return CustomNotFoundResponseBuilder().build()

  def index(self, **query_params: RequestsIndexQueryParams) -> Tuple[RequestsIndexResponse, int]:
    self.__adapt_scenario_id(query_params)

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
      requests = requests.where('scenario_id', scenario_id)
      sort_order = query_params.get('sort_order') or 'asc'

    if starred:
      requests = requests.where('starred', starred)

    if query:
      requests = search_request(requests, query)

    total = requests.count()
    requests = requests.offset(page * size).limit(size).order_by(sort_by, sort_order).get()

    return self.success({
      'list': list(map(lambda request: ORMToStooblyRequestTransformer(request, {}).transform(), requests)),
      'total': total,
    })

  def update(self, request_id: int,  **params: RequestShowResponse):
    request = self.__request(request_id)

    if not request:
      return self.__request_not_found()

    transformer = ORMToRequestTransformer(request)

    if params.get('request'):
      create_params = build_params(params['request'])
      del params['request']

      if not create_params:
        return self.bad_request('Could not parse request')

      if request.update(
        **build_request_columns(create_params['flow'], create_params['joined_request'], **params),
      ):
        response = request.response
        if response.update(**{
          **build_response_columns(create_params['flow'], create_params['joined_request']),
        }):
          return self.success(ORMToStooblyRequestTransformer(request, {}).transform())
    else:
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

        return self.success(ORMToStooblyRequestTransformer(request, {}).transform())

    return self.internal_error('Could not update request')

  def destroy(self, request_id: int, **params: RequestDestroyParams):
    request = self.__request(request_id)

    if not request:
      return self.__request_not_found()

    if params.get('force') or request.is_deleted:
      request.delete()
    else:
      request.update({'is_deleted': True})

    return self.success(ORMToStooblyRequestTransformer(request, {}).transform())

  def destroy_all(self, **params: RequestDestroyAllParams) -> Tuple[RequestsIndexQueryParams, int]:
    self.__adapt_scenario_id(params)

    ids = params.get('ids')
    scenario_id = params.get('scenario_id')

    if not isinstance(ids, list) and not scenario_id:
      return self.bad_request('Missing ids')

    requests_query_builder = self.__request_orm

    if isinstance(ids, list):
      requests_query_builder = requests_query_builder.where_in('id', ids)

    if scenario_id:
      requests_query_builder = requests_query_builder.where_for(scenario_id=scenario_id)

    requests = requests_query_builder.get()

    res = self.success({
      'list': list(map(lambda request: ORMToStooblyRequestTransformer(request, {}).transform(), requests)),
      'total': requests.count(),
    })

    for request in requests:
      request.delete()

    return res

  def snapshot(self, request_id: str, **params):
    request = self.__request(request_id)

    if not request:
      return self.__request_not_found()

    file_path = snapshot_request(request, **params)
    if not file_path:
      return self.internal_error()

    return self.success(file_path)

  def index_similar(self, params: RequestIndexSimilarParams):
    pattern = f"%{params['pattern']}"
    candidates = None

    if params['host'] == '%':
      candidates = self.__request_orm.where('host', 'like', params['host'])
    else:
      candidates = self.__request_orm.where('host', params['host'])

    if params['port'] == '%':
      candidates = candidates.where('port', 'like', params['port'])
    else:
      candidates = candidates.where('port', params['port'])

    candidates = candidates.where('method', params['method'])
    candidates = candidates.where('path', 'like', pattern)
    if params.get('scenario_id'):
      candidates = candidates.where('scenario_id', params['scenario_id'])

    return candidates.get()

  def __filter_request_response_columns(self, request_columns: RequestCreateParams):
    if request_columns.get('endpoint_promise'):
      del request_columns['endpoint_promise']

    if request_columns.get('infer'):
      del request_columns['infer']

    if request_columns.get('project_id'):
      del request_columns['project_id']

    if request_columns.get('retry'):
      del request_columns['retry']

  def __request(self, request_id: str):
    if self.validate_uuid(request_id):
      return self.__request_orm.find_by(uuid=request_id)
    else:
      return self.__request_orm.find(request_id)

  def __request_not_found(self):
    return self.not_found('Request not found')

  def __adapt_scenario_id(self, params: dict):
    if not params.get('scenario_id'):
      return

    scenario_id = params['scenario_id']
    if not self.validate_uuid(scenario_id):
      return

    scenario = self.__scenario_orm.find_by(uuid=scenario_id)
    if scenario:
      params['scenario_id'] = scenario.id

  def __ignored_components(self, endpoint_promise):
    endpoint = endpoint_promise()

    if endpoint:
      ignored_components = endpoint.get('ignored_components')

      if ignored_components:
        return ignored_components
    return []