import pdb
import requests

from typing import Union

from stoobly_agent.app.cli.helpers.context import ReplayContext
from stoobly_agent.app.cli.helpers.test_facade import TestFacade
from stoobly_agent.app.proxy.replay.body_parser_service import decode_response
from stoobly_agent.app.proxy.test.helpers.test_results_builder import TestResultsBuilder
from stoobly_agent.app.proxy.test.helpers.diff_service import diff
from stoobly_agent.app.settings import Settings
from stoobly_agent.config.constants import custom_headers
from stoobly_agent.lib.api.interfaces.tests import TestShowResponse
from stoobly_agent.lib.api.keys.project_key import InvalidProjectKey, ProjectKey
from stoobly_agent.lib.utils.decode import decode

class TestReplayContext(ReplayContext):

  def __init__(self, replay_context: ReplayContext):
    super().__init__(replay_context.request)

    self.with_response(replay_context.response)
    self.end_time = replay_context.end_time
    self.start_time = replay_context.start_time

    self.__project_id = -1
    self.__test_results_builder = TestResultsBuilder()

    if self.has_test_results:
      self.__test_results_builder.deserialize(replay_context.response.content)

  @property
  def has_test_results(self):
    headers = self.response.headers
    return headers.get(custom_headers.CONTENT_TYPE) == custom_headers.CONTENT_TYPE_TEST_RESULTS

  @property
  def project_id(self):
    return self.__project_id

  @project_id.setter
  def project_id(self, v):
    self.__project_id = v

  @property
  def response_content(self):
    if self.has_test_results:
      return self.__test_results_builder.received_response
    else:
      content = self.response.content
      content_type = self.response.headers.get('content-type')

      return decode_response(content, content_type)

  @property
  def response_status_code(self):
    if self.has_test_results:
      return self.__test_results_builder.status
    else:
      return self.response.status_code

  @property
  def test_results_builder(self):
    return self.__test_results_builder

  def diff_response(self, response: TestShowResponse, test_facade: TestFacade):
    if response['passed'] or response['skipped']:
      return (self.response_content, self.response_status_code, self.latency)

    expected_response_content, expected_status_code = self.expected_response_content(test_facade)

    if not self.has_test_results:
      return (
        diff(expected_response_content, self.response_content),
        diff(expected_status_code, self.response_status_code),
        diff(response['expected_latency'], self.latency)
      )
    else:
      builder = self.test_results_builder
      return (
        diff(expected_response_content, builder.received_response),
        diff(expected_status_code, self.response_status_code),
        diff(response['expected_latency'], self.latency)
      )

  def expected_response_content(self, test_facade: TestFacade):
    if not self.has_test_results: 
      response = self.__get_test_expected_response_with_context(test_facade)

      if isinstance(response, requests.Response):
        content = decode(response.content)
        content_type = response.headers.get('content-type')

        return decode_response(content, content_type), response.status_code
      else:
        return '', 0
    else:
      builder = self.test_results_builder
      return builder.expected_response, builder.expected_status_code

  def test_show_response(self, test_facade = None) -> TestShowResponse:
    if not self.has_test_results: 
      return self.__get_test_response_with_context(test_facade)
    else:
      builder = self.test_results_builder

      # The following is inferred from settings (assumes nothing has changed)
      settings = Settings.instance()
      project_id = -1

      try:
        project_key = ProjectKey(settings.proxy.intercept.project_key) 
        project_id = project_key.id
      except InvalidProjectKey:
        pass

      return {
        'expected_latency': builder.expected_latency,
        'id': None,
        'log': builder.log,
        'passed': builder.passed,
        'project_id': project_id,
        'skipped': builder.skipped,
        'strategy': builder.strategy,
      }
    
  def __get_test_response_with_context(self, test_facade: TestFacade) -> Union[TestShowResponse, str]:
    try:
      res = test_facade.show_with_context(super(), self.project_id)
      return res
    except AssertionError as e:
      return f"API Error: {e}"

  def __get_test_expected_response_with_context(self, test_facade: TestFacade):
    try:
      res = test_facade.expected_response_with_context(super(), self.project_id)
      return res
    except AssertionError as e:
      return f"API Error: {e}"