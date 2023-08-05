from mitmproxy.http import HTTPFlow as MitmproxyHTTPFlow

from stoobly_agent.app.proxy.intercept_settings import InterceptSettings

class InterceptContext():

  def __init__(self, flow: MitmproxyHTTPFlow, intercept_settings: InterceptSettings):
    self.__flow = flow
    self.__intercept_settings = intercept_settings

  @property
  def flow(self):
    return self.__flow

  @property
  def intercept_settings(self):
    return self.__intercept_settings

