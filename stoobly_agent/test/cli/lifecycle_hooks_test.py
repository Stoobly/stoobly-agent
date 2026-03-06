import pdb
import pytest

from click.testing import CliRunner
from pathlib import Path

from stoobly_agent.app.cli.config_cli import config
from stoobly_agent.app.cli.request_cli import request
from stoobly_agent.app.models.adapters.raw_http_request_adapter import RawHttpRequestAdapter
from stoobly_agent.app.models.adapters.raw_http_response_adapter import RawHttpResponseAdapter
from stoobly_agent.app.settings.constants import request_component
from stoobly_agent.cli import mock, record
from stoobly_agent.config.constants import mode
from stoobly_agent.lib.orm.request import Request
from stoobly_agent.lib.orm.response import Response
from stoobly_agent.test.test_helper import DETERMINISTIC_GET_REQUEST_URL, reset

@pytest.fixture(scope='module')
def runner():
  return CliRunner()

class TestLifecycleHooks():
  @pytest.fixture(scope='class', autouse=True)
  def settings(self):
    return reset()

  @pytest.fixture(scope='class')
  def lifecycle_hooks_path(self):
    return str(Path(__file__).parent.parent / 'mock_data' / 'lifecycle_hooks.py')

  @pytest.fixture(scope='class')
  def record_result(self, runner: CliRunner, lifecycle_hooks_path: str):
    record_result = runner.invoke(record, [
      '--lifecycle-hooks-path', lifecycle_hooks_path, '--output', '/dev/null', DETERMINISTIC_GET_REQUEST_URL
    ])
    assert record_result.exit_code == 0
    return record_result

  @pytest.fixture(scope='class')
  def recorded_request(self):
    return Request.last()

  @pytest.fixture(scope='class')
  def mock_result(self, runner: CliRunner, lifecycle_hooks_path: str):
    mock_result = runner.invoke(mock, [
      '--lifecycle-hooks-path', lifecycle_hooks_path, '--output', '/dev/null', DETERMINISTIC_GET_REQUEST_URL
    ])
    assert mock_result.exit_code == 0
    return mock_result

  @pytest.fixture(scope='class')
  def test_result(self, runner: CliRunner, lifecycle_hooks_path: str, recorded_request: Request):
    test_result = runner.invoke(request, [
      'test', '--format', 'json', '--lifecycle-hooks-path', lifecycle_hooks_path, recorded_request.key() 
    ])
    assert test_result.exit_code == 0
    return test_result

  def test_calls_record_hooks(self, record_result):
    expected_stdout = ['before_request', 'before_replay', 'after_replay', 'before_record', 'after_record', 'before_response']
    assert record_result.stdout.strip() == "\n".join(expected_stdout)

  def test_calls_mock_hooks(self, mock_result):
    expected_stdout = ['before_request', 'before_mock', 'after_mock', 'before_response']
    assert mock_result.stdout.strip() == "\n".join(expected_stdout)

  def test_calls_test_hooks(self, test_result):
     expected_stdout = [
       'before_request', 'before_replay', 'after_replay', 'before_mock', 'after_mock', 'before_test', 'after_test', 'before_response'
     ]
     stdout = test_result.stdout
     lifecycle_hooks_output = stdout.split('{')[0]
     assert lifecycle_hooks_output.strip() == "\n".join(expected_stdout)


class TestRecordModifications():
  """Test that lifecycle hooks can modify requests and responses in record mode."""

  @pytest.fixture(scope='class', autouse=True)
  def settings(self):
    return reset()

  @pytest.fixture(scope='class')
  def lifecycle_hooks_path(self):
    return str(Path(__file__).parent.parent / 'mock_data' / 'lifecycle_hooks_modify.py')

  @pytest.fixture(scope='class')
  def record_result(self, runner: CliRunner, lifecycle_hooks_path: str):
    # Don't use --output /dev/null so we can verify stdout contains lifecycle hook prints
    record_result = runner.invoke(record, [
      '--lifecycle-hooks-path', lifecycle_hooks_path, DETERMINISTIC_GET_REQUEST_URL
    ])
    assert record_result.exit_code == 0
    return record_result

  @pytest.fixture(scope='class')
  def recorded_request(self, record_result):
    return Request.last()

  @pytest.fixture(scope='class')
  def recorded_response(self, record_result):
    return Response.last()

  @pytest.fixture(scope='class')
  def python_request(self, recorded_request: Request):
    return RawHttpRequestAdapter(recorded_request.raw).to_request()

  @pytest.fixture(scope='class')
  def python_response(self, recorded_response: Response):
    return RawHttpResponseAdapter(recorded_response.raw).to_response()

  class TestBeforeReplayHook():
    """Test that before_replay hook can modify outbound request headers."""

    def test_adds_header_to_request(self, python_request):
      from stoobly_agent.test.mock_data.lifecycle_hooks_modify import (
        BEFORE_REPLAY_HEADER_NAME, BEFORE_REPLAY_HEADER_VALUE
      )
      assert python_request.headers.get(BEFORE_REPLAY_HEADER_NAME) == BEFORE_REPLAY_HEADER_VALUE

  class TestAfterReplayHook():
    """Test that after_replay hook can modify response headers."""

    def test_adds_header_to_response(self, python_response):
      from stoobly_agent.test.mock_data.lifecycle_hooks_modify import (
        AFTER_REPLAY_HEADER_NAME, AFTER_REPLAY_HEADER_VALUE
      )
      assert python_response.headers.get(AFTER_REPLAY_HEADER_NAME) == AFTER_REPLAY_HEADER_VALUE

  class TestBeforeRecordHook():
    """Test that before_record hook can modify request before storage."""

    def test_adds_header_to_stored_request(self, python_request):
      from stoobly_agent.test.mock_data.lifecycle_hooks_modify import (
        BEFORE_RECORD_HEADER_NAME, BEFORE_RECORD_HEADER_VALUE
      )
      assert python_request.headers.get(BEFORE_RECORD_HEADER_NAME) == BEFORE_RECORD_HEADER_VALUE

  class TestHookPersistence():
    """
    Test which hook changes persist to before_response.
    
    - before_record operates on a deep copy, so changes do NOT persist
    - after_replay operates on the original flow, so changes DO persist
    """

    def test_before_record_changes_do_not_persist_to_before_response(self, record_result):
      from stoobly_agent.test.mock_data.lifecycle_hooks_modify import (
        BEFORE_RESPONSE_VERIFIED_HEADER_VALUE
      )
      # The before_response hook prints this value if it sees the before_record header
      # Since before_record operates on a copy, this should NOT be in the output
      assert BEFORE_RESPONSE_VERIFIED_HEADER_VALUE not in record_result.stdout

    def test_after_replay_changes_do_persist_to_before_response(self, record_result):
      from stoobly_agent.test.mock_data.lifecycle_hooks_modify import (
        AFTER_REPLAY_PERSISTS_MARKER
      )
      # The before_response hook prints this value if it sees the after_replay header
      # Since after_replay operates on the original flow, this SHOULD be in the output
      assert AFTER_REPLAY_PERSISTS_MARKER in record_result.stdout

  class TestReplayChangesVisibleInBeforeRecord():
    """
    Test that changes made in before_replay and after_replay hooks are visible
    in the before_record hook.
    
    This verifies the lifecycle hook ordering:
    before_replay -> after_replay -> before_record
    """

    def test_before_replay_changes_visible_in_before_record(self, record_result):
      from stoobly_agent.test.mock_data.lifecycle_hooks_modify import (
        BEFORE_REPLAY_VISIBLE_IN_BEFORE_RECORD_MARKER
      )
      # The before_record hook prints this marker if it sees the before_replay header
      assert BEFORE_REPLAY_VISIBLE_IN_BEFORE_RECORD_MARKER in record_result.stdout

    def test_after_replay_changes_visible_in_before_record(self, record_result):
      from stoobly_agent.test.mock_data.lifecycle_hooks_modify import (
        AFTER_REPLAY_VISIBLE_IN_BEFORE_RECORD_MARKER
      )
      # The before_record hook prints this marker if it sees the after_replay header
      assert AFTER_REPLAY_VISIBLE_IN_BEFORE_RECORD_MARKER in record_result.stdout


class TestReplayRewriteRulesInRecordMode():
  """
  Test that replay rewrite rules are applied during record mode.
  
  This verifies that configuring rewrite rules with --mode replay
  will apply those rules to outbound requests during recording.
  """

  @pytest.fixture(scope='function', autouse=True)
  def settings(self):
    return reset()

  class TestRequestHeaderRewrite():
    """Test that replay mode request header rewrite rules are applied in record mode."""

    def test_rewrites_request_header(self, runner: CliRunner):
      header_name = 'X-Replay-Rewrite-Header'
      header_value = 'replay-rewrite-value'

      # Configure a replay mode rewrite rule
      rewrite_result = runner.invoke(config, [
        'rewrite', 'set',
        '--method', 'GET',
        '--mode', mode.REPLAY,
        '--name', header_name,
        '--value', header_value,
        '--pattern', '.*?',
        '--type', request_component.HEADER
      ])
      assert rewrite_result.exit_code == 0

      # Record a request - replay rewrite rules should be applied
      record_result = runner.invoke(record, [DETERMINISTIC_GET_REQUEST_URL])
      assert record_result.exit_code == 0

      # Verify the header was added to the stored request
      _request = Request.last()
      python_request = RawHttpRequestAdapter(_request.raw).to_request()
      assert python_request.headers.get(header_name) == header_value

  class TestResponseHeaderRewrite():
    """Test that replay mode response header rewrite rules are applied in record mode."""

    def test_rewrites_response_header(self, runner: CliRunner):
      header_name = 'X-Replay-Response-Header'
      header_value = 'replay-response-value'

      # Configure a replay mode response header rewrite rule
      rewrite_result = runner.invoke(config, [
        'rewrite', 'set',
        '--method', 'GET',
        '--mode', mode.REPLAY,
        '--name', header_name,
        '--value', header_value,
        '--pattern', '.*?',
        '--type', request_component.RESPONSE_HEADER
      ])
      assert rewrite_result.exit_code == 0

      # Record a request - replay rewrite rules should be applied
      record_result = runner.invoke(record, [DETERMINISTIC_GET_REQUEST_URL])
      assert record_result.exit_code == 0

      # Verify the header was added to the stored response
      _response = Response.last()
      python_response = RawHttpResponseAdapter(_response.raw).to_response()
      assert python_response.headers.get(header_name) == header_value

  class TestReplayRulesDoNotAffectRecordRules():
    """Test that replay rules and record rules can coexist and both are applied."""

    def test_both_replay_and_record_rules_applied(self, runner: CliRunner):
      replay_header_name = 'X-Replay-Header'
      replay_header_value = 'from-replay-rule'
      record_header_name = 'X-Record-Header'
      record_header_value = 'from-record-rule'

      # Configure a replay mode rewrite rule
      rewrite_result = runner.invoke(config, [
        'rewrite', 'set',
        '--method', 'GET',
        '--mode', mode.REPLAY,
        '--name', replay_header_name,
        '--value', replay_header_value,
        '--pattern', '.*?',
        '--type', request_component.HEADER
      ])
      assert rewrite_result.exit_code == 0

      # Configure a record mode rewrite rule
      rewrite_result = runner.invoke(config, [
        'rewrite', 'set',
        '--method', 'GET',
        '--mode', mode.RECORD,
        '--name', record_header_name,
        '--value', record_header_value,
        '--pattern', '.*?',
        '--type', request_component.HEADER
      ])
      assert rewrite_result.exit_code == 0

      # Record a request - both rules should be applied
      record_result = runner.invoke(record, [DETERMINISTIC_GET_REQUEST_URL])
      assert record_result.exit_code == 0

      # Verify both headers were added
      _request = Request.last()
      python_request = RawHttpRequestAdapter(_request.raw).to_request()
      assert python_request.headers.get(replay_header_name) == replay_header_value
      assert python_request.headers.get(record_header_name) == record_header_value


class TestTestModifications():
  """
  Test that lifecycle hooks can modify requests and responses in test mode.
  
  Lifecycle hook order in test mode:
  before_request -> before_replay -> after_replay -> before_mock -> after_mock -> before_test -> after_test -> before_response
  """

  @pytest.fixture(scope='class', autouse=True)
  def settings(self):
    return reset()

  @pytest.fixture(scope='class')
  def lifecycle_hooks_path(self):
    return str(Path(__file__).parent.parent / 'mock_data' / 'lifecycle_hooks_test_modify.py')

  @pytest.fixture(scope='class')
  def recorded_request(self, runner: CliRunner):
    # First record a request to test against
    record_result = runner.invoke(record, [DETERMINISTIC_GET_REQUEST_URL])
    assert record_result.exit_code == 0
    return Request.last()

  @pytest.fixture(scope='class')
  def test_result(self, runner: CliRunner, lifecycle_hooks_path: str, recorded_request: Request):
    # Don't use --output /dev/null so we can verify stdout contains lifecycle hook prints
    test_result = runner.invoke(request, [
      'test', '--format', 'json', '--lifecycle-hooks-path', lifecycle_hooks_path, recorded_request.key()
    ])
    assert test_result.exit_code == 0
    return test_result

  class TestBeforeReplayChanges():
    """Test that changes in before_replay are visible in after_replay."""

    def test_before_replay_changes_visible_in_after_replay(self, test_result):
      from stoobly_agent.test.mock_data.lifecycle_hooks_test_modify import (
        BEFORE_REPLAY_VISIBLE_IN_AFTER_REPLAY_MARKER
      )
      # The after_replay hook prints this marker if it sees the before_replay header
      assert BEFORE_REPLAY_VISIBLE_IN_AFTER_REPLAY_MARKER in test_result.stdout

  class TestAfterReplayChanges():
    """Test that changes in after_replay are visible in both before_mock and before_test."""

    def test_after_replay_changes_visible_in_before_mock(self, test_result):
      from stoobly_agent.test.mock_data.lifecycle_hooks_test_modify import (
        AFTER_REPLAY_VISIBLE_IN_BEFORE_MOCK_MARKER
      )
      # The before_mock hook prints this marker if it sees the after_replay header
      assert AFTER_REPLAY_VISIBLE_IN_BEFORE_MOCK_MARKER in test_result.stdout

    def test_after_replay_changes_visible_in_before_test(self, test_result):
      from stoobly_agent.test.mock_data.lifecycle_hooks_test_modify import (
        AFTER_REPLAY_VISIBLE_IN_BEFORE_TEST_MARKER
      )
      # The before_test hook prints this marker if it sees the after_replay header
      assert AFTER_REPLAY_VISIBLE_IN_BEFORE_TEST_MARKER in test_result.stdout

  class TestBeforeMockChanges():
    """Test that changes in before_mock are visible in after_mock."""

    def test_before_mock_changes_visible_in_after_mock(self, test_result):
      from stoobly_agent.test.mock_data.lifecycle_hooks_test_modify import (
        BEFORE_MOCK_VISIBLE_IN_AFTER_MOCK_MARKER
      )
      # The after_mock hook prints this marker if it sees the before_mock header
      assert BEFORE_MOCK_VISIBLE_IN_AFTER_MOCK_MARKER in test_result.stdout

  class TestMockChangesDoNotAffectTest():
    """Test that changes in before_mock and after_mock are NOT visible in before_test."""

    def test_before_mock_changes_not_visible_in_before_test(self, test_result):
      from stoobly_agent.test.mock_data.lifecycle_hooks_test_modify import (
        BEFORE_MOCK_NOT_VISIBLE_IN_BEFORE_TEST_MARKER
      )
      # The before_test hook prints this marker if it does NOT see the before_mock header
      assert BEFORE_MOCK_NOT_VISIBLE_IN_BEFORE_TEST_MARKER in test_result.stdout

    def test_after_mock_changes_not_visible_in_before_test(self, test_result):
      from stoobly_agent.test.mock_data.lifecycle_hooks_test_modify import (
        AFTER_MOCK_NOT_VISIBLE_IN_BEFORE_TEST_MARKER
      )
      # The before_test hook prints this marker if it does NOT see the after_mock header
      assert AFTER_MOCK_NOT_VISIBLE_IN_BEFORE_TEST_MARKER in test_result.stdout

  class TestBeforeTestChanges():
    """Test that changes in before_test are visible in after_test."""

    def test_before_test_changes_visible_in_after_test(self, test_result):
      from stoobly_agent.test.mock_data.lifecycle_hooks_test_modify import (
        BEFORE_TEST_VISIBLE_IN_AFTER_TEST_MARKER
      )
      # The after_test hook prints this marker if it sees the before_test header
      assert BEFORE_TEST_VISIBLE_IN_AFTER_TEST_MARKER in test_result.stdout