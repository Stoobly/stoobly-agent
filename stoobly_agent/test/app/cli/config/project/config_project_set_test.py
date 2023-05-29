import importlib
import pdb
import pytest

from click.testing import CliRunner

import stoobly_agent.app.cli.config_cli
import stoobly_agent.cli

from stoobly_agent.test.test_helper import reset
from stoobly_agent.app.settings import Settings
from stoobly_agent.lib.api.keys import ProjectKey

class TestConfigProjectSet():

  @pytest.fixture(scope='class', autouse=True)
  def settings(self):
    settings = reset()
    settings.cli.features.remote = True
    settings.commit()
    return settings

  class TestWhenRecordPolicyOverwrite():

    @pytest.mark.skip(reason="Passes when run individually, otherwise fails")
    def test_it_sets_scenario_overwritable(self, settings: Settings):
      settings.proxy.intercept.active = True
      settings.commit()

      project_key = settings.proxy.intercept.project_key
      _project_key = ProjectKey(project_key)

      importlib.reload(stoobly_agent.app.cli.config_cli)
      importlib.reload(stoobly_agent.cli)

      from stoobly_agent.cli import config
      set_results = CliRunner().invoke(config, ['project', 'set', _project_key.encode(1, _project_key.organization_id)])
      assert set_results.exit_code == 0

      settings.load()
      assert settings.proxy.intercept.active == False
