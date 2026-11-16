import os

import pytest
import yaml
from click.testing import CliRunner

from stoobly_agent import COMMAND
from stoobly_agent.app.cli.scaffold_cli import scaffold
from stoobly_agent.config.data_dir import DATA_DIR_NAME, DataDir
from stoobly_agent.test.test_helper import reset


def _scaffold_path(app_dir: str) -> str:
  return os.path.join(app_dir, DATA_DIR_NAME, 'scaffold.yml')


def _read_scaffold(path: str) -> dict:
  with open(path) as fp:
    return yaml.safe_load(fp)


def _assert_scaffold_yml_updated_message(output: str, scaffold_path: str):
  relative_path = os.path.relpath(scaffold_path)
  expected = (
    f"Updated {relative_path}, run `{COMMAND} scaffold apply {relative_path}` "
    "to apply the changes"
  )
  assert expected in output


def _create_app(runner: CliRunner, app_dir: str, *extra_args):
  os.makedirs(app_dir, exist_ok=True)
  os.makedirs(os.path.join(app_dir, DATA_DIR_NAME), exist_ok=True)
  docker_socket_path = os.path.join(app_dir, 'docker.sock')
  if not os.path.exists(docker_socket_path):
    open(docker_socket_path, 'a').close()
  result = runner.invoke(scaffold, [
    'app', 'create',
    '--app-dir-path', app_dir,
    '--docker-socket-path', docker_socket_path,
    '--quiet',
    *extra_args,
    'test-app',
  ])
  assert result.exit_code == 0, result.output
  return result


def _create_service(runner: CliRunner, app_dir: str, service_name: str, *extra_args):
  result = runner.invoke(scaffold, [
    'service', 'create',
    '--app-dir-path', app_dir,
    '--quiet',
    *extra_args,
    service_name,
  ])
  assert result.exit_code == 0, result.output
  return result


def _apply_scaffold(runner: CliRunner, scaffold_path: str):
  result = runner.invoke(scaffold, ['apply', scaffold_path])
  assert result.exit_code == 0, result.output
  return result


class TestScaffoldSaveCli:
  @pytest.fixture(autouse=True)
  def settings(self):
    return reset()

  @pytest.fixture(autouse=True)
  def isolate_data_dir_cache(self):
    DataDir._instances = None
    yield
    DataDir._instances = None

  @pytest.fixture
  def runner(self):
    return CliRunner()

  @pytest.fixture
  def app_dir(self, tmp_path):
    return os.path.join(str(tmp_path), 'test-app')

  def test_app_create_saves_by_default(self, runner: CliRunner, app_dir: str):
    scaffold_path = _scaffold_path(app_dir)
    assert not os.path.exists(scaffold_path)

    result = _create_app(runner, app_dir)
    assert os.path.exists(scaffold_path)
    _assert_scaffold_yml_updated_message(result.output, scaffold_path)
    assert not os.path.exists(os.path.join(app_dir, DATA_DIR_NAME, 'services'))

    data = _read_scaffold(scaffold_path)
    assert data['version'] == 1
    assert len(data['commands']) == 1
    step = data['commands'][0]
    assert step['resource'] == 'app'
    assert step['action'] == 'create'
    assert step['options']['app_name'] == 'test-app'
    assert step['options']['app_dir_path'] == app_dir
    assert 'apply' not in step['options']
    assert 'save' not in step['options']

  def test_app_create_apply_creates_without_save(self, runner: CliRunner, app_dir: str):
    scaffold_path = _scaffold_path(app_dir)

    result = _create_app(runner, app_dir, '--apply')
    assert os.path.exists(os.path.join(app_dir, DATA_DIR_NAME, 'services'))
    assert not os.path.exists(scaffold_path)
    assert 'Updated' not in result.output or 'scaffold.yml' not in result.output

  def test_service_create_saves_by_default(self, runner: CliRunner, app_dir: str):
    _create_app(runner, app_dir, '--apply')
    scaffold_path = _scaffold_path(app_dir)
    assert not os.path.exists(scaffold_path)

    result = _create_service(
      runner, app_dir, 'api',
      '--hostname', 'api.example.com',
      '--scheme', 'https',
      '--port', '443',
    )
    _assert_scaffold_yml_updated_message(result.output, scaffold_path)
    assert not os.path.exists(os.path.join(app_dir, DATA_DIR_NAME, 'services', 'api'))

    data = _read_scaffold(scaffold_path)
    assert len(data['commands']) == 1
    step = data['commands'][0]
    assert step['resource'] == 'service'
    assert step['action'] == 'create'
    assert step['options']['service_name'] == 'api'
    assert step['options']['hostname'] == 'api.example.com'
    assert 'apply' not in step['options']

  def test_service_create_saves_without_applied_scaffold(self, runner: CliRunner, app_dir: str):
    # Declare-only app create leaves no services/.config.yml; service create must
    # still pin scaffold.yml to app_dir instead of falling back to cwd data dir.
    _create_app(runner, app_dir)
    scaffold_path = _scaffold_path(app_dir)
    services_path = os.path.join(app_dir, DATA_DIR_NAME, 'services')
    assert os.path.exists(scaffold_path)
    assert not os.path.exists(services_path)

    result = _create_service(
      runner, app_dir, 'api',
      '--hostname', 'api.example.com',
      '--scheme', 'https',
      '--port', '443',
    )
    _assert_scaffold_yml_updated_message(result.output, scaffold_path)
    assert not os.path.exists(services_path)

    data = _read_scaffold(scaffold_path)
    assert len(data['commands']) == 2
    step = data['commands'][1]
    assert step['resource'] == 'service'
    assert step['action'] == 'create'
    assert step['options']['service_name'] == 'api'
    assert step['options']['hostname'] == 'api.example.com'

  def test_service_create_apply_creates_without_save(self, runner: CliRunner, app_dir: str):
    _create_app(runner, app_dir, '--apply')
    scaffold_path = _scaffold_path(app_dir)

    _create_service(
      runner, app_dir, 'api',
      '--hostname', 'api.example.com',
      '--scheme', 'https',
      '--port', '443',
      '--apply',
    )
    assert os.path.exists(os.path.join(app_dir, DATA_DIR_NAME, 'services', 'api'))
    assert not os.path.exists(scaffold_path)

  def test_service_update_merges_into_create(self, runner: CliRunner, app_dir: str):
    _create_app(runner, app_dir, '--apply')
    _create_service(
      runner, app_dir, 'api',
      '--hostname', 'api.example.com',
      '--scheme', 'https',
      '--port', '443',
    )
    scaffold_path = _scaffold_path(app_dir)
    _apply_scaffold(runner, scaffold_path)

    result = runner.invoke(scaffold, [
      'service', 'update',
      '--app-dir-path', app_dir,
      '--port', '8443',
      'api',
    ])
    assert result.exit_code == 0, result.output
    # service update always applies on disk; still reports scaffold.yml update
    assert f'Updated {scaffold_path}' in result.output or os.path.relpath(scaffold_path) in result.output

    data = _read_scaffold(scaffold_path)
    assert len(data['commands']) == 1
    step = data['commands'][0]
    assert step['resource'] == 'service'
    assert step['action'] == 'create'
    assert step['options']['service_name'] == 'api'
    assert step['options']['hostname'] == 'api.example.com'
    assert step['options']['scheme'] == 'https'
    assert step['options']['port'] == 8443
    assert 'apply' not in step['options']
    assert 'service_path' not in step['options']
    assert 'name' not in step['options']

  def test_service_update_without_create_appends_create(self, runner: CliRunner, app_dir: str):
    _create_app(runner, app_dir, '--apply')
    _create_service(
      runner, app_dir, 'api',
      '--hostname', 'api.example.com',
      '--scheme', 'https',
      '--port', '443',
      '--apply',
    )
    scaffold_path = _scaffold_path(app_dir)
    assert not os.path.exists(scaffold_path)

    result = runner.invoke(scaffold, [
      'service', 'update',
      '--app-dir-path', app_dir,
      '--port', '8443',
      'api',
    ])
    assert result.exit_code == 0, result.output
    assert os.path.exists(scaffold_path)

    data = _read_scaffold(scaffold_path)
    assert len(data['commands']) == 1
    step = data['commands'][0]
    assert step['resource'] == 'service'
    assert step['action'] == 'create'
    assert step['options']['service_name'] == 'api'
    assert step['options']['port'] == 8443

  def test_service_update_rename_updates_create_name(self, runner: CliRunner, app_dir: str):
    _create_app(runner, app_dir, '--apply')
    _create_service(
      runner, app_dir, 'api',
      '--hostname', 'api.example.com',
      '--scheme', 'https',
      '--port', '443',
    )
    scaffold_path = _scaffold_path(app_dir)
    _apply_scaffold(runner, scaffold_path)

    result = runner.invoke(scaffold, [
      'service', 'update',
      '--app-dir-path', app_dir,
      '--name', 'api-v2',
      'api',
    ])
    assert result.exit_code == 0, result.output

    data = _read_scaffold(scaffold_path)
    assert len(data['commands']) == 1
    step = data['commands'][0]
    assert step['action'] == 'create'
    assert step['options']['service_name'] == 'api-v2'
    assert step['options']['hostname'] == 'api.example.com'
    assert 'name' not in step['options']

  def test_service_delete_removes_matching_create(self, runner: CliRunner, app_dir: str):
    _create_app(runner, app_dir, '--apply')
    _create_service(
      runner, app_dir, 'api',
      '--hostname', 'api.example.com',
      '--scheme', 'https',
      '--port', '443',
    )
    scaffold_path = _scaffold_path(app_dir)
    _apply_scaffold(runner, scaffold_path)

    result = runner.invoke(scaffold, [
      'service', 'delete',
      '--app-dir-path', app_dir,
      'api',
    ])
    assert result.exit_code == 0, result.output
    assert f'Updated {scaffold_path}' in result.output or os.path.relpath(scaffold_path) in result.output
    assert not os.path.exists(os.path.join(app_dir, DATA_DIR_NAME, 'services', 'api'))

    data = _read_scaffold(scaffold_path)
    assert data['commands'] == []

  def test_workflow_create_saves_by_default(self, runner: CliRunner, app_dir: str):
    _create_app(runner, app_dir, '--apply')
    scaffold_path = _scaffold_path(app_dir)

    result = runner.invoke(scaffold, [
      'workflow', 'create',
      '--app-dir-path', app_dir,
      '--service', 'api',
      '--template', 'mock',
      '--quiet',
      'ci',
    ])
    assert result.exit_code == 0, result.output

    data = _read_scaffold(scaffold_path)
    assert len(data['commands']) == 1
    step = data['commands'][0]
    assert step['resource'] == 'workflow'
    assert step['action'] == 'create'
    assert step['options']['workflow_name'] == 'ci'
    assert step['options']['template'] == 'mock'
    assert step['options']['service'] == ['api']
    assert 'apply' not in step['options']

  def test_workflow_create_saves_without_applied_scaffold(self, runner: CliRunner, app_dir: str):
    _create_app(runner, app_dir)
    scaffold_path = _scaffold_path(app_dir)
    services_path = os.path.join(app_dir, DATA_DIR_NAME, 'services')
    assert os.path.exists(scaffold_path)
    assert not os.path.exists(services_path)

    result = runner.invoke(scaffold, [
      'workflow', 'create',
      '--app-dir-path', app_dir,
      '--service', 'api',
      '--template', 'mock',
      '--quiet',
      'ci',
    ])
    assert result.exit_code == 0, result.output
    assert not os.path.exists(services_path)

    data = _read_scaffold(scaffold_path)
    assert len(data['commands']) == 2
    step = data['commands'][1]
    assert step['resource'] == 'workflow'
    assert step['action'] == 'create'
    assert step['options']['workflow_name'] == 'ci'
    assert step['options']['template'] == 'mock'
    assert step['options']['service'] == ['api']

  def test_service_create_upserts_same_name(self, runner: CliRunner, app_dir: str):
    _create_app(runner, app_dir, '--apply')
    scaffold_path = _scaffold_path(app_dir)

    _create_service(
      runner, app_dir, 'api',
      '--hostname', 'api.example.com',
      '--scheme', 'https',
      '--port', '443',
    )
    result = _create_service(
      runner, app_dir, 'api',
      '--hostname', 'api.updated.com',
      '--scheme', 'https',
      '--port', '8443',
    )
    assert result.exit_code == 0, result.output

    data = _read_scaffold(scaffold_path)
    assert len(data['commands']) == 1
    step = data['commands'][0]
    assert step['resource'] == 'service'
    assert step['action'] == 'create'
    assert step['options']['service_name'] == 'api'
    assert step['options']['hostname'] == 'api.updated.com'
    assert step['options']['port'] == 8443

  def test_scaffold_apply_does_not_reappend(self, runner: CliRunner, tmp_path):
    app_dir = os.path.join(str(tmp_path), 'apply-app')
    _create_app(runner, app_dir, '--apply')

    config_path = os.path.join(str(tmp_path), 'scaffold.yml')
    with open(config_path, 'w') as fp:
      yaml.safe_dump({
        'version': 1,
        'commands': [
          {
            'resource': 'service',
            'action': 'create',
            'options': {
              'service_name': 'api',
              'app_dir_path': app_dir,
              'hostname': 'api.example.com',
              'scheme': 'https',
              'port': 443,
              'quiet': True,
            },
          },
        ],
      }, fp, default_flow_style=False, sort_keys=False)

    before = _read_scaffold(config_path)
    result = runner.invoke(scaffold, ['apply', config_path])
    assert result.exit_code == 0, result.output

    after = _read_scaffold(config_path)
    assert after == before
    assert len(after['commands']) == 1

    app_scaffold = _scaffold_path(app_dir)
    assert not os.path.exists(app_scaffold)
