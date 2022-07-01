import requests
import time

from stoobly_agent.app.models.schemas.request import Request

class ReplayContext():

  def __init__(self, request: Request):
    self.__end_time = None
    self.__start_time = time.time()

    self.__request: Request = request
    self.__response: requests.Response = None

    self.__sequence = None

  @property
  def end_time(self):
    return self.__end_time

  @property
  def request(self):
    return self.__request

  @property
  def response(self):
    return self.__response

  @property
  def sequence(self):
    return self.__sequence

  @property
  def start_time(self):
    return self.__start_time

  def clone(self):
    return ReplayContext(self.__request.clone())

  def with_response(self, response: requests.Response):
    self.__end_time = time.time()
    self.__response = response
    return self

  def with_sequence(self, sequence):
    self.__sequence = sequence
    return self

