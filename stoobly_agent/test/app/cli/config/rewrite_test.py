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

class TestRewrite():

  def test_it_sets_rule(self, settings: Settings):
    runner = CliRunner()

    header_name = 'access-token'
    header_value = ''
    method = 'GET'
    _mode = mode.RECORD
    pattern = '.*?'

    rewrite_result = runner.invoke(config, [
        'rewrite', 'set', 
        '--method', method, '--mode', _mode, '--name', header_name, '--value', header_value, '--pattern', pattern, '--type', request_component.HEADER
      ]
    )
    assert rewrite_result.exit_code == 0

    settings.load()

    rewrite_rules = settings.proxy.rewrite.rewrite_rules(str(LOCAL_PROJECT_ID))
    assert len(rewrite_rules) == 1

    rewrite_rule = rewrite_rules[0]
    assert rewrite_rule.pattern == pattern
    assert rewrite_rule.methods == [method]

    parameter_rules = rewrite_rule.parameter_rules
    assert len(parameter_rules) == 1

    parameter_rule = parameter_rules[0]
    assert parameter_rule.modes == [_mode]
    assert parameter_rule.type == request_component.HEADER
    assert parameter_rule.name == header_name
    assert parameter_rule.value == header_value