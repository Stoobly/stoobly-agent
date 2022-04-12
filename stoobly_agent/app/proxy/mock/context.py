import time

from mitmproxy.http import HTTPFlow as MitmproxyHTTPFlow
from requests import Response
from typing import Union

from stoobly_agent.app.models.request_model import RequestModel
from stoobly_agent.app.proxy.intercept_settings import InterceptSettings

class MockContext():
  def __init__(self, flow: MitmproxyHTTPFlow, intercept_settings: InterceptSettings):
    self.__flow = flow
    self.__intercept_settings = intercept_settings
    self.start_time = time.time()

    self.model = None
    self.response = None

  @property
  def flow(self):
    return self.__flow

  @property
  def intercept_settings(self):
    return self.__intercept_settings

  def with_response(self, response: Response):
    self.response = response
    return self

  def with_model(self, model: RequestModel):
    self.model = model
    return self