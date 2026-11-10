import pdb

from typing import Union

from stoobly_agent.app.cli.helpers.context import ReplayContext
from stoobly_agent.app.cli.helpers.test_facade import TestFacade
from stoobly_agent.app.proxy.replay.body_parser_service import decode_response
from stoobly_agent.app.proxy.test.helpers.expected_response_codec import decode_expected_response
from stoobly_agent.app.proxy.test.helpers.diff_service import diff
from stoobly_agent.app.settings import Settings
from stoobly_agent.config.constants import custom_headers
from stoobly_agent.lib.api.interfaces.tests import TestShowResponse
from stoobly_agent.lib.api.keys.project_key import InvalidProjectKey, ProjectKey
from stoobly_agent.lib.intercepted_requests.simple_logger import SimpleInterceptedRequestsLogger
from stoobly_agent.lib.utils.decode import decode

class TestReplayContext(ReplayContext):

  def __init__(self, replay_context: ReplayContext):
    super().__init__(replay_context.request)

    self.with_response(replay_context.response)
    self.end_time = replay_context.end_time
    self.start_time = replay_context.start_time

    self.__project_id = -1
    self.__request_log_entry = None

    if self.has_test_results:
      self.__request_log_entry = self.__load_request_log_entry()

  @property
  def has_test_results(self):
    headers = self.response.headers
    return headers.get(custom_headers.REQUEST_LOG_ROW_ID) is not None

  @property
  def project_id(self):
    return self.__project_id

  @project_id.setter
  def project_id(self, v):
    self.__project_id = v

  @property
  def request_log_entry(self) -> Union[dict, None]:
    return self.__request_log_entry

  @property
  def response_content(self):
    content = self.response.content
    content_type = self.response.headers.get('content-type')

    return decode_response(content, content_type)

  @property
  def response_status_code(self):
    return self.response.status_code

  @property
  def has_expected(self) -> bool:
    if self.__request_log_entry is not None:
      return any(
        key in self.__request_log_entry
        for key in ('expected_response', 'expected_status_code', 'expected_latency')
      )

    return self.response.headers.get(custom_headers.TEST_ID) is not None

  def diff_response(self, response: TestShowResponse, test_facade: TestFacade):
    if response['passed'] or response['skipped']:
      return (self.response_content, self.response_status_code, self.latency)

    if not self.has_expected:
      return None

    expected_response_content, expected_status_code = self.expected_response_content(test_facade)
    expected_latency = response.get('expected_latency')
    if expected_latency is None and self.__request_log_entry:
      expected_latency = self.__request_log_entry.get('expected_latency')

    return (
      diff(expected_response_content, self.response_content),
      diff(expected_status_code, self.response_status_code),
      diff(expected_latency, self.latency)
    )

  def expected_response_content(self, test_facade: TestFacade):
    if not self.has_expected:
      return None, None

    if self.__request_log_entry and 'expected_response' in self.__request_log_entry:
      expected = decode_expected_response(self.__request_log_entry.get('expected_response'))
      expected_status_code = self.__request_log_entry.get('expected_status_code') or 0
      return expected, expected_status_code

    response = self.__get_test_expected_response_with_context(test_facade)

    # Lazy import for runtime isinstance check
    from requests import Response
    if isinstance(response, Response):
      content = decode(response.content)
      content_type = response.headers.get('content-type')

      return decode_response(content, content_type), response.status_code
    else:
      return None, None

  def test_show_response(self, test_facade = None) -> TestShowResponse:
    if self.__request_log_entry is not None:
      entry = self.__request_log_entry

      # The following is inferred from settings (assumes nothing has changed)
      settings = Settings.instance()
      project_id = -1

      try:
        project_key = ProjectKey(settings.proxy.intercept.project_key) 
        project_id = project_key.id
      except InvalidProjectKey:
        pass

      test_id = self.response.headers.get(custom_headers.TEST_ID)

      return {
        'expected_latency': entry.get('expected_latency'),
        'id': test_id,
        'log': entry.get('log') or '',
        'passed': bool(entry.get('passed')),
        'project_id': project_id,
        'skipped': bool(entry.get('skipped')),
        'strategy': entry.get('strategy'),
      }

    return self.__get_test_response_with_context(test_facade)
    
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

  def __load_request_log_entry(self) -> Union[dict, None]:
    headers = self.response.headers
    row_id = headers.get(custom_headers.REQUEST_LOG_ROW_ID)
    if row_id is None:
      return None

    parsed_row_id = str(row_id).strip()
    if not parsed_row_id:
      return None

    return SimpleInterceptedRequestsLogger.get_entry(parsed_row_id)
