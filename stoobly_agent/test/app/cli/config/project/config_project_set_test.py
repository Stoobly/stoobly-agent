import importlib
import pdb
import pytest

from click.testing import CliRunner

import stoobly_agent.cli

from stoobly_agent.test.test_helper import reset
from stoobly_agent.app.settings import Settings
from stoobly_agent.lib.api.keys import ProjectKey

@pytest.fixture(scope='module')
def runner():
    return CliRunner()

class TestConfigProjectSet():

  @pytest.fixture(scope='class', autouse=True)
  def settings(self):
    settings = reset()
    settings.cli.features.remote = True
    settings.commit()
    return settings

  @pytest.fixture(scope='class')
  def remote_enabled_config(scope='class'):
    importlib.reload(stoobly_agent.cli)
    from stoobly_agent.cli import config
    return config

  class TestWhenRecordPolicyOverwrite():
    def test_it_sets_scenario_overwritable(self, runner: CliRunner, remote_enabled_config, settings: Settings):
      settings.proxy.intercept.active = True
      settings.commit()

      project_key = settings.proxy.intercept.project_key
      _project_key = ProjectKey(project_key)

      set_results = runner.invoke(remote_enabled_config, ['project', 'set', _project_key.encode(1, _project_key.organization_id)])

      assert set_results.exit_code == 0

      settings.load()
      assert settings.proxy.intercept.active == False
