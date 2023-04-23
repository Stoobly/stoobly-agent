import pdb
import pytest

from click.testing import CliRunner

from stoobly_agent.test.test_helper import reset

from stoobly_agent.app.settings import Settings
from stoobly_agent.app.settings.constants import firewall_action
from stoobly_agent.cli import config
from stoobly_agent.config.constants import mode
from stoobly_agent.lib.api.keys.project_key import LOCAL_PROJECT_ID

@pytest.fixture
def settings():
  return reset()

class TestFirewall():

  def test_it_sets_rule(self, settings: Settings):
    runner = CliRunner()

    method = 'POST'
    _mode = mode.MOCK
    pattern = '.*?'

    firewall_result = runner.invoke(config, [
        'firewall', 'set', 
        '--method', method, '--mode', _mode, '--pattern', pattern, '--action', firewall_action.EXCLUDE
      ]
    )
    assert firewall_result.exit_code == 0

    settings.load()

    firewall_rules = settings.proxy.firewall.firewall_rules(str(LOCAL_PROJECT_ID))
    assert len(firewall_rules) == 1

    firewall_rule = firewall_rules[0]
    assert firewall_rule.pattern == pattern
    assert firewall_rule.methods == [method]
    assert firewall_rule.action == firewall_action.EXCLUDE
    assert firewall_rule.modes == [_mode]