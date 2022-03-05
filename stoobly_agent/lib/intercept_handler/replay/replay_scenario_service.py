from typing import Union

from stoobly_agent.lib.api.interfaces.requests_index_query_params import RequestsIndexQueryParams
from stoobly_agent.lib.api.interfaces.requests_index_response import RequestsIndexResponse
from stoobly_agent.lib.api.schemas.request import Request
from stoobly_agent.lib.api.requests_resource import RequestsResource

from .replay_request_service import replay as replay_request, ReplayRequestOptions

def replay(api: RequestsResource, **kwargs):
  options: ReplayRequestOptions = kwargs # For annotation purposes

  scenario_key = options['scenario_key']

  page = 0
  count = 0
  l = []

  while True:
    requests_response = __get_requests(
      api, scenario_key, { 
        'page': page, 'size': '25'
      }
    )

    if not requests_response:
      return l

    total = requests_response['total']
    requests = requests_response['list']
    
    if len(requests) == 0:
      return l

    for request_partial in requests:
      request_id = request_partial['id']
      request = __get_request(api, scenario_key, request_id)

      response = replay_request(Request(request), **kwargs) 

      l.append(response)

    count += len(requests)

    if count >= total:
      return l

    page += 1

def __get_requests(
   api: RequestsResource, scenario_key: str, query_params: RequestsIndexQueryParams = {}
) -> Union[None, RequestsIndexResponse]:
  scenario_data = RequestsResource.decode_scenario_key(scenario_key)

  project_id = scenario_data['project_id']
  scenario_id = scenario_data['id']

  res = api.index(project_id, {
    'scenario_id': scenario_id,
    'page': query_params.get('page'),
    'size': query_params.get('size'),
  })

  if not res.ok:
    raise AssertionError(f"Could not get requests for scenario {scenario_key}")

  return res.json()

def __get_request(api: RequestsResource, scenario_key: str, request_id: int):
  scenario_data = RequestsResource.decode_scenario_key(scenario_key)

  project_id = scenario_data['project_id']

  res = api.show(
    project_id, request_id, {
      'body': True,
      'headers': True,
      'query_params': True,
      'response': True
    }
  )

  if not res.ok:
    raise AssertionError(f"Could not get details for request {request_id}")

  return res.json()