import requests

from mitmproxy.http import Request as MitmproxyRequest

class PythonRequestAdapter():
  
  def __init__(self, request: MitmproxyRequest):
    self.__request = request

  def adapt(self):
    return requests.Request(
      method=self.__request.method,
      url=self.__request.url,
      headers=self.__request.headers,
      data=self.__request.content
    )
