from mitmproxy.http import HTTPFlow as MitmproxyHTTPFlow

from stoobly_agent.app.proxy.intercept_settings import InterceptSettings

from ..context import InterceptContext

class RecordContext(InterceptContext):
  def __init__(self, flow: MitmproxyHTTPFlow, intercept_settings: InterceptSettings):
    super().__init__(flow, intercept_settings)