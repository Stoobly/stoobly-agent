import time

from mitmproxy.http import HTTPFlow as MitmproxyHTTPFlow
from requests import Response

class MockContext():
  def __init__(self, flow: MitmproxyHTTPFlow):
    self.__flow = flow
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
  def response(self):
    return self.__response

  @property
  def start_time(self):
    return self.__start_time

  def with_response(self, response: Response):
    self.__response = response
    self.__end_time = time.time()
    return self