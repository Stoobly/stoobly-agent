import pdb
from runpy import run_path
from pprint import pprint
from stoobly_agent.app.cli.helpers.scenario_facade import ScenarioFacade

from stoobly_agent.app.models.factories.resource.request import RequestResourceFactory
from stoobly_agent.app.models.types import OPENAPI_FORMAT
from stoobly_agent.app.models.types.request import RequestFindParams
from stoobly_agent.app.settings import Settings

from ..types.endpoint import EndpointCreateCliOptions
from .openapi_endpoint_adapter import OpenApiEndpointAdapter
from .synchronize_request_service import SynchronizeRequestService

class EndpointFacade():
  def __init__(self, __settings: Settings):
    self.__settings = __settings
    self.local_db_request_adapter = RequestResourceFactory(self.__settings.remote).local_db()
    self.synchronize_request_service = SynchronizeRequestService(local_db_request_adapter=self.local_db_request_adapter)
  
  def create(self, **kwargs: EndpointCreateCliOptions):
    if kwargs.get('format') == OPENAPI_FORMAT:
      lifecycle_hooks = {}

      try:
        lifecycle_hooks = run_path(kwargs['lifecycle_hooks_script_path'])
      except Exception as e:
        pass

      self.__create_from_openapi(kwargs.get('path'), kwargs.get('scenario_key'), lifecycle_hooks)

  def __create_from_openapi(self, file_path: str, scenario_key: str, lifecycle_hooks = {}):
    endpoint_adapter = OpenApiEndpointAdapter()
    endpoints = endpoint_adapter.adapt_from_file(file_path)

    scenario_id = 0
    if scenario_key:
      scenario = ScenarioFacade(self.__settings)
      scenario_response, status = scenario.show(scenario_key)
      if status == 200 and scenario_response:
        scenario_id = scenario_response['id']

    for endpoint in endpoints:
      host = endpoint['host']
      if host == '':
        host = '%'

      port = endpoint['port']
      method = endpoint['method']
      pattern = endpoint['match_pattern']

      params = RequestFindParams(host=host, port=port, method=method, pattern=pattern, scenario_id=scenario_id)
      similar_requests = self.local_db_request_adapter.find_similar_requests(params)

      for request in similar_requests:
        self.synchronize_request_service.synchronize_request(request, endpoint, lifecycle_hooks)

