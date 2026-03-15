import importlib
import os
import pdb
import pytest

from click.testing import CliRunner

from stoobly_agent.app.cli import setting_cli
from stoobly_agent.app.settings import Settings
from stoobly_agent.config.constants import env_vars
from stoobly_agent.test.test_helper import reset
from stoobly_agent.lib.api.keys import ProjectKey

@pytest.fixture(scope='module')
def setting():
  importlib.reload(env_vars) # Fix strange bug where FEATURE_REMOTE does not exist
  os.environ[env_vars.FEATURE_REMOTE] = '1'
  importlib.reload(setting_cli)
  del os.environ[env_vars.FEATURE_REMOTE]
  return setting_cli.setting

class TestSettingsProjectSet():

  @pytest.fixture(scope='class', autouse=True)
  def settings(self):
    return reset()

  class TestWhenRecordPolicyOverwrite():

    def test_it_sets_scenario_overwritable(self, setting, settings: Settings):
      settings.proxy.intercept.active = True
      settings.commit()

      project_key = settings.proxy.intercept.project_key
      _project_key = ProjectKey(project_key)

      set_results = CliRunner().invoke(setting, ['project', 'set', _project_key.encode(1, _project_key.organization_id)])
      assert set_results.exit_code == 0

      settings.load()
      assert settings.proxy.intercept.active == False
