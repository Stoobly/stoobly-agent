import os

import pytest
from click.testing import CliRunner

from stoobly_agent.app.cli.scaffold.constants import SERVICES_NAMESPACE
from stoobly_agent.app.cli.scaffold.settings_init_manager import (
  SCAFFOLD_INTERCEPT_DELIMITER_BEGIN,
  SCAFFOLD_INTERCEPT_DELIMITER_END,
  SCAFFOLD_SETTINGS_DELIMITER_BEGIN,
  SCAFFOLD_SETTINGS_DELIMITER_END,
)
from stoobly_agent.app.cli.scaffold.templates.constants import CORE_BUILD_SERVICE_NAME, CUSTOM_INIT
from stoobly_agent.app.cli.scaffold_intercept_cli import intercept
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


def _intercept_block(contents: str) -> str:
  begin = contents.index(SCAFFOLD_INTERCEPT_DELIMITER_BEGIN)
  end = contents.index(SCAFFOLD_INTERCEPT_DELIMITER_END)
  return contents[begin:end + len(SCAFFOLD_INTERCEPT_DELIMITER_END)]


class TestScaffoldInterceptCli:
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
    os.makedirs(os.path.join(app_dir, DATA_DIR_NAME, SERVICES_NAMESPACE), exist_ok=True)
    return app_dir

  def test_enable_prepends_intercept_block(self, app_dir):
    init_path = _create_build_init(app_dir, 'record')

    result = CliRunner().invoke(intercept, [
      'enable',
      '--workflow', 'record',
      '--app-dir-path', app_dir,
    ])

    assert result.exit_code == 0, result.output
    with open(init_path) as fp:
      contents = fp.read()

    assert contents.startswith('#! /bin/bash\n')
    assert SCAFFOLD_INTERCEPT_DELIMITER_BEGIN in contents
    assert SCAFFOLD_INTERCEPT_DELIMITER_END in contents

    block = _intercept_block(contents)
    assert "stoobly-agent intercept enable" in block
    assert "# Add custom initialization here" in contents
    assert contents.index(SCAFFOLD_INTERCEPT_DELIMITER_BEGIN) < contents.index('# Add custom initialization here')

  def test_set_writes_command(self, app_dir):
    init_path = _create_build_init(app_dir, 'record')

    result = CliRunner().invoke(intercept, [
      'set',
      '--mode', 'record',
      '--policy', 'all',
      '--order', 'append',
      '--strategy', 'full',
      '--workflow', 'record',
      '--app-dir-path', app_dir,
    ])

    assert result.exit_code == 0, result.output
    with open(init_path) as fp:
      contents = fp.read()

    block = _intercept_block(contents)
    assert "stoobly-agent intercept set" in block
    assert "--mode record" in block
    assert "--policy all" in block
    assert "--order append" in block
    assert "--strategy full" in block

  def test_second_command_appends_inside_markers(self, app_dir):
    init_path = _create_build_init(app_dir, 'mock')

    runner = CliRunner()
    first = runner.invoke(intercept, [
      'set',
      '--mode', 'mock',
      '--policy', 'all',
      '--workflow', 'mock',
      '--app-dir-path', app_dir,
    ])
    assert first.exit_code == 0, first.output

    second = runner.invoke(intercept, [
      'enable',
      '--workflow', 'mock',
      '--app-dir-path', app_dir,
    ])
    assert second.exit_code == 0, second.output

    with open(init_path) as fp:
      contents = fp.read()

    assert contents.count(SCAFFOLD_INTERCEPT_DELIMITER_BEGIN) == 1
    assert contents.count(SCAFFOLD_INTERCEPT_DELIMITER_END) == 1

    block = _intercept_block(contents)
    assert "stoobly-agent intercept set" in block
    assert "stoobly-agent intercept enable" in block
    assert block.index("stoobly-agent intercept set") < block.index("stoobly-agent intercept enable")

  def test_intercept_block_uses_intercept_delimiter_after_settings(self, app_dir):
    init_path = _create_build_init(app_dir, 'record')
    runner = CliRunner()

    setting_result = runner.invoke(setting, [
      'filter', 'set',
      '--action', 'exclude',
      '--method', 'GET',
      '--mode', 'record',
      '--pattern', '.*',
      '--workflow', 'record',
      '--app-dir-path', app_dir,
    ])
    assert setting_result.exit_code == 0, setting_result.output

    intercept_result = runner.invoke(intercept, [
      'enable',
      '--workflow', 'record',
      '--app-dir-path', app_dir,
    ])
    assert intercept_result.exit_code == 0, intercept_result.output

    with open(init_path) as fp:
      contents = fp.read()

    assert SCAFFOLD_SETTINGS_DELIMITER_BEGIN in contents
    assert SCAFFOLD_INTERCEPT_DELIMITER_BEGIN in contents
    assert SCAFFOLD_SETTINGS_DELIMITER_BEGIN not in _intercept_block(contents)
    assert contents.index(SCAFFOLD_SETTINGS_DELIMITER_END) < contents.index(SCAFFOLD_INTERCEPT_DELIMITER_BEGIN)
    assert "stoobly-agent intercept enable" in _intercept_block(contents)

  def test_disable_writes_command(self, app_dir):
    init_path = _create_build_init(app_dir, 'test')

    result = CliRunner().invoke(intercept, [
      'disable',
      '--workflow', 'test',
      '--app-dir-path', app_dir,
    ])

    assert result.exit_code == 0, result.output
    with open(init_path) as fp:
      contents = fp.read()

    block = _intercept_block(contents)
    assert "stoobly-agent intercept disable" in block

  def test_multiple_workflows(self, app_dir):
    record_init = _create_build_init(app_dir, 'record')
    mock_init = _create_build_init(app_dir, 'mock')

    result = CliRunner().invoke(intercept, [
      'enable',
      '--workflow', 'record',
      '--workflow', 'mock',
      '--app-dir-path', app_dir,
    ])

    assert result.exit_code == 0, result.output
    for init_path in (record_init, mock_init):
      with open(init_path) as fp:
        contents = fp.read()
      assert "stoobly-agent intercept enable" in _intercept_block(contents)

  def test_defaults_to_all_workflows(self, app_dir):
    record_init = _create_build_init(app_dir, 'record')
    mock_init = _create_build_init(app_dir, 'mock')

    result = CliRunner().invoke(intercept, [
      'enable',
      '--app-dir-path', app_dir,
    ])

    assert result.exit_code == 0, result.output
    for init_path in (record_init, mock_init):
      with open(init_path) as fp:
        contents = fp.read()
      assert "stoobly-agent intercept enable" in _intercept_block(contents)

  def test_set_requires_an_option(self, app_dir):
    _create_build_init(app_dir, 'record')

    result = CliRunner().invoke(intercept, [
      'set',
      '--workflow', 'record',
      '--app-dir-path', app_dir,
    ])

    assert result.exit_code != 0
    assert 'Missing an option' in result.output or 'Missing an option' in (result.exception and str(result.exception) or '')

  def test_missing_init_exits_nonzero(self, app_dir):
    result = CliRunner().invoke(intercept, [
      'enable',
      '--workflow', 'record',
      '--app-dir-path', app_dir,
    ])

    assert result.exit_code != 0
    assert 'Init script not found' in result.output or 'Init script not found' in (result.exception and str(result.exception) or '')

  def test_no_build_workflows_exits_nonzero(self, app_dir):
    result = CliRunner().invoke(intercept, [
      'enable',
      '--app-dir-path', app_dir,
    ])

    assert result.exit_code != 0
    assert 'No build workflow init scripts found' in result.output or 'No build workflow init scripts found' in (result.exception and str(result.exception) or '')
