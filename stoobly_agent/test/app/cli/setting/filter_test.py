import pdb
import pytest

from click.testing import CliRunner

from stoobly_agent.test.test_helper import reset

from stoobly_agent.app.cli.setting_cli import setting
from stoobly_agent.app.settings import Settings
from stoobly_agent.app.settings.constants import filter_action
from stoobly_agent.config.constants import mode
from stoobly_agent.lib.api.keys.project_key import LOCAL_PROJECT_ID

@pytest.fixture
def settings():
  return reset()

class TestFilter():

  def test_it_sets_rule(self, settings: Settings):
    runner = CliRunner()

    method = 'POST'
    _mode = mode.MOCK
    pattern = '.*?'

    filter_result = runner.invoke(setting, [
        'filter', 'set',
        '--method', method, '--mode', _mode, '--pattern', pattern, '--action', filter_action.EXCLUDE
      ]
    )
    assert filter_result.exit_code == 0

    settings.load()

    filter_rules = settings.proxy.filter.filter_rules(str(LOCAL_PROJECT_ID))
    assert len(filter_rules) == 1

    filter_rule = filter_rules[0]
    assert filter_rule.pattern == pattern
    assert filter_rule.methods == [method]
    assert filter_rule.action == filter_action.EXCLUDE
    assert filter_rule.modes == [_mode]