import pytest
from click.testing import CliRunner

from stoobly_agent.test.test_helper import reset
from stoobly_agent.app.cli.request_cli import request


@pytest.fixture(scope='module')
def runner():
  return CliRunner()

@pytest.fixture(autouse=True, scope='module')
def settings():
  return reset('stoobly-agent-test-diff')


class TestRequestDiffCli:
  def test_it_gracefully_errors_on_bad_key(self, runner: CliRunner):
    res = runner.invoke(request, ['diff', 'p0.iBADBADBADBADBADBADBADBADBADBADB'])
    assert res.exit_code == 1
    assert 'Error: Invalid request key' in res.output
