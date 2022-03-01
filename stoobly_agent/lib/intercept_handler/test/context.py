import time

from .context_response import TestContextResponse

class TestContext():
  def __init__(self, strategy):
    self.strategy = strategy
    self.start_time = time.time()

    self.expected_response = None
    self.expected_mitmproxy_response = None
    self.response = None

  def with_expected_response(self, response: TestContextResponse):
    self.expected_response = response
    return self

  def with_response(self, response: TestContextResponse):
    self.response = response
    return self