import time

from .context_response import TestContextResponse

class TestContext():
  def __init__(self, request, strategy):
    self.__request = request
    self.strategy = strategy
    self.start_time = time.time()

    self.expected_response = None
    self.response = None

  @property
  def request(self):
    return self.__request

  def with_expected_response(self, response: TestContextResponse):
    self.expected_response = response
    return self

  def with_response(self, response: TestContextResponse):
    self.response = response
    return self