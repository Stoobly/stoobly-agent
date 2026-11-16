import os

import pytest
import yaml
from click.testing import CliRunner

from stoobly_agent.app.cli.scaffold.constants import SERVICES_NAMESPACE
from stoobly_agent.app.cli.scaffold.settings_init_manager import (
  SCAFFOLD_INIT_DELIMITER_BEGIN,
  SCAFFOLD_INIT_DELIMITER_END,
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


def _init_block(contents: str) -> str:
  begin = contents.index(SCAFFOLD_INIT_DELIMITER_BEGIN)
  end = contents.index(SCAFFOLD_INIT_DELIMITER_END)
  return contents[begin:end + len(SCAFFOLD_INIT_DELIMITER_END)]


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

  def test_rewrite_set_prepends_init_block(self, app_dir):
    init_path = _create_build_init(app_dir, 'record')

    result = CliRunner().invoke(setting, ['rewrite', 'set', '--apply',
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
    assert SCAFFOLD_INIT_DELIMITER_BEGIN in contents
    assert SCAFFOLD_INIT_DELIMITER_END in contents

    block = _init_block(contents)
    assert "stoobly-agent setting rewrite set" in block
    assert "--method GET" in block
    assert "--mode record" in block
    assert "--pattern" in block
    assert "--name authorization" in block
    assert "--type Header" in block
    assert "# Add custom initialization here" in contents
    # Init block must appear before the rest of the custom content.
    assert contents.index(SCAFFOLD_INIT_DELIMITER_BEGIN) < contents.index('# Add custom initialization here')

  def test_second_set_appends_inside_markers(self, app_dir):
    init_path = _create_build_init(app_dir, 'record')

    runner = CliRunner()
    first = runner.invoke(setting, ['rewrite', 'set', '--apply',
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

    second = runner.invoke(setting, ['filter', 'set', '--apply',
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

    assert contents.count(SCAFFOLD_INIT_DELIMITER_BEGIN) == 1
    assert contents.count(SCAFFOLD_INIT_DELIMITER_END) == 1

    block = _init_block(contents)
    assert "stoobly-agent setting rewrite set" in block
    assert "stoobly-agent setting filter set" in block
    assert block.index("stoobly-agent setting rewrite set") < block.index("stoobly-agent setting filter set")

  def test_match_set_writes_command(self, app_dir):
    init_path = _create_build_init(app_dir, 'mock')

    result = CliRunner().invoke(setting, ['match', 'set', '--apply',
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

    block = _init_block(contents)
    assert "stoobly-agent setting match set" in block
    assert "--component Header" in block
    assert "--mode mock" in block

  def test_saves_scaffold_yml_by_default(self, app_dir):
    init_path = _create_build_init(app_dir, 'record')
    before = open(init_path).read()
    scaffold_path = os.path.join(app_dir, DATA_DIR_NAME, 'scaffold.yml')
    assert not os.path.exists(scaffold_path)

    result = CliRunner().invoke(setting, [
      'filter', 'set',
      '--action', 'exclude',
      '--method', 'POST',
      '--mode', 'record',
      '--pattern', '.*',
      '--workflow', 'record',
      '--app-dir-path', app_dir,
    ])
    assert result.exit_code == 0, result.output
    assert os.path.exists(scaffold_path)
    relative_path = os.path.relpath(scaffold_path)
    assert f'Updated {relative_path}, run `' in result.output
    assert f'scaffold apply {relative_path}' in result.output
    assert open(init_path).read() == before

    with open(scaffold_path) as fp:
      data = yaml.safe_load(fp)

    assert data['version'] == 1
    assert len(data['commands']) == 1
    step = data['commands'][0]
    assert step['resource'] == 'setting'
    assert step['action'] == 'filter set'
    assert step['options']['action'] == 'exclude'
    assert step['options']['method'] == ['POST']
    assert step['options']['mode'] == ['record']
    assert step['options']['pattern'] == '.*'
    assert step['options']['workflow'] == ['record']
    assert step['options']['app_dir_path'] == app_dir
    assert 'apply' not in step['options']
    assert 'save' not in step['options']

  def test_apply_updates_init_without_scaffold_yml(self, app_dir):
    init_path = _create_build_init(app_dir, 'record')
    scaffold_path = os.path.join(app_dir, DATA_DIR_NAME, 'scaffold.yml')

    result = CliRunner().invoke(setting, [
      'filter', 'set',
      '--action', 'exclude',
      '--method', 'POST',
      '--mode', 'record',
      '--pattern', '.*',
      '--apply',
      '--workflow', 'record',
      '--app-dir-path', app_dir,
    ])
    assert result.exit_code == 0, result.output
    assert not os.path.exists(scaffold_path)
    assert SCAFFOLD_INIT_DELIMITER_BEGIN in open(init_path).read()

  def test_save_appends_to_existing_scaffold_yml(self, app_dir):
    _create_build_init(app_dir, 'record')
    scaffold_path = os.path.join(app_dir, DATA_DIR_NAME, 'scaffold.yml')
    with open(scaffold_path, 'w') as fp:
      yaml.safe_dump({
        'version': 1,
        'commands': [
          {'resource': 'app', 'action': 'create', 'options': {'app_name': 'existing'}},
        ],
      }, fp)

    result = CliRunner().invoke(setting, [
      'match', 'set',
      '--method', 'GET',
      '--mode', 'mock',
      '--pattern', '.*',
      '--workflow', 'record',
      '--app-dir-path', app_dir,
    ])
    assert result.exit_code == 0, result.output

    with open(scaffold_path) as fp:
      data = yaml.safe_load(fp)

    assert len(data['commands']) == 2
    assert data['commands'][0]['resource'] == 'app'
    assert data['commands'][1]['resource'] == 'setting'
    assert data['commands'][1]['action'] == 'match set'

  def test_filter_set_upserts_same_pattern_and_methods(self, app_dir):
    _create_build_init(app_dir, 'record')
    scaffold_path = os.path.join(app_dir, DATA_DIR_NAME, 'scaffold.yml')
    runner = CliRunner()

    first = runner.invoke(setting, [
      'filter', 'set',
      '--action', 'exclude',
      '--method', 'GET',
      '--mode', 'record',
      '--pattern', '.*',
      '--workflow', 'record',
      '--app-dir-path', app_dir,
    ])
    assert first.exit_code == 0, first.output

    second = runner.invoke(setting, [
      'filter', 'set',
      '--action', 'include',
      '--method', 'GET',
      '--mode', 'mock',
      '--pattern', '.*',
      '--workflow', 'record',
      '--app-dir-path', app_dir,
    ])
    assert second.exit_code == 0, second.output

    with open(scaffold_path) as fp:
      data = yaml.safe_load(fp)

    assert len(data['commands']) == 1
    step = data['commands'][0]
    assert step['action'] == 'filter set'
    assert step['options']['action'] == 'include'
    assert step['options']['mode'] == ['mock']

  def test_rewrite_set_keeps_distinct_names(self, app_dir):
    _create_build_init(app_dir, 'record')
    scaffold_path = os.path.join(app_dir, DATA_DIR_NAME, 'scaffold.yml')
    runner = CliRunner()
    common = [
      '--method', 'GET',
      '--mode', 'record',
      '--pattern', '.*',
      '--type', 'Header',
      '--value', '',
      '--workflow', 'record',
      '--app-dir-path', app_dir,
    ]

    first = runner.invoke(setting, ['rewrite', 'set', '--name', 'authorization', *common])
    assert first.exit_code == 0, first.output
    second = runner.invoke(setting, ['rewrite', 'set', '--name', 'cookie', *common])
    assert second.exit_code == 0, second.output

    with open(scaffold_path) as fp:
      data = yaml.safe_load(fp)

    assert [c['options']['name'] for c in data['commands']] == ['authorization', 'cookie']

  def test_defaults_to_all_workflows(self, app_dir):
    record_init = _create_build_init(app_dir, 'record')
    mock_init = _create_build_init(app_dir, 'mock')

    result = CliRunner().invoke(setting, ['filter', 'set', '--apply',
      '--action', 'exclude',
      '--method', 'GET',
      '--mode', 'record',
      '--pattern', '.*',
      '--app-dir-path', app_dir,
    ])

    assert result.exit_code == 0, result.output
    for init_path in (record_init, mock_init):
      with open(init_path) as fp:
        contents = fp.read()
      assert "stoobly-agent setting filter set" in _init_block(contents)

  def test_missing_init_exits_nonzero(self, app_dir):
    result = CliRunner().invoke(setting, [
      'filter', 'set',
      '--apply',
      '--action', 'include',
      '--method', 'GET',
      '--mode', 'mock',
      '--pattern', '.*',
      '--workflow', 'record',
      '--app-dir-path', app_dir,
    ])

    assert result.exit_code != 0
    assert 'Init script not found' in result.output or 'Init script not found' in (result.exception and str(result.exception) or '')
