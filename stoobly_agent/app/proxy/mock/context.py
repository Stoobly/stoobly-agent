import time

from mitmproxy.http import HTTPFlow as MitmproxyHTTPFlow
from requests import Response

from stoobly_agent.app.proxy.intercept_settings import InterceptSettings

from ..context import InterceptContext

class MockContext(InterceptContext):
  def __init__(self, flow: MitmproxyHTTPFlow, intercept_settings: InterceptSettings):
    super().__init__(flow, intercept_settings)

    self.__start_time = time.time()
    self.__end_time = None
    self.__response = None

  @property
  def end_time(self):
    return self.__end_time

  @property
  def response(self):
    return self.__response

  @property
  def start_time(self):
    return self.__start_time

  def with_response(self, response: Response):
    self.__response = response
    self.__end_time = time.time()
    return self