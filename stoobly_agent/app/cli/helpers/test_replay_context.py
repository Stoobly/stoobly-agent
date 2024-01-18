import pdb

from typing import Union

from stoobly_agent.app.cli.helpers.context import ReplayContext
from stoobly_agent.app.cli.helpers.test_facade import TestFacade
from stoobly_agent.app.proxy.test.helpers.test_results_builder import TestResultsBuilder
from stoobly_agent.app.proxy.test.helpers.diff_service import diff
from stoobly_agent.app.settings import Settings
from stoobly_agent.config.constants import custom_headers
from stoobly_agent.lib.api.interfaces.tests import TestShowResponse
from stoobly_agent.lib.api.keys.project_key import InvalidProjectKey, ProjectKey

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
      return self.response.content

  @property
  def test_results_builder(self):
    return self.__test_results_builder

  def test_show_response(self, test_facade = None) -> TestShowResponse:
    if not self.has_test_results: 
      return self.__get_test_response_with_context(test_facade)
    else:
      builder = self.test_results_builder
      headers = self.response.headers

      # The following is inferred from settings (assumes nothing has changed)
      settings = Settings.instance()
      project_id = -1

      try:
        project_key = ProjectKey(settings.proxy.intercept.project_key) 
        project_id = project_key.id
      except InvalidProjectKey:
        pass

      return {
        'expected_latency': headers.get(custom_headers.RESPONSE_LATENCY),
        'id': None,
        'log': self.__build_log(builder),
        'passed': builder.passed,
        'project_id': project_id,
        'strategy': builder.strategy,
      }

  def __build_log(self, builder: TestResultsBuilder):
    log = [builder.log]

    if not builder.passed:
      log.append("\n" + diff(builder.expected_response, builder.received_response))

    return "\n".join(log)

  def __get_test_response_with_context(self, test_facade: TestFacade) -> Union[TestShowResponse, str]:
    try:
      res = test_facade.show_with_context(super(), self.project_id)
      return res
    except AssertionError as e:
      return f"API Error: {e}"