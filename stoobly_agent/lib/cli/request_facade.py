import pdb

from stoobly_agent.lib.api.interfaces.request_show_response import RequestShowResponse
from stoobly_agent.lib.api.requests_resource import RequestsResource
from stoobly_agent.lib.api.schemas.request import Request
from stoobly_agent.lib.api.keys.request_key import RequestKey
from stoobly_agent.lib.intercept_handler.constants import modes, test_strategies
from stoobly_agent.lib.intercept_handler.replay.replay_request_service import replay
from stoobly_agent.lib.settings import Settings

class RequestFacade():

  def __init__(self, settings: Settings):
    self.api = RequestsResource(settings.api_url, settings.api_key)
    self.settings = settings

  def show(self, request_key: str, **kwargs) -> RequestShowResponse:
    key = RequestKey(request_key)
    res = self.api.show(key.project_id, key.request_id, kwargs)

    return res.json()

  def index(self, project_key, **kwargs):
    res = self.api.from_project_key(
      project_key, lambda project_id: self.api.index(project_id, kwargs)
    ) 
    return res.json()

  def replay(self, request_key: str, **kwargs):
    kwargs['mode'] = modes.NONE
    return self.__replay(request_key, **kwargs)

  def record(self, request_key: str, **kwargs):
    kwargs['mode'] = modes.RECORD
    return self.__replay(request_key, **kwargs)

  def mock(self, request_key: str, **kwargs):
    kwargs['mode'] = modes.MOCK
    return self.__replay(request_key, **kwargs)

  def test(self, request_key: str, **kwargs):
    kwargs['mode'] = modes.TEST
    kwargs['strategy'] = kwargs.get('strategy') or test_strategies.DIFF
    
    if kwargs.get('save_to_report'):
      kwargs['report_key'] = kwargs.get('save_to_report')

    return self.__replay(request_key, **kwargs)

  def __replay(self, request_key: str, **kwargs):
    request_response = self.show(request_key, **{
      'body': True,
      'headers': True,
      'query_params': True,
      'response': True,
      **kwargs
    })
    return replay(Request(request_response), **kwargs)


