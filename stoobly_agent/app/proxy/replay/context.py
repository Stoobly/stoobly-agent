import time

from mitmproxy.http import HTTPFlow as MitmproxyHTTPFlow
from requests import Response

from stoobly_agent.app.proxy.intercept_settings import InterceptSettings

class ReplayContext():
  def __init__(self, flow: MitmproxyHTTPFlow, intercept_settings: InterceptSettings):
    self.__flow = flow
    self.__intercept_settings = intercept_settings

    self.__start_time = time.time()
    self.__end_time = None
    self.__response = None

  @property
  def end_time(self):
    return self.__end_time

  @property
  def flow(self):
    return self.__flow

  @property
  def intercept_settings(self):
    return self.__intercept_settings

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