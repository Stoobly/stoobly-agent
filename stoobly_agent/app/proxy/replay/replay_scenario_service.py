import pdb

from stoobly_agent.app.models.request_model import RequestModel
from stoobly_agent.app.models.schemas.request import Request
from stoobly_agent.app.settings import Settings
from stoobly_agent.lib.api.endpoints_resource import EndpointsResource
from stoobly_agent.lib.api.interfaces import RequestShowResponse, RequestsIndexQueryParams
from stoobly_agent.lib.api.keys.scenario_key import ScenarioKey

from ...cli.helpers.context import ReplayContext
from .replay_request_service import replay_with_trace, ReplayRequestOptions
from .trace_context import TraceContext

PAGE_SIZE = '25'

def inject_replay():
  settings = Settings.instance()
  request_model = RequestModel(settings)
  endpoints_resource = EndpointsResource(settings.remote.api_url, settings.remote.api_key)

  return lambda scenario_key, options: replay(scenario_key, request_model, endpoints_resource, options)

def replay(
  scenario_key: str, request_model: RequestModel, endpoints_resource: EndpointsResource, options: ReplayRequestOptions
):
  scenario_key = ScenarioKey(scenario_key)
  trace_context = options.get('trace_context') or TraceContext(endpoints_resource)

  page = 0
  count = 0

  while True:
    requests_index = __get_requests(
      request_model, scenario_key, { 'page': page, 'size': PAGE_SIZE, 'sort_order': 'asc' }
    )

    if not requests_index:
      return

    requests = list(map(lambda request: Request(request), requests_index['list']))
    total = requests_index['total']
  
    if not requests or len(requests) == 0:
      return

    for request_partial in requests:
      count += 1

      request_id = request_partial.id
      request_response = __get_request(request_model, scenario_key, request_id)
      if not request_response:
        continue
      
      context = ReplayContext(Request(request_response)).with_sequence(count)
      replay_with_trace(context, trace_context, options)

    if count >= total:
      return

    page += 1

def __get_requests(
  request_model: RequestModel, scenario_key: ScenarioKey, query_params: RequestsIndexQueryParams = {}
):
  project_id = scenario_key.project_id
  scenario_id = scenario_key.id

  return request_model.index(**{
    'project_id': project_id,
    'scenario_id': scenario_id,
    'page': query_params.get('page'),
    'size': query_params.get('size'),
    'sort_order': query_params.get('sort_order'),
  })

def __get_request(
  request_model: RequestModel, scenario_key: ScenarioKey, request_id: int
) -> RequestShowResponse:
  project_id = scenario_key.project_id

  return request_model.show(
    request_id,
    **{
      'body': True,
      'headers': True,
      'project_id': project_id,
      'query_params': True,
      'response': True
    }
  )