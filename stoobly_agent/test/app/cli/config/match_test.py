import pdb
import pytest

from click.testing import CliRunner

from stoobly_agent.test.test_helper import reset

from stoobly_agent.app.settings import Settings
from stoobly_agent.app.settings.constants import request_component
from stoobly_agent.cli import config
from stoobly_agent.config.constants import mode
from stoobly_agent.lib.api.keys.project_key import LOCAL_PROJECT_ID

@pytest.fixture
def settings():
  return reset()

class TestMatch():

  def test_it_sets_rule(self, settings: Settings):
    runner = CliRunner()

    method = 'POST'
    _mode = mode.MOCK
    pattern = '.*?'

    match_result = runner.invoke(config, [
        'match', 'set', 
        '--method', method, '--mode', _mode, '--pattern', pattern, '--component', request_component.BODY_PARAM
      ]
    )
    assert match_result.exit_code == 0

    settings.load()

    match_rules =  settings.proxy.match.match_rules(str(LOCAL_PROJECT_ID))
    assert len(match_rules) == 1

    match_rule = match_rules[0]
    assert match_rule.pattern == pattern
    assert match_rule.methods == [method]
    assert match_rule.components == [request_component.BODY_PARAM]
    assert match_rule.modes == [_mode]