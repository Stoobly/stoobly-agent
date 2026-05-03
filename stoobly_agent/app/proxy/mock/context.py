import time

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from requests import Response
    from mitmproxy.http import HTTPFlow as MitmproxyHTTPFlow

from stoobly_agent.app.proxy.intercept_settings import InterceptSettings
from stoobly_agent.app.proxy.utils.response_handler import apply_response

from ..context import InterceptContext

class MockContext(InterceptContext):
  def __init__(self, flow: 'MitmproxyHTTPFlow', intercept_settings: InterceptSettings):
    super().__init__(flow, intercept_settings)

    self.__start_time = time.time()
    self.__end_time = None

  @property
  def end_time(self):
    return self.__end_time

  @property
  def modified(self):
    return not not self.end_time

  @property
  def start_time(self):
    return self.__start_time

  def with_response(self, response: 'Response'):
    apply_response(self.flow, response)
    self.__end_time = time.time()
    return self