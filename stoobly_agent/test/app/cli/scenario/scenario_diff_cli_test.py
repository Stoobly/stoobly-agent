import pytest
from click.testing import CliRunner

from stoobly_agent.test.test_helper import reset
from stoobly_agent.app.cli.scenario_cli import scenario


@pytest.fixture(scope='module')
def runner():
  return CliRunner()

@pytest.fixture(autouse=True, scope='module')
def settings():
  return reset('stoobly-agent-test-scenario-diff')


class TestScenarioDiffCli:
  def test_it_gracefully_errors_on_bad_key(self, runner: CliRunner):
    res = runner.invoke(scenario, ['snapshot', 'diff', 'p0.sBADBADBADBADBADBADBADBADBADBADB'])
    # scenario diff handler prints error and exits(1)
    assert res.exit_code == 1
    assert 'Error: Invalid scenario key' in res.output
