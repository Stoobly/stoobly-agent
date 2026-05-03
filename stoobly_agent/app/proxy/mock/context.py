from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mitmproxy.http import HTTPFlow as MitmproxyHTTPFlow

from stoobly_agent.app.proxy.intercept_settings import InterceptSettings

from ..context import InterceptContext

class MockContext(InterceptContext):
  def __init__(self, flow: 'MitmproxyHTTPFlow', intercept_settings: InterceptSettings):
    super().__init__(flow, intercept_settings)

  @property
  def end_time(self):
    response = self.flow.response
    if not response:
      return None
    return response.timestamp_end

  @property
  def start_time(self):
    request = self.flow.request
    return request.timestamp_start
