import pdb

from stoobly_agent.app.models.request_model import RequestModel
from stoobly_agent.app.models.schemas.request import Request
from stoobly_agent.lib.api.endpoints_resource import EndpointsResource
from stoobly_agent.lib.api.interfaces import RequestShowResponse, RequestsIndexQueryParams
from stoobly_agent.lib.api.keys.scenario_key import ScenarioKey

from .replay_request_service import replay as replay_request, ReplayRequestOptions
from .trace_context import TraceContext

def replay(scenario_key: str, request_model: RequestModel, options: ReplayRequestOptions):
  scenario_key = ScenarioKey(scenario_key)
  settings = request_model.settings
  endpoints_resource = EndpointsResource(settings.remote.api_url, settings.remote.api_key)
  context = TraceContext(endpoints_resource)

  page = 0
  count = 0
  l = []

  while True:
    requests_index = __get_requests(
      request_model, scenario_key, { 'page': page, 'size': '25' }
    )

    requests = list(map(lambda request: Request(request), requests_index['list']))
    total = requests_index['total']
  
    if not requests or len(requests) == 0:
      return l

    for request_partial in requests:
      request_id = request_partial.id
      response = __get_request(request_model, scenario_key, request_id)
      if not response:
        continue

      request = Request(response)
      context.with_request(request, lambda: replay_request(request, **options))

      l.append(response)

    # Next page of requests...
    count += len(requests)

    if count >= total:
      return l

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