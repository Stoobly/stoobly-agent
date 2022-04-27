import pdb

from stoobly_agent.lib.api.interfaces import RequestShowResponse, RequestsIndexQueryParams
from stoobly_agent.lib.api.keys.scenario_key import InvalidScenarioKey, ScenarioKey
from stoobly_agent.app.models.request_model import RequestModel
from stoobly_agent.app.models.schemas.request import Request

from .replay_request_service import replay as replay_request, ReplayRequestOptions

def replay(scenario_key: str, request_model: RequestModel, options: ReplayRequestOptions):
  scenario_key = ScenarioKey(scenario_key)

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
      request = Request(__get_request(request_model, scenario_key, request_id))

      response = replay_request(request, **options) 

      l.append(response)

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

def __get_request(request_model: RequestModel, scenario_key: ScenarioKey, request_id: int) -> RequestShowResponse:
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