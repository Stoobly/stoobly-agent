import json
import os

import pytest
from click.testing import CliRunner

from stoobly_agent.app.settings import Settings
from stoobly_agent.cli import main
from stoobly_agent.config.data_dir import DataDir
from stoobly_agent.test.test_helper import reset


@pytest.fixture
def settings():
  return reset()


class TestDescribe:

  def test_describe_output(self, settings: Settings):
    runner = CliRunner()
    data_dir = DataDir.instance()

    result = runner.invoke(main, ['describe'])

    assert result.exit_code == 0

    data = json.loads(result.output)
    assert data['context_dir_path'] == data_dir.context_dir_path
    assert data['context_dir_path'] == os.path.abspath(os.path.join(data_dir.path, '..'))

    settings_dict = data['settings']
    assert 'proxy' in settings_dict
    assert 'ui' in settings_dict
    assert 'cli' not in settings_dict
    assert 'remote' not in settings_dict

  def test_setting_describe_removed(self, settings: Settings):
    runner = CliRunner()

    result = runner.invoke(main, ['setting', 'describe'])

    assert result.exit_code != 0
