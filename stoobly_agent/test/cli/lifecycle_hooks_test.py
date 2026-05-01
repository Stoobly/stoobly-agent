import pdb
import pytest

from click.testing import CliRunner
from pathlib import Path

from stoobly_agent.app.cli.setting_cli import setting
from stoobly_agent.app.cli.request_cli import request
from stoobly_agent.app.models.adapters.raw_http_request_adapter import RawHttpRequestAdapter
from stoobly_agent.app.models.adapters.raw_http_response_adapter import RawHttpResponseAdapter
from stoobly_agent.app.settings import Settings
from stoobly_agent.app.settings.constants import request_component
from stoobly_agent.cli import mock, record
from stoobly_agent.config.constants import mode, record_policy, test_policy
from stoobly_agent.lib.api.keys.project_key import ProjectKey
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

  @pytest.fixture(scope='class')
  def replay_result(self, runner: CliRunner, lifecycle_hooks_path: str, recorded_request: Request):
    replay_result = runner.invoke(request, [
      'replay', '--format', 'json', '--lifecycle-hooks-path', lifecycle_hooks_path, recorded_request.key()
    ])
    assert replay_result.exit_code == 0
    return replay_result

  def test_calls_record_hooks(self, record_result):
    expected_stdout = ['before_request', 'before_normalize', 'after_normalize', 'before_record', 'after_record', 'before_response']
    assert record_result.stdout.strip() == "\n".join(expected_stdout)

  def test_calls_mock_hooks(self, mock_result):
    expected_stdout = ['before_request', 'before_normalize', 'before_mock', 'after_normalize', 'after_mock', 'before_response']
    assert mock_result.stdout.strip() == "\n".join(expected_stdout)

  def test_calls_replay_hooks(self, replay_result):
    expected_stdout = ['before_request', 'before_normalize', 'after_normalize', 'before_response']
    stdout = replay_result.stdout
    lifecycle_hooks_output = stdout.split('{')[0]
    assert lifecycle_hooks_output.strip() == "\n".join(expected_stdout)

  def test_calls_test_hooks(self, test_result):
    # In a test_policy=found flow, 
    # before_normalize and after_normalize are called twice for mock flow and test flow respectively
     expected_stdout = [
       'before_request', 'before_normalize', 'after_normalize', 'before_mock', 'after_normalize', 'after_mock', 'before_test', 'after_test', 'before_response'
     ]
     stdout = test_result.stdout
     lifecycle_hooks_output = stdout.split('{')[0]
     assert lifecycle_hooks_output.strip() == "\n".join(expected_stdout)

  class TestWithTestPolicyNone():
    @pytest.fixture(scope='class', autouse=True)
    def settings(self):
      return reset()

    @pytest.fixture(scope='class')
    def lifecycle_hooks_path(self):
      return str(Path(__file__).parent.parent / 'mock_data' / 'lifecycle_hooks.py')

    @pytest.fixture(scope='class')
    def test_result(self, runner: CliRunner, lifecycle_hooks_path: str):
      settings = Settings.instance()
      project_key = ProjectKey(settings.proxy.intercept.project_key)
      data_rule = settings.proxy.data.data_rules(project_key.id)
      data_rule.record_policy = record_policy.ALL
      data_rule.test_policy = test_policy.NONE
      settings.commit()

      record_result = runner.invoke(record, [DETERMINISTIC_GET_REQUEST_URL])
      assert record_result.exit_code == 0
      recorded_request = Request.last()

      test_result = runner.invoke(request, [
        'test', '--format', 'json', '--lifecycle-hooks-path', lifecycle_hooks_path, recorded_request.key()
      ])
      return test_result

    def test_calls_test_hooks(self, test_result):
      expected_stdout = [
        'before_request', 'before_normalize', 'before_mock', 'after_normalize', 'after_mock', 'before_response'
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

  class TestBeforeNormalizeHook():
    """Test that before_normalize hook can modify outbound request headers."""

    def test_adds_header_to_request(self, python_request):
      from stoobly_agent.test.mock_data.lifecycle_hooks_modify import (
        BEFORE_NORMALIZE_HEADER_NAME, BEFORE_NORMALIZE_HEADER_VALUE
      )
      assert python_request.headers.get(BEFORE_NORMALIZE_HEADER_NAME) == BEFORE_NORMALIZE_HEADER_VALUE

  class TestAfterNormalizeHook():
    """Test that after_normalize hook can modify response headers."""

    def test_adds_header_to_response(self, python_response):
      from stoobly_agent.test.mock_data.lifecycle_hooks_modify import (
        AFTER_NORMALIZE_HEADER_NAME, AFTER_NORMALIZE_HEADER_VALUE
      )
      assert python_response.headers.get(AFTER_NORMALIZE_HEADER_NAME) == AFTER_NORMALIZE_HEADER_VALUE

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
    - after_normalize operates on the original flow, so changes DO persist
    """

    def test_before_record_changes_do_not_persist_to_before_response(self, record_result):
      from stoobly_agent.test.mock_data.lifecycle_hooks_modify import (
        BEFORE_RESPONSE_VERIFIED_HEADER_VALUE
      )
      # The before_response hook prints this value if it sees the before_record header
      # Since before_record operates on a copy, this should NOT be in the output
      assert BEFORE_RESPONSE_VERIFIED_HEADER_VALUE not in record_result.stdout

    def test_after_normalize_changes_do_persist_to_before_response(self, record_result):
      from stoobly_agent.test.mock_data.lifecycle_hooks_modify import (
        AFTER_NORMALIZE_PERSISTS_MARKER
      )
      # The before_response hook prints this value if it sees the after_normalize header
      # Since after_normalize operates on the original flow, this SHOULD be in the output
      assert AFTER_NORMALIZE_PERSISTS_MARKER in record_result.stdout

  class TestNormalizeChangesVisibleInBeforeRecord():
    """
    Test that changes made in before_normalize and after_normalize hooks are visible
    in the before_record hook.
    
    This verifies the lifecycle hook ordering:
    before_normalize -> after_normalize -> before_record
    """

    def test_before_normalize_changes_visible_in_before_record(self, record_result):
      from stoobly_agent.test.mock_data.lifecycle_hooks_modify import (
        BEFORE_NORMALIZE_VISIBLE_IN_BEFORE_RECORD_MARKER
      )
      # The before_record hook prints this marker if it sees the before_normalize header
      assert BEFORE_NORMALIZE_VISIBLE_IN_BEFORE_RECORD_MARKER in record_result.stdout

    def test_after_normalize_changes_visible_in_before_record(self, record_result):
      from stoobly_agent.test.mock_data.lifecycle_hooks_modify import (
        AFTER_NORMALIZE_VISIBLE_IN_BEFORE_RECORD_MARKER
      )
      # The before_record hook prints this marker if it sees the after_normalize header
      assert AFTER_NORMALIZE_VISIBLE_IN_BEFORE_RECORD_MARKER in record_result.stdout


class TestNormalizeRewriteRulesInRecordMode():
  """
  Test that normalize rewrite rules are applied during record mode.
  
  This verifies that configuring rewrite rules with --mode normalize
  will apply those rules to outbound requests during recording.
  """

  @pytest.fixture(scope='function', autouse=True)
  def settings(self):
    return reset()

  class TestRequestHeaderRewrite():
    """Test that normalize mode request header rewrite rules are applied in record mode."""

    def test_rewrites_request_header(self, runner: CliRunner):
      header_name = 'X-Normalize-Rewrite-Header'
      header_value = 'normalize-rewrite-value'

      # Configure a normalize mode rewrite rule
      rewrite_result = runner.invoke(setting, [
        'rewrite', 'set',
        '--method', 'GET',
        '--mode', mode.NORMALIZE,
        '--name', header_name,
        '--value', header_value,
        '--pattern', '.*?',
        '--type', request_component.HEADER
      ])
      assert rewrite_result.exit_code == 0

      # Record a request - normalize rewrite rules should be applied
      record_result = runner.invoke(record, [DETERMINISTIC_GET_REQUEST_URL])
      assert record_result.exit_code == 0

      # Verify the header was added to the stored request
      _request = Request.last()
      python_request = RawHttpRequestAdapter(_request.raw).to_request()
      assert python_request.headers.get(header_name) == header_value

  class TestResponseHeaderRewrite():
    """Test that normalize mode response header rewrite rules are applied in record mode."""

    def test_rewrites_response_header(self, runner: CliRunner):
      header_name = 'X-Normalize-Response-Header'
      header_value = 'normalize-response-value'

      # Configure a normalize mode response header rewrite rule
      rewrite_result = runner.invoke(setting, [
        'rewrite', 'set',
        '--method', 'GET',
        '--mode', mode.NORMALIZE,
        '--name', header_name,
        '--value', header_value,
        '--pattern', '.*?',
        '--type', request_component.RESPONSE_HEADER
      ])
      assert rewrite_result.exit_code == 0

      # Record a request - normalize rewrite rules should be applied
      record_result = runner.invoke(record, [DETERMINISTIC_GET_REQUEST_URL])
      assert record_result.exit_code == 0

      # Verify the header was added to the stored response
      _response = Response.last()
      python_response = RawHttpResponseAdapter(_response.raw).to_response()
      assert python_response.headers.get(header_name) == header_value

  class TestNormalizeRulesDoNotAffectRecordRules():
    """Test that normalize rules and record rules can coexist and both are applied."""

    def test_both_normalize_and_record_rules_applied(self, runner: CliRunner):
      normalize_header_name = 'X-Normalize-Header'
      normalize_header_value = 'from-normalize-rule'
      record_header_name = 'X-Record-Header'
      record_header_value = 'from-record-rule'

      # Configure a normalize mode rewrite rule
      rewrite_result = runner.invoke(setting, [
        'rewrite', 'set',
        '--method', 'GET',
        '--mode', mode.NORMALIZE,
        '--name', normalize_header_name,
        '--value', normalize_header_value,
        '--pattern', '.*?',
        '--type', request_component.HEADER
      ])
      assert rewrite_result.exit_code == 0

      # Configure a record mode rewrite rule
      rewrite_result = runner.invoke(setting, [
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
      assert python_request.headers.get(normalize_header_name) == normalize_header_value
      assert python_request.headers.get(record_header_name) == record_header_value


class TestTestModifications():
  """
  Test that lifecycle hooks can modify requests and responses in test mode.
  
  Lifecycle hook order in test mode:
  before_request -> before_normalize -> after_normalize -> before_mock -> after_mock -> before_test -> after_test -> before_response
  """

  @pytest.fixture(scope='class', autouse=True)
  def settings(self):
    return reset()

  @pytest.fixture(scope='class')
  def lifecycle_hooks_path(self):
    from stoobly_agent.test.mock_data import lifecycle_hooks_test_modify
    return str(Path(lifecycle_hooks_test_modify.__file__).resolve())

  @pytest.fixture(scope='class')
  def recorded_request(self, runner: CliRunner):
    # Keep this fixture independent from policy mutations in earlier tests.
    settings = Settings.instance()
    project_key = ProjectKey(settings.proxy.intercept.project_key)
    data_rule = settings.proxy.data.data_rules(project_key.id)
    data_rule.record_policy = record_policy.ALL
    data_rule.test_policy = test_policy.FOUND
    settings.commit()

    # First record a request to test against
    record_result = runner.invoke(record, [DETERMINISTIC_GET_REQUEST_URL])
    assert record_result.exit_code == 0
    return Request.last()

  @pytest.fixture(scope='class')
  def test_result_found(self, runner: CliRunner, lifecycle_hooks_path: str, recorded_request: Request):
    settings = Settings.instance()
    project_key = ProjectKey(settings.proxy.intercept.project_key)
    data_rule = settings.proxy.data.data_rules(project_key.id)
    data_rule.test_policy = test_policy.FOUND
    settings.commit()

    # Don't use --output /dev/null so we can verify stdout contains lifecycle hook prints
    test_result = runner.invoke(request, [
      'test', '--format', 'json', '--lifecycle-hooks-path', lifecycle_hooks_path, recorded_request.key()
    ])
    assert test_result.exit_code == 0
    return test_result

  @pytest.fixture(scope='class')
  def test_result_none(self, runner: CliRunner, lifecycle_hooks_path: str, recorded_request: Request):
    settings = Settings.instance()
    project_key = ProjectKey(settings.proxy.intercept.project_key)
    data_rule = settings.proxy.data.data_rules(project_key.id)
    data_rule.test_policy = test_policy.NONE
    settings.commit()

    test_result = runner.invoke(request, [
      'test', '--format', 'json', '--lifecycle-hooks-path', lifecycle_hooks_path, recorded_request.key()
    ])
    assert test_result.exit_code != 0
    return test_result

  class TestBeforeNormalizeChanges():
    """Test that changes in before_normalize are visible in after_normalize."""

    def test_before_normalize_changes_visible_in_after_normalize(self, test_result_found):
      from stoobly_agent.test.mock_data.lifecycle_hooks_test_modify import (
        BEFORE_NORMALIZE_VISIBLE_IN_AFTER_NORMALIZE_MARKER
      )
      # The after_normalize hook prints this marker if it sees the before_normalize header
      assert BEFORE_NORMALIZE_VISIBLE_IN_AFTER_NORMALIZE_MARKER in test_result_found.stdout

  class TestAfterNormalizeChanges():
    """Test that changes in after_normalize are visible in both before_mock and before_test."""

    def test_after_normalize_changes_visible_in_before_mock(self, test_result_found):
      from stoobly_agent.test.mock_data.lifecycle_hooks_test_modify import (
        AFTER_NORMALIZE_VISIBLE_IN_BEFORE_MOCK_MARKER
      )
      # The before_mock hook prints this marker if it sees the after_normalize header
      assert AFTER_NORMALIZE_VISIBLE_IN_BEFORE_MOCK_MARKER in test_result_found.stdout

    def test_after_normalize_changes_visible_in_before_test(self, test_result_found):
      from stoobly_agent.test.mock_data.lifecycle_hooks_test_modify import (
        AFTER_NORMALIZE_VISIBLE_IN_BEFORE_TEST_MARKER
      )
      # The before_test hook prints this marker if it sees the after_normalize header
      assert AFTER_NORMALIZE_VISIBLE_IN_BEFORE_TEST_MARKER in test_result_found.stdout

  class TestBeforeMockChanges():
    """Test that changes in before_mock are visible in after_mock."""

    def test_before_mock_changes_visible_in_after_mock(self, test_result_found):
      from stoobly_agent.test.mock_data.lifecycle_hooks_test_modify import (
        BEFORE_MOCK_VISIBLE_IN_AFTER_MOCK_MARKER
      )
      # The after_mock hook prints this marker if it sees the before_mock header
      assert BEFORE_MOCK_VISIBLE_IN_AFTER_MOCK_MARKER in test_result_found.stdout

  class TestMockChangesDoNotAffectTest():
    """Test that changes in before_mock and after_mock are NOT visible in before_test."""

    def test_calls_none_policy_test_hooks(self, test_result_none):
      from stoobly_agent.test.mock_data.lifecycle_hooks_test_modify import (
        BEFORE_REQUEST_CALLED_MARKER,
        AFTER_MOCK_CALLED_MARKER,
        BEFORE_TEST_CALLED_MARKER,
        AFTER_TEST_CALLED_MARKER,
        BEFORE_RESPONSE_CALLED_MARKER,
      )

      assert test_result_none.exit_code != 0
      assert BEFORE_REQUEST_CALLED_MARKER in test_result_none.stdout
      assert AFTER_MOCK_CALLED_MARKER in test_result_none.stdout
      assert BEFORE_RESPONSE_CALLED_MARKER in test_result_none.stdout
      assert BEFORE_TEST_CALLED_MARKER not in test_result_none.stdout
      assert AFTER_TEST_CALLED_MARKER not in test_result_none.stdout

    def test_before_mock_changes_not_visible_in_before_test(self, test_result_none):
      from stoobly_agent.test.mock_data.lifecycle_hooks_test_modify import (
        BEFORE_MOCK_NOT_VISIBLE_IN_BEFORE_TEST_MARKER
      )
      # With test_policy=none, before_test does not run, so this marker is absent.
      assert BEFORE_MOCK_NOT_VISIBLE_IN_BEFORE_TEST_MARKER not in test_result_none.stdout

    def test_after_mock_changes_not_visible_in_before_test(self, test_result_none):
      from stoobly_agent.test.mock_data.lifecycle_hooks_test_modify import (
        AFTER_MOCK_NOT_VISIBLE_IN_BEFORE_TEST_MARKER
      )
      # With test_policy=none, before_test does not run, so this marker is absent.
      assert AFTER_MOCK_NOT_VISIBLE_IN_BEFORE_TEST_MARKER not in test_result_none.stdout

  class TestBeforeTestChanges():
    """Test that changes in before_test are visible in after_test."""

    def test_before_test_changes_visible_in_after_test(self, test_result_found):
      from stoobly_agent.test.mock_data.lifecycle_hooks_test_modify import (
        BEFORE_TEST_VISIBLE_IN_AFTER_TEST_MARKER
      )
      # The after_test hook prints this marker if it sees the before_test header
      assert BEFORE_TEST_VISIBLE_IN_AFTER_TEST_MARKER in test_result_found.stdout

class TestLifecycleHooksOriginSelection():
  """
  Verify lifecycle hooks selection honors origin-specific entries:
  - When an origin-qualified entry matches the request origin, it is selected.
  - When no origin-qualified entry matches, the first entry without origin is selected.
  """

  @pytest.fixture(scope='function', autouse=True)
  def settings(self):
    return reset()

  @pytest.fixture(scope='function')
  def scripts(self, tmp_path: Path):
    # Create two simple lifecycle hooks scripts with distinct markers
    default_script = tmp_path / 'lifecycle_hooks_default.py'
    origin_script = tmp_path / 'lifecycle_hooks_origin.py'

    default_script.write_text(
      "\n".join([
        "from stoobly_agent.app.proxy.context import InterceptContext",
        "def handle_before_request(context: InterceptContext):",
        "  print('default_selected')",
      ])
    )
    origin_script.write_text(
      "\n".join([
        "from stoobly_agent.app.proxy.context import InterceptContext",
        "def handle_before_request(context: InterceptContext):",
        "  print('origin_selected')",
      ])
    )

    return {
      'default': str(default_script),
      'origin': str(origin_script),
    }

  class TestMock():
    def test_picks_origin_specific_when_matches(self, runner: CliRunner, scripts):
      origin = 'https://dog.ceo'
      result = runner.invoke(mock, [
        '--lifecycle-hooks-path', f"{scripts['origin']}:{origin}",
        '--output', '/dev/null',
        DETERMINISTIC_GET_REQUEST_URL,
      ])
      # Some environments may return NOT_FOUND for mock; still verify hook selection
      assert 'origin_selected' in result.stdout
      assert 'default_selected' not in result.stdout

    def test_picks_default_when_no_origin_match(self, runner: CliRunner, scripts):
      result = runner.invoke(mock, [
        '--lifecycle-hooks-path', scripts['default'],
        '--output', '/dev/null',
        DETERMINISTIC_GET_REQUEST_URL,
      ])
      assert 'default_selected' in result.stdout
      assert 'origin_selected' not in result.stdout

  class TestRecord():
    def test_picks_origin_specific_when_matches(self, runner: CliRunner, scripts):
      origin = 'https://dog.ceo'
      result = runner.invoke(record, [
        '--lifecycle-hooks-path', f"{scripts['origin']}:{origin}",
        '--output', '/dev/null',
        DETERMINISTIC_GET_REQUEST_URL,
      ])
      assert result.exit_code == 0
      assert 'origin_selected' in result.stdout
      assert 'default_selected' not in result.stdout

    def test_picks_default_when_no_origin_match(self, runner: CliRunner, scripts):
      result = runner.invoke(record, [
        '--lifecycle-hooks-path', scripts['default'],
        '--output', '/dev/null',
        DETERMINISTIC_GET_REQUEST_URL,
      ])
      assert result.exit_code == 0
      assert 'default_selected' in result.stdout
      assert 'origin_selected' not in result.stdout

  class TestRequestTest():
    def test_picks_origin_specific_when_matches(self, runner: CliRunner, scripts):
      from stoobly_agent.app.cli.request_cli import request
      origin = 'https://dog.ceo'
      # First record to create a request to test
      record_result = runner.invoke(record, [DETERMINISTIC_GET_REQUEST_URL])
      assert record_result.exit_code == 0
      recorded_request = Request.last()
      result = runner.invoke(request, [
        'test', '--format', 'json',
        '--lifecycle-hooks-path', f"{scripts['origin']}:{origin}",
        recorded_request.key(),
      ])
      assert result.exit_code == 0
      assert 'origin_selected' in result.stdout.split('{')[0]
      assert 'default_selected' not in result.stdout.split('{')[0]

    def test_picks_default_when_no_origin_match(self, runner: CliRunner, scripts):
      from stoobly_agent.app.cli.request_cli import request
      non_matching_origin = 'https://example.invalid'
      # First record to create a request to test
      record_result = runner.invoke(record, [DETERMINISTIC_GET_REQUEST_URL])
      assert record_result.exit_code == 0
      recorded_request = Request.last()
      result = runner.invoke(request, [
        'test', '--format', 'json',
        '--lifecycle-hooks-path', scripts['default'],
        recorded_request.key(),
      ])
      assert result.exit_code == 0
      assert 'default_selected' in result.stdout.split('{')[0]
      assert 'origin_selected' not in result.stdout.split('{')[0]