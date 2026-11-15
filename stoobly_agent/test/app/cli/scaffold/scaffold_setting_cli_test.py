import os

import pytest
from click.testing import CliRunner

from stoobly_agent.app.cli.scaffold.constants import SERVICES_NAMESPACE
from stoobly_agent.app.cli.scaffold.settings_init_manager import (
  SCAFFOLD_SETTINGS_DELIMITER_BEGIN,
  SCAFFOLD_SETTINGS_DELIMITER_END,
)
from stoobly_agent.app.cli.scaffold.templates.constants import CORE_BUILD_SERVICE_NAME, CUSTOM_INIT
from stoobly_agent.app.cli.scaffold_setting_cli import setting
from stoobly_agent.config.app_data_dir import SERVICES_CONFIG_FILE_PATH
from stoobly_agent.config.data_dir import DATA_DIR_NAME, DataDir
from stoobly_agent.test.test_helper import reset


def _make_scaffold_app_dir(app_dir: str) -> str:
  services_config_path = os.path.join(app_dir, DATA_DIR_NAME, SERVICES_CONFIG_FILE_PATH)
  os.makedirs(os.path.dirname(services_config_path), exist_ok=True)
  if not os.path.exists(services_config_path):
    with open(services_config_path, 'w') as fp:
      fp.write('')
  return app_dir


def _build_init_path(app_dir: str, workflow_name: str) -> str:
  return os.path.join(
    app_dir, DATA_DIR_NAME, SERVICES_NAMESPACE, CORE_BUILD_SERVICE_NAME, workflow_name, CUSTOM_INIT
  )


def _create_build_init(app_dir: str, workflow_name: str, contents: str = None) -> str:
  init_path = _build_init_path(app_dir, workflow_name)
  os.makedirs(os.path.dirname(init_path), exist_ok=True)
  with open(init_path, 'w') as fp:
    fp.write(contents if contents is not None else "#! /bin/bash\n\n# Add custom initialization here\n")
  return init_path


def _settings_block(contents: str) -> str:
  begin = contents.index(SCAFFOLD_SETTINGS_DELIMITER_BEGIN)
  end = contents.index(SCAFFOLD_SETTINGS_DELIMITER_END)
  return contents[begin:end + len(SCAFFOLD_SETTINGS_DELIMITER_END)]


class TestScaffoldSettingCli:
  @pytest.fixture(autouse=True)
  def settings(self):
    return reset()

  @pytest.fixture(autouse=True)
  def isolate_data_dir_cache(self):
    DataDir._instances = None
    yield
    DataDir._instances = None

  @pytest.fixture
  def app_dir(self, tmp_path):
    app_dir = os.path.join(str(tmp_path), 'test-app')
    os.makedirs(app_dir)
    _make_scaffold_app_dir(app_dir)
    # App.valid requires services namespace and context .stoobly
    os.makedirs(os.path.join(app_dir, DATA_DIR_NAME, SERVICES_NAMESPACE), exist_ok=True)
    return app_dir

  def test_rewrite_set_prepends_settings_block(self, app_dir):
    init_path = _create_build_init(app_dir, 'record')

    result = CliRunner().invoke(setting, [
      'rewrite', 'set',
      '--method', 'GET',
      '--mode', 'record',
      '--pattern', '.*',
      '--name', 'authorization',
      '--type', 'Header',
      '--value', '',
      '--workflow', 'record',
      '--app-dir-path', app_dir,
    ])

    assert result.exit_code == 0, result.output
    with open(init_path) as fp:
      contents = fp.read()

    assert contents.startswith('#! /bin/bash\n')
    assert SCAFFOLD_SETTINGS_DELIMITER_BEGIN in contents
    assert SCAFFOLD_SETTINGS_DELIMITER_END in contents

    block = _settings_block(contents)
    assert "stoobly-agent setting rewrite set" in block
    assert "--method GET" in block
    assert "--mode record" in block
    assert "--pattern" in block
    assert "--name authorization" in block
    assert "--type Header" in block
    assert "# Add custom initialization here" in contents
    # Settings block must appear before the rest of the custom content.
    assert contents.index(SCAFFOLD_SETTINGS_DELIMITER_BEGIN) < contents.index('# Add custom initialization here')

  def test_second_set_appends_inside_markers(self, app_dir):
    init_path = _create_build_init(app_dir, 'record')

    runner = CliRunner()
    first = runner.invoke(setting, [
      'rewrite', 'set',
      '--method', 'GET',
      '--mode', 'record',
      '--pattern', '.*',
      '--name', 'authorization',
      '--type', 'Header',
      '--value', '',
      '--workflow', 'record',
      '--app-dir-path', app_dir,
    ])
    assert first.exit_code == 0, first.output

    second = runner.invoke(setting, [
      'filter', 'set',
      '--action', 'exclude',
      '--method', 'POST',
      '--mode', 'record',
      '--pattern', '.*',
      '--workflow', 'record',
      '--app-dir-path', app_dir,
    ])
    assert second.exit_code == 0, second.output

    with open(init_path) as fp:
      contents = fp.read()

    assert contents.count(SCAFFOLD_SETTINGS_DELIMITER_BEGIN) == 1
    assert contents.count(SCAFFOLD_SETTINGS_DELIMITER_END) == 1

    block = _settings_block(contents)
    assert "stoobly-agent setting rewrite set" in block
    assert "stoobly-agent setting filter set" in block
    assert block.index("stoobly-agent setting rewrite set") < block.index("stoobly-agent setting filter set")

  def test_match_set_writes_command(self, app_dir):
    init_path = _create_build_init(app_dir, 'mock')

    result = CliRunner().invoke(setting, [
      'match', 'set',
      '--method', 'POST',
      '--mode', 'mock',
      '--pattern', '.*',
      '--component', 'Header',
      '--workflow', 'mock',
      '--app-dir-path', app_dir,
    ])

    assert result.exit_code == 0, result.output
    with open(init_path) as fp:
      contents = fp.read()

    block = _settings_block(contents)
    assert "stoobly-agent setting match set" in block
    assert "--component Header" in block
    assert "--mode mock" in block

  def test_intercept_enable_writes_command_for_workflows(self, app_dir):
    develop_init = _create_build_init(app_dir, 'develop')
    mock_init = _create_build_init(app_dir, 'mock')

    result = CliRunner().invoke(setting, [
      'intercept', 'enable',
      '--workflow', 'develop',
      '--workflow', 'mock',
      '--app-dir-path', app_dir,
    ])

    assert result.exit_code == 0, result.output
    for init_path in (develop_init, mock_init):
      with open(init_path) as fp:
        contents = fp.read()
      block = _settings_block(contents)
      assert 'stoobly-agent intercept enable' in block

  def test_overwrite_replaces_settings_section(self, app_dir):
    init_path = _create_build_init(app_dir, 'record')
    runner = CliRunner()

    first = runner.invoke(setting, [
      'rewrite', 'set',
      '--method', 'GET',
      '--mode', 'record',
      '--pattern', '.*',
      '--name', 'authorization',
      '--type', 'Header',
      '--value', '',
      '--workflow', 'record',
      '--app-dir-path', app_dir,
    ])
    assert first.exit_code == 0, first.output

    second = runner.invoke(setting, [
      'filter', 'set',
      '--action', 'exclude',
      '--method', 'POST',
      '--mode', 'record',
      '--pattern', '.*',
      '--overwrite',
      '--workflow', 'record',
      '--app-dir-path', app_dir,
    ])
    assert second.exit_code == 0, second.output

    with open(init_path) as fp:
      contents = fp.read()

    assert contents.count(SCAFFOLD_SETTINGS_DELIMITER_BEGIN) == 1
    assert contents.count(SCAFFOLD_SETTINGS_DELIMITER_END) == 1

    block = _settings_block(contents)
    assert 'stoobly-agent setting filter set' in block
    assert 'stoobly-agent setting rewrite set' not in block

  def test_intercept_overwrite_replaces_settings_section(self, app_dir):
    init_path = _create_build_init(app_dir, 'mock')
    runner = CliRunner()

    first = runner.invoke(setting, [
      'match', 'set',
      '--method', 'GET',
      '--mode', 'mock',
      '--pattern', '.*',
      '--workflow', 'mock',
      '--app-dir-path', app_dir,
    ])
    assert first.exit_code == 0, first.output

    second = runner.invoke(setting, [
      'intercept', 'enable',
      '--overwrite',
      '--workflow', 'mock',
      '--app-dir-path', app_dir,
    ])
    assert second.exit_code == 0, second.output

    block = _settings_block(open(init_path).read())
    assert 'stoobly-agent intercept enable' in block
    assert 'stoobly-agent setting match set' not in block

  def test_missing_init_exits_nonzero(self, app_dir):
    result = CliRunner().invoke(setting, [
      'filter', 'set',
      '--action', 'include',
      '--method', 'GET',
      '--mode', 'mock',
      '--pattern', '.*',
      '--workflow', 'record',
      '--app-dir-path', app_dir,
    ])

    assert result.exit_code != 0
    assert 'Init script not found' in result.output or 'Init script not found' in (result.exception and str(result.exception) or '')
