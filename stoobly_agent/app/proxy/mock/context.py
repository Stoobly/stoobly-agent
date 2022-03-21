import time

from mitmproxy.http import HTTPFlow as MitmproxyHTTPFlow
from requests import Response
from typing import Union

from stoobly_agent.app.models.request_model import RequestModel
from stoobly_agent.app.settings.types import IProjectMockSettings, IProjectTestSettings 

class MockContext():
  def __init__(self, flow: MitmproxyHTTPFlow, active_mode_settings: Union[IProjectMockSettings , IProjectTestSettings]):
    self.active_mode_settings = active_mode_settings
    self.flow = flow
    self.start_time = time.time()

    self.model = None
    self.response = None

  def with_response(self, response: Response):
    self.response = response
    return self

  def with_model(self, model: RequestModel):
    self.model = model
    return self