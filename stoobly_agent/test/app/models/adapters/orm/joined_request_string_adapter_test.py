import json
import pdb
import pytest

from click.testing import CliRunner, Result

from stoobly_agent.test.test_helper import DETERMINISTIC_GET_REQUEST_URL, reset

from stoobly_agent.app.models.adapters.raw_joined.response import RawJoinedResponseAdapterFactory
from stoobly_agent.app.models.adapters.orm.joined_request_string_adapter import JoinedRequestStringAdapter
from stoobly_agent.cli import record
from stoobly_agent.lib.orm.request import Request

@pytest.fixture(scope='module')
def runner():
  return CliRunner()

class TestJoindRequestStringAdapter():
  @pytest.fixture(scope='class', autouse=True)
  def settings(self):
    return reset()

  class TestWhenEncoded():
    @pytest.fixture(scope='class')
    def record_result(self, runner: CliRunner) -> Result:
      url = DETERMINISTIC_GET_REQUEST_URL
      record_result = runner.invoke(record, ['--header', 'Accept-Encoding: gzip', url])
      return record_result

    @pytest.fixture(scope='class')
    def created_request(self, record_result: Result):
      assert record_result.exit_code == 0
      return Request.last()

    def test_idempotent(self, created_request: Request):
      adapter = JoinedRequestStringAdapter(created_request)
      assert adapter.adapt() == adapter.adapt()

    def test_it_decodes(self, created_request: Request):
      adapter = JoinedRequestStringAdapter(created_request)

      non_decoded_response = RawJoinedResponseAdapterFactory(adapter.adapt()).python_response()
      adapter.decode_response()

      decoded_response = RawJoinedResponseAdapterFactory(adapter.adapt()).python_response()

      assert len(non_decoded_response.content) == len(decoded_response.content)

  class TestWhenNotEncoded():
    @pytest.fixture(scope='class')
    def record_result(self, runner: CliRunner) -> Result:
      url = DETERMINISTIC_GET_REQUEST_URL
      record_result = runner.invoke(record, [url])
      return record_result

    @pytest.fixture(scope='class')
    def created_request(self, record_result: Result):
      assert record_result.exit_code == 0
      return Request.last()

    def test_idempotent(self, created_request: Request):
      adapter = JoinedRequestStringAdapter(created_request)
      assert adapter.adapt() == adapter.adapt()

    def test_it_decodes(self, created_request: Request):
      adapter = JoinedRequestStringAdapter(created_request)

      non_decoded_response = RawJoinedResponseAdapterFactory(adapter.adapt()).python_response()
      adapter.decode_response()

      decoded_response = RawJoinedResponseAdapterFactory(adapter.adapt()).python_response()

      assert len(non_decoded_response.content) == len(decoded_response.content)