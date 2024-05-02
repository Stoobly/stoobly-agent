import pdb
import pytest

from click.testing import CliRunner
from typing import List

from stoobly_agent.test.test_helper import reset

from stoobly_agent.app.settings import Settings
from stoobly_agent.app.settings.constants import request_component
from stoobly_agent.app.settings.rewrite_rule import ParameterRule, RewriteRule, UrlRule
from stoobly_agent.cli import config
from stoobly_agent.config.constants import mode
from stoobly_agent.lib.api.keys.project_key import LOCAL_PROJECT_ID

@pytest.fixture(scope='class')
def settings():
  return reset()

@pytest.fixture(scope='module')
def runner():
  return CliRunner()

class TestRewrite():

  class TestParameter():

    @pytest.fixture(scope='class')
    def header_name(self):
      return 'access-token'

    @pytest.fixture(scope='class')
    def header_value(self):
      return ''

    @pytest.fixture(scope='class')
    def method(self):
      return 'GET'

    @pytest.fixture(scope='class')
    def _mode(self):
      return mode.RECORD

    @pytest.fixture(scope='class')
    def pattern(self):
      return '.*?'

    @pytest.fixture(scope='class')
    def _type(self):
      return request_component.HEADER

    @pytest.fixture(autouse=True, scope='class')
    def rewrite_result(self, settings: Settings, runner: CliRunner, method, _mode, header_name, header_value, pattern, _type):
      rewrite_result = runner.invoke(config, [
          'rewrite', 'set', 
          '--method', method, '--mode', _mode, '--name', header_name, '--value', header_value, '--pattern', pattern, '--type', _type
        ]
      )
      settings.load()
      return rewrite_result

    @pytest.fixture()
    def rewrite_rules(self, settings: Settings):
      return settings.proxy.rewrite.rewrite_rules(str(LOCAL_PROJECT_ID))

    @pytest.fixture()
    def rewrite_rule(self, rewrite_rules: List[RewriteRule]):
      return rewrite_rules[0]

    @pytest.fixture()
    def parameter_rule(self, rewrite_rule: RewriteRule):
      parameter_rules = rewrite_rule.parameter_rules
      return parameter_rules[0]

    def test_no_errors_returned(self, rewrite_result):
      assert rewrite_result.exit_code == 0

    def test_one_rewrite_rule(self, rewrite_rules: List[RewriteRule]):
      assert len(rewrite_rules) == 1

    def test_pattern(self, rewrite_rule: RewriteRule, pattern):
      assert rewrite_rule.pattern == pattern

    def test_methods(self, rewrite_rule: RewriteRule, method):
      assert rewrite_rule.methods == [method]

    def test_one_parameter_rule(self, rewrite_rule: RewriteRule):
      parameter_rules = rewrite_rule.parameter_rules
      assert len(parameter_rules) == 1

    def test_modes(self, parameter_rule: ParameterRule, _mode):
      assert parameter_rule.modes == [_mode]

    def test_type(self, parameter_rule: ParameterRule, _type):
      assert parameter_rule.type == _type

    def test_header_name(self, parameter_rule: ParameterRule, header_name):
      assert parameter_rule.name == header_name

    def test_header_value(self, parameter_rule: ParameterRule, header_value):
      assert parameter_rule.value == header_value

  class TestUrl():

    @pytest.fixture(scope='class')
    def scheme(self):
      return 'https'

    @pytest.fixture(scope='class')
    def hostname(self):
      return 'localhostname'

    @pytest.fixture(scope='class')
    def port(self):
      return '80'

    @pytest.fixture(scope='class')
    def method(self):
      return 'GET'

    @pytest.fixture(scope='class')
    def _mode(self):
      return mode.RECORD

    @pytest.fixture(scope='class')
    def path(self):
      return '/index.html'

    @pytest.fixture(scope='class')
    def pattern(self):
      return '.*?'

    @pytest.fixture(autouse=True, scope='class')
    def rewrite_result(self, settings: Settings, runner: CliRunner, method, _mode, path, pattern, scheme, hostname, port):
      rewrite_result = runner.invoke(config, [
          'rewrite', 'set', 
          '--method', method, '--mode', _mode, '--pattern', pattern, '--hostname', hostname, '--path', path, '--port', port, '--scheme', scheme,
        ]
      )
      settings.load()
      return rewrite_result

    @pytest.fixture()
    def rewrite_rules(self, settings: Settings):
      return settings.proxy.rewrite.rewrite_rules(str(LOCAL_PROJECT_ID))

    @pytest.fixture()
    def rewrite_rule(self, rewrite_rules: List[RewriteRule]):
      return rewrite_rules[0]

    @pytest.fixture()
    def url_rule(self, rewrite_rule: RewriteRule):
      url_rules = rewrite_rule.url_rules
      return url_rules[0]

    def test_no_errors_returned(self, rewrite_result):
      assert rewrite_result.exit_code == 0

    def test_one_rewrite_rule(self, rewrite_rules: List[RewriteRule]):
      assert len(rewrite_rules) == 1

    def test_pattern(self, rewrite_rule: RewriteRule, pattern):
      assert rewrite_rule.pattern == pattern

    def test_methods(self, rewrite_rule: RewriteRule, method):
      assert rewrite_rule.methods == [method]

    def test_one_url_rule(self, rewrite_rule: RewriteRule):
      url_rules = rewrite_rule.url_rules
      assert len(url_rules) == 1

    def test_modes(self, url_rule: UrlRule, _mode):
      assert url_rule.modes == [_mode]

    def test_url_hostname(self, url_rule: UrlRule, hostname):
      assert url_rule.hostname == hostname

    def test_url_path(self, url_rule: UrlRule, path: str):
      assert url_rule.path == path

    def test_url_port(self, url_rule: UrlRule, port):
      assert url_rule.port == port

    def test_url_scheme(self, url_rule: UrlRule, scheme):
      assert url_rule.scheme == scheme