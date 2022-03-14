import pdb

from stoobly_agent.lib.api.keys.project_key import ProjectKey
from stoobly_agent.lib.api.keys.request_key import RequestKey
from stoobly_agent.lib.models.request_model import RequestModel
from stoobly_agent.app.proxy.constants import modes, test_strategies
from stoobly_agent.app.proxy.replay.replay_request_service import replay
from stoobly_agent.lib.settings import Settings

class RequestFacade():

  def __init__(self, settings: Settings):
    self.model = RequestModel(settings)

  def show(self, request_key: str, **kwargs):
    key = RequestKey(request_key)
    return self.model.show(key.project_id, key.request_id, kwargs)

  def index(self, project_key, **kwargs):
    key = ProjectKey(project_key)
    return self.model.index(key.id, kwargs)

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
    request = self.show(request_key, **{
      'body': True,
      'headers': True,
      'query_params': True,
      'response': True,
      **kwargs
    })
    return replay(request, **kwargs)


