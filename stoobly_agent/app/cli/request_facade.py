import pdb
from stoobly_agent.config.constants import test_origin, test_strategy

from stoobly_agent.app.models.request_model import RequestModel
from stoobly_agent.app.models.schemas.request import Request
from stoobly_agent.app.proxy.replay.replay_request_service import replay
from stoobly_agent.app.settings import Settings
from stoobly_agent.lib.api.keys.project_key import ProjectKey
from stoobly_agent.lib.api.keys.request_key import RequestKey
from stoobly_agent.config.constants import mode

class RequestFacade():

  def __init__(self, settings: Settings):
    self.model = RequestModel(settings)

  def show(self, request_key: str, **kwargs):
    key = RequestKey(request_key)
    return self.model.show(key.id, **{ 
      'project_id': key.project_id, 
      **kwargs 
    })

  def index(self, project_key, **kwargs):
    key = ProjectKey(project_key)
    return self.model.index(**{ 'project_id': key.id, **kwargs})

  def replay(self, request_key: str, **kwargs):
    kwargs['mode'] = mode.NONE
    return self.__replay(request_key, **kwargs)

  def record(self, request_key: str, **kwargs):
    kwargs['mode'] = mode.RECORD
    return self.__replay(request_key, **kwargs)

  def mock(self, request_key: str, **kwargs):
    kwargs['mode'] = mode.MOCK
    return self.__replay(request_key, **kwargs)

  def test(self, request_key: str, **kwargs):
    kwargs['mode'] = mode.TEST
    kwargs['strategy'] = kwargs.get('strategy') or test_strategy.DIFF
    kwargs['test_origin'] = test_origin.CLI
    
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
    return replay(Request(request), **kwargs)