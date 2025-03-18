import pdb
import pytest

from click.testing import CliRunner
from pathlib import Path

from stoobly_agent.cli import mock, record, request
from stoobly_agent.lib.orm.request import Request
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
    expected_stdout = ['before_request', 'before_record', 'after_record', 'before_response']
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