import pdb
import requests
import time

from stoobly_agent.app.models.adapters.python import PythonRequestAdapterFactory
from stoobly_agent.app.models.schemas.request import Request

class ReplayContext():

  def __init__(self, request: Request):
    self.__end_time = None
    self.__start_time = time.time()

    self.__request: Request = request
    self.__response: requests.Response = None

    self.__sequence = None

  @classmethod
  def from_python_request(cls, request: requests.Request):
    stoobly_request = PythonRequestAdapterFactory(request).stoobly_request()
    return cls(Request(stoobly_request))

  @property
  def end_time(self):
    return self.__end_time

  @end_time.setter
  def end_time(self, v):
    self.__end_time = v 

  # ms
  @property
  def latency(self):
    seconds = self.end_time - self.start_time
    return round(seconds * 1000)

  @property
  def key(self):
    return self.__request.key

  @property
  def request(self):
    return self.__request

  @property
  def response(self):
    return self.__response

  @property
  def response_content(self):
    return self.__response.content

  @property
  def sequence(self):
    return self.__sequence

  @property
  def start_time(self):
    return self.__start_time

  @start_time.setter
  def start_time(self, v):
    self.__start_time = v

  def clone(self):
    return ReplayContext(self.__request.clone())

  def with_response(self, response: requests.Response):
    self.__end_time = time.time()
    self.__response = response
    return self

  def with_sequence(self, sequence):
    self.__sequence = sequence
    return self

