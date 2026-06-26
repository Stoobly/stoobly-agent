import os
import pathlib

import pytest
import yaml
import json

from click.testing import CliRunner

from stoobly_agent.app.cli.scaffold.constants import APP_COPY_ON_WORKFLOW_UP_ENV, CONFIG_FILE
from stoobly_agent.app.cli.scaffold_cli import scaffold
from stoobly_agent.cli import init as cli_init
from stoobly_agent.config.data_dir import DATA_DIR_NAME
from stoobly_agent.test.test_helper import reset


@pytest.fixture(scope='module', autouse=True)
def settings():
  return reset()


@pytest.fixture(scope='module')
def runner():
  return CliRunner()


def _prepare_app_dir(app_dir_path: pathlib.Path):
  pathlib.Path(f"{app_dir_path}/{DATA_DIR_NAME}").mkdir(parents=True, exist_ok=True)


def _context_config_path(context_dir_path: pathlib.Path) -> pathlib.Path:
  return context_dir_path / DATA_DIR_NAME / CONFIG_FILE


def _read_config(path: pathlib.Path) -> dict:
  with open(path, 'r') as fp:
    return yaml.safe_load(fp)


def _read_settings(context_dir_path: pathlib.Path) -> dict:
  settings_path = context_dir_path / DATA_DIR_NAME / 'settings.yml'
  with open(settings_path, 'r') as fp:
    return yaml.safe_load(fp)


def _write_config(path: pathlib.Path, config: dict):
  path.parent.mkdir(parents=True, exist_ok=True)
  with open(path, 'w') as fp:
    yaml.dump(config, fp)


def _create_app_with_context(runner: CliRunner, app_dir_path: pathlib.Path, context_dir_path: pathlib.Path):
  app_dir_path.mkdir()
  context_dir_path.mkdir()
  _prepare_app_dir(app_dir_path)

  result = runner.invoke(scaffold, [
    'app', 'create',
    '--app-dir-path', str(app_dir_path),
    '--context-dir-path', str(context_dir_path),
    '--quiet',
    'test-app',
  ])
  assert result.exit_code == 0


def _create_service(
  runner: CliRunner,
  app_dir_path: pathlib.Path,
  service_name: str,
  context_dir_path: pathlib.Path = None,
):
  command = [
    'service', 'create',
    '--app-dir-path', str(app_dir_path),
    '--quiet',
    service_name,
  ]
  if context_dir_path:
    command.extend(['--context-dir-path', str(context_dir_path)])

  result = runner.invoke(scaffold, command)
  assert result.exit_code == 0


class TestScaffoldAppCreateValidation:
  def test_copy_on_workflow_up_allowed_with_local_runtime(self, runner: CliRunner, tmp_path):
    docker_socket_path = tmp_path / 'docker.sock'
    docker_socket_path.touch()
    _prepare_app_dir(tmp_path)

    result = runner.invoke(scaffold, [
      'app', 'create',
      '--app-dir-path', str(tmp_path),
      '--copy-on-workflow-up',
      '--docker-socket-path', str(docker_socket_path),
      '--runtime', 'local',
      '--quiet',
      'test-app',
    ])

    assert result.exit_code == 0

    config_path = tmp_path / DATA_DIR_NAME / 'services' / CONFIG_FILE
    config = _read_config(config_path)
    assert config[APP_COPY_ON_WORKFLOW_UP_ENV] is True
    assert config['APP_RUNTIME'] == 'local'

  def test_context_dir_path_must_exist(self, runner: CliRunner, tmp_path):
    app_dir_path = tmp_path / 'app'
    app_dir_path.mkdir()
    _prepare_app_dir(app_dir_path)

    missing_context_dir = tmp_path / 'missing-context'

    result = runner.invoke(scaffold, [
      'app', 'create',
      '--app-dir-path', str(app_dir_path),
      '--context-dir-path', str(missing_context_dir),
      '--quiet',
      'test-app',
    ])

    assert result.exit_code != 0


class TestScaffoldAppCreateContextDirPaths:
  def test_writes_scaffold_app_dir_path_to_context_config(self, runner: CliRunner, tmp_path):
    app_dir_path = tmp_path / 'app'
    context_dir_path = tmp_path / 'context'
    app_dir_path.mkdir()
    context_dir_path.mkdir()
    _prepare_app_dir(app_dir_path)

    result = runner.invoke(scaffold, [
      'app', 'create',
      '--app-dir-path', str(app_dir_path),
      '--context-dir-path', str(context_dir_path),
      '--quiet',
      'test-app',
    ])

    assert result.exit_code == 0

    config = _read_config(_context_config_path(context_dir_path))
    assert config['scaffold']['app_dir_path'] == os.path.relpath(str(app_dir_path), str(context_dir_path))
    assert config['scaffold']['services'] == []
    assert not os.path.isabs(config['scaffold']['app_dir_path'])

  def test_writes_config_for_multiple_context_dirs(self, runner: CliRunner, tmp_path):
    app_dir_path = tmp_path / 'app'
    context_a = tmp_path / 'context-a'
    context_b = tmp_path / 'context-b'
    app_dir_path.mkdir()
    context_a.mkdir()
    context_b.mkdir()
    _prepare_app_dir(app_dir_path)

    result = runner.invoke(scaffold, [
      'app', 'create',
      '--app-dir-path', str(app_dir_path),
      '--context-dir-path', str(context_a),
      '--context-dir-path', str(context_b),
      '--quiet',
      'test-app',
    ])

    assert result.exit_code == 0

    for context_dir_path in (context_a, context_b):
      config = _read_config(_context_config_path(context_dir_path))
      assert config['scaffold']['app_dir_path'] == os.path.relpath(str(app_dir_path), str(context_dir_path))
      assert config['scaffold']['services'] == []
      assert (context_dir_path / DATA_DIR_NAME / 'settings.yml').exists()

  def test_rerun_preserves_existing_config_properties(self, runner: CliRunner, tmp_path):
    app_dir_path = tmp_path / 'app'
    context_dir_path = tmp_path / 'context'
    app_dir_path.mkdir()
    context_dir_path.mkdir()
    _prepare_app_dir(app_dir_path)

    config_path = _context_config_path(context_dir_path)
    _write_config(config_path, {'workflow': {'name': 'record'}})

    runner.invoke(scaffold, [
      'app', 'create',
      '--app-dir-path', str(app_dir_path),
      '--context-dir-path', str(context_dir_path),
      '--quiet',
      'test-app',
    ])

    result = runner.invoke(scaffold, [
      'app', 'create',
      '--app-dir-path', str(app_dir_path),
      '--context-dir-path', str(context_dir_path),
      '--quiet',
      'test-app',
    ])

    assert result.exit_code == 0

    config = _read_config(config_path)
    assert config['workflow']['name'] == 'record'
    assert config['scaffold']['app_dir_path'] == os.path.relpath(str(app_dir_path), str(context_dir_path))

  def test_rerun_resets_services_to_empty(self, runner: CliRunner, tmp_path):
    app_dir_path = tmp_path / 'app'
    context_dir_path = tmp_path / 'context'
    app_dir_path.mkdir()
    context_dir_path.mkdir()
    _prepare_app_dir(app_dir_path)

    runner.invoke(scaffold, [
      'app', 'create',
      '--app-dir-path', str(app_dir_path),
      '--context-dir-path', str(context_dir_path),
      '--quiet',
      'test-app',
    ])

    runner.invoke(scaffold, [
      'service', 'create',
      '--app-dir-path', str(app_dir_path),
      '--context-dir-path', str(context_dir_path),
      '--quiet',
      'api',
    ])

    assert _read_config(_context_config_path(context_dir_path))['scaffold']['services'] == ['api']

    result = runner.invoke(scaffold, [
      'app', 'create',
      '--app-dir-path', str(app_dir_path),
      '--context-dir-path', str(context_dir_path),
      '--quiet',
      'test-app',
    ])

    assert result.exit_code == 0
    assert _read_config(_context_config_path(context_dir_path))['scaffold']['services'] == []

  def test_rerun_preserves_existing_context_settings(self, runner: CliRunner, tmp_path):
    app_dir_path = tmp_path / 'app'
    context_dir_path = tmp_path / 'context'
    app_dir_path.mkdir()
    context_dir_path.mkdir()
    _prepare_app_dir(app_dir_path)

    runner.invoke(scaffold, [
      'app', 'create',
      '--app-dir-path', str(app_dir_path),
      '--context-dir-path', str(context_dir_path),
      '--quiet',
      'test-app',
    ])

    settings_path = context_dir_path / DATA_DIR_NAME / 'settings.yml'
    settings = _read_settings(context_dir_path)
    settings['remote']['api_key'] = 'preserve-me'
    with open(settings_path, 'w') as fp:
      yaml.dump(settings, fp)

    result = runner.invoke(scaffold, [
      'app', 'create',
      '--app-dir-path', str(app_dir_path),
      '--context-dir-path', str(context_dir_path),
      '--quiet',
      'test-app',
    ])

    assert result.exit_code == 0

    updated_settings = _read_settings(context_dir_path)
    assert updated_settings['remote']['api_key'] == 'preserve-me'

  def test_init_does_not_write_context_config(self, runner: CliRunner, tmp_path):
    context_dir_path = tmp_path / 'context'
    context_dir_path.mkdir()

    with runner.isolated_filesystem(temp_dir=str(context_dir_path)):
      result = runner.invoke(cli_init, [])

    assert result.exit_code == 0
    assert not _context_config_path(context_dir_path).exists()


class TestScaffoldServiceCreateContextDirPaths:
  def test_adds_service_to_context_config(self, runner: CliRunner, tmp_path):
    app_dir_path = tmp_path / 'app'
    context_dir_path = tmp_path / 'context'
    app_dir_path.mkdir()
    context_dir_path.mkdir()
    _prepare_app_dir(app_dir_path)

    runner.invoke(scaffold, [
      'app', 'create',
      '--app-dir-path', str(app_dir_path),
      '--context-dir-path', str(context_dir_path),
      '--quiet',
      'test-app',
    ])

    result = runner.invoke(scaffold, [
      'service', 'create',
      '--app-dir-path', str(app_dir_path),
      '--context-dir-path', str(context_dir_path),
      '--quiet',
      'api',
    ])

    assert result.exit_code == 0

    config = _read_config(_context_config_path(context_dir_path))
    assert config['scaffold']['services'] == ['api']

  def test_appends_services_for_multiple_context_dirs(self, runner: CliRunner, tmp_path):
    app_dir_path = tmp_path / 'app'
    context_a = tmp_path / 'context-a'
    context_b = tmp_path / 'context-b'
    app_dir_path.mkdir()
    context_a.mkdir()
    context_b.mkdir()
    _prepare_app_dir(app_dir_path)

    runner.invoke(scaffold, [
      'app', 'create',
      '--app-dir-path', str(app_dir_path),
      '--context-dir-path', str(context_a),
      '--context-dir-path', str(context_b),
      '--quiet',
      'test-app',
    ])

    runner.invoke(scaffold, [
      'service', 'create',
      '--app-dir-path', str(app_dir_path),
      '--context-dir-path', str(context_a),
      '--quiet',
      'api',
    ])

    result = runner.invoke(scaffold, [
      'service', 'create',
      '--app-dir-path', str(app_dir_path),
      '--context-dir-path', str(context_a),
      '--context-dir-path', str(context_b),
      '--quiet',
      'assets',
    ])

    assert result.exit_code == 0

    assert _read_config(_context_config_path(context_a))['scaffold']['services'] == ['api', 'assets']
    assert _read_config(_context_config_path(context_b))['scaffold']['services'] == ['assets']

  def test_does_not_duplicate_service_on_rerun(self, runner: CliRunner, tmp_path):
    app_dir_path = tmp_path / 'app'
    context_dir_path = tmp_path / 'context'
    app_dir_path.mkdir()
    context_dir_path.mkdir()
    _prepare_app_dir(app_dir_path)

    runner.invoke(scaffold, [
      'app', 'create',
      '--app-dir-path', str(app_dir_path),
      '--context-dir-path', str(context_dir_path),
      '--quiet',
      'test-app',
    ])

    for _ in range(2):
      runner.invoke(scaffold, [
        'service', 'create',
        '--app-dir-path', str(app_dir_path),
        '--context-dir-path', str(context_dir_path),
        '--quiet',
        'api',
      ])

    config = _read_config(_context_config_path(context_dir_path))
    assert config['scaffold']['services'] == ['api']

  def test_context_dir_path_must_exist(self, runner: CliRunner, tmp_path):
    app_dir_path = tmp_path / 'app'
    context_dir_path = tmp_path / 'context'
    app_dir_path.mkdir()
    context_dir_path.mkdir()
    _prepare_app_dir(app_dir_path)

    runner.invoke(scaffold, [
      'app', 'create',
      '--app-dir-path', str(app_dir_path),
      '--quiet',
      'test-app',
    ])

    result = runner.invoke(scaffold, [
      'service', 'create',
      '--app-dir-path', str(app_dir_path),
      '--context-dir-path', str(tmp_path / 'missing-context'),
      '--quiet',
      'api',
    ])

    assert result.exit_code != 0


class TestContextServiceDefaults:
  def test_service_list_defaults_to_context_services(self, runner: CliRunner, tmp_path):
    app_dir_path = tmp_path / 'app'
    context_dir_path = tmp_path / 'context'
    _create_app_with_context(runner, app_dir_path, context_dir_path)
    _create_service(runner, app_dir_path, 'svc-api', context_dir_path)
    _create_service(runner, app_dir_path, 'svc-assets', context_dir_path)

    config = _read_config(_context_config_path(context_dir_path))
    config['scaffold']['services'] = ['svc-api']
    _write_config(_context_config_path(context_dir_path), config)

    result = runner.invoke(scaffold, [
      'service', 'list',
      '--app-dir-path', str(app_dir_path),
      '--context-dir-path', str(context_dir_path),
    ])

    assert result.exit_code == 0
    assert 'svc-api' in result.output
    assert 'svc-assets' not in result.output

  def test_service_list_explicit_service_overrides_context(self, runner: CliRunner, tmp_path):
    app_dir_path = tmp_path / 'app'
    context_dir_path = tmp_path / 'context'
    _create_app_with_context(runner, app_dir_path, context_dir_path)
    _create_service(runner, app_dir_path, 'svc-api', context_dir_path)
    _create_service(runner, app_dir_path, 'svc-assets', context_dir_path)

    config = _read_config(_context_config_path(context_dir_path))
    config['scaffold']['services'] = ['svc-api']
    _write_config(_context_config_path(context_dir_path), config)

    result = runner.invoke(scaffold, [
      'service', 'list',
      '--app-dir-path', str(app_dir_path),
      '--context-dir-path', str(context_dir_path),
      '--service', 'svc-assets',
    ])

    assert result.exit_code == 0
    assert 'svc-assets' in result.output
    assert 'svc-api' not in result.output

  def test_empty_context_services_lists_all(self, runner: CliRunner, tmp_path):
    app_dir_path = tmp_path / 'app'
    context_dir_path = tmp_path / 'context'
    _create_app_with_context(runner, app_dir_path, context_dir_path)
    _create_service(runner, app_dir_path, 'svc-api')
    _create_service(runner, app_dir_path, 'svc-assets')

    assert _read_config(_context_config_path(context_dir_path))['scaffold']['services'] == []

    result = runner.invoke(scaffold, [
      'service', 'list',
      '--app-dir-path', str(app_dir_path),
      '--context-dir-path', str(context_dir_path),
    ])

    assert result.exit_code == 0
    assert 'svc-api' in result.output
    assert 'svc-assets' in result.output


class TestScaffoldDescribe:
  def test_describe_with_context_config(self, runner: CliRunner, tmp_path):
    app_dir_path = tmp_path / 'app'
    context_dir_path = tmp_path / 'e2e'
    _create_app_with_context(runner, app_dir_path, context_dir_path)
    _create_service(runner, app_dir_path, 'svc-api', context_dir_path)

    result = runner.invoke(scaffold, [
      'describe',
      '--context-dir-path', str(context_dir_path),
    ])

    assert result.exit_code == 0
    assert str(app_dir_path) in result.output
    assert 'svc-api' in result.output
    assert 'test-app' in result.output

    data = json.loads(result.output)
    assert 'scaffold' in data['context_config']
    assert 'APP_NAME' in data['app_config']

  def test_describe_without_context_config(self, runner: CliRunner, tmp_path):
    app_dir_path = tmp_path / 'app'
    app_dir_path.mkdir()
    _prepare_app_dir(app_dir_path)

    create_result = runner.invoke(scaffold, [
      'app', 'create',
      '--app-dir-path', str(app_dir_path),
      '--quiet',
      'my-app',
    ])
    assert create_result.exit_code == 0

    result = runner.invoke(scaffold, [
      'describe',
      '--context-dir-path', str(app_dir_path),
    ])

    assert result.exit_code == 0
    assert str(app_dir_path) in result.output
    assert 'my-app' in result.output

    data = json.loads(result.output)
    assert 'context_config' not in data

  def test_describe_split_layout(self, runner: CliRunner, tmp_path):
    app_dir_path = tmp_path / 'app'
    context_dir_path = tmp_path / 'e2e'
    _create_app_with_context(runner, app_dir_path, context_dir_path)

    result = runner.invoke(scaffold, [
      'describe',
      '--context-dir-path', str(context_dir_path),
    ])

    assert result.exit_code == 0
    assert str(app_dir_path) in result.output
    assert os.path.relpath(str(app_dir_path), str(context_dir_path)) in result.output
