import json
import logging
import os
import shutil
import tempfile

import pytest
import yaml
from click.testing import CliRunner

from stoobly_agent.app.cli.scaffold.app import App
from stoobly_agent.app.cli.scaffold.apply_command import LOG_ID
from stoobly_agent.app.cli.scaffold.constants import SERVICES_NAMESPACE
from stoobly_agent.app.cli.scaffold.service import Service
from stoobly_agent.app.cli.scaffold_cli import scaffold
from stoobly_agent.config.constants.env_vars import LOG_LEVEL
from stoobly_agent.config.data_dir import DATA_DIR_NAME, DataDir
from stoobly_agent.lib.logger import Logger
from stoobly_agent.test.test_helper import reset


class TestScaffoldApply:

  @pytest.fixture(scope='module', autouse=True)
  def settings(self):
    return reset()

  @pytest.fixture(autouse=True)
  def reset_apply_logger(self):
    # Other CLI tests (e.g. request replay) leave LOG_LEVEL=warning in the process env.
    os.environ.pop(LOG_LEVEL, None)
    # Logger caches StreamHandlers bound to sys.stderr; clear between CliRunner invokes.
    if LOG_ID in Logger._instances:
      log = Logger._instances.pop(LOG_ID)
      for handler in list(log.handlers):
        log.removeHandler(handler)
      log.setLevel(logging.NOTSET)

  @pytest.fixture
  def runner(self):
    return CliRunner()

  @pytest.fixture
  def temp_dir(self):
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)

  def _write_yaml(self, path, data):
    with open(path, 'w') as fp:
      yaml.dump(data, fp)

  def _write_json(self, path, data):
    with open(path, 'w') as fp:
      json.dump(data, fp)

  def test_help_loads(self, runner: CliRunner):
    result = runner.invoke(scaffold, ['apply', '--help'])
    assert result.exit_code == 0
    assert 'PATH' in result.output or 'path' in result.output.lower()
    assert '--dry-run' in result.output
    assert '--format' in result.output
    # PATH is optional; Click marks optional arguments with brackets.
    assert '[PATH]' in result.output

  def test_omitted_path_uses_data_dir_scaffold_file(self, runner: CliRunner):
    config_path = DataDir.instance().scaffold_file_path
    self._write_yaml(config_path, {
      'version': 1,
      'commands': [
        {
          'resource': 'app',
          'action': 'create',
          'options': {
            'app_name': 'default-path-app',
            'quiet': True,
            'runtime': 'local',
          },
        },
      ],
    })

    try:
      result = runner.invoke(scaffold, ['apply', '--dry-run'])
      assert result.exit_code == 0, result.output
      combined = result.output + (result.stderr or '')
      assert 'would apply app create default-path-app' in combined
    finally:
      if os.path.exists(config_path):
        os.remove(config_path)

  def test_omitted_path_missing_default_file(self, runner: CliRunner):
    config_path = DataDir.instance().scaffold_file_path
    if os.path.exists(config_path):
      os.remove(config_path)

    result = runner.invoke(scaffold, ['apply'])
    assert result.exit_code != 0

  def test_happy_path_app_and_service_create(self, runner: CliRunner, temp_dir: str):
    app_dir_path = os.path.join(temp_dir, 'my-app')
    os.makedirs(app_dir_path, exist_ok=True)
    os.makedirs(os.path.join(app_dir_path, DATA_DIR_NAME), exist_ok=True)
    docker_socket_path = os.path.join(temp_dir, 'docker.sock')
    open(docker_socket_path, 'a').close()

    config_path = os.path.join(temp_dir, 'scaffold.yml')
    self._write_yaml(config_path, {
      'version': 1,
      'commands': [
        {
          'resource': 'app',
          'action': 'create',
          'options': {
            'app_name': 'my-app',
            'app_dir_path': app_dir_path,
            'docker_socket_path': docker_socket_path,
            'quiet': True,
            'runtime': 'local',
          },
        },
        {
          'resource': 'service',
          'action': 'create',
          'options': {
            'service_name': 'api',
            'app_dir_path': app_dir_path,
            'hostname': 'api.example.com',
            'scheme': 'https',
            'port': 443,
            'quiet': True,
          },
        },
      ],
    })

    result = runner.invoke(scaffold, ['apply', config_path])
    assert result.exit_code == 0, result.output
    combined = result.output + (result.stderr or '')
    assert 'applying app create my-app' in combined
    assert 'applying service create api' in combined
    assert '--hostname' not in combined
    assert '--app-dir-path' not in combined

    app = App(app_dir_path)
    service = Service('api', app)
    assert os.path.exists(service.dir_path)
    assert os.path.exists(os.path.join(app.scaffold_namespace_path))

  def test_dry_run_does_not_invoke(self, runner: CliRunner, temp_dir: str):
    app_dir_path = os.path.join(temp_dir, 'dry-run-app')
    os.makedirs(app_dir_path, exist_ok=True)
    os.makedirs(os.path.join(app_dir_path, DATA_DIR_NAME), exist_ok=True)
    docker_socket_path = os.path.join(temp_dir, 'docker.sock')
    open(docker_socket_path, 'a').close()

    config_path = os.path.join(temp_dir, 'scaffold.yml')
    self._write_yaml(config_path, {
      'version': 1,
      'commands': [
        {
          'resource': 'app',
          'action': 'create',
          'options': {
            'app_name': 'dry-run-app',
            'app_dir_path': app_dir_path,
            'docker_socket_path': docker_socket_path,
            'quiet': True,
            'runtime': 'local',
          },
        },
        {
          'resource': 'service',
          'action': 'create',
          'options': {
            'service_name': 'api',
            'app_dir_path': app_dir_path,
            'hostname': 'api.example.com',
            'scheme': 'https',
            'port': 443,
            'quiet': True,
          },
        },
      ],
    })

    result = runner.invoke(scaffold, ['apply', '--dry-run', config_path])
    assert result.exit_code == 0, result.output
    combined = result.output + (result.stderr or '')
    assert 'would apply app create dry-run-app' in combined
    assert 'would apply service create api' in combined
    assert 'applying ' not in combined

    assert not os.path.exists(os.path.join(app_dir_path, DATA_DIR_NAME, SERVICES_NAMESPACE))
    assert not os.path.exists(os.path.join(app_dir_path, DATA_DIR_NAME, SERVICES_NAMESPACE, 'api'))

  def test_format_json(self, runner: CliRunner, temp_dir: str):
    app_dir_path = os.path.join(temp_dir, 'json-app')
    os.makedirs(app_dir_path, exist_ok=True)
    os.makedirs(os.path.join(app_dir_path, DATA_DIR_NAME), exist_ok=True)
    docker_socket_path = os.path.join(temp_dir, 'docker.sock')
    open(docker_socket_path, 'a').close()

    config_path = os.path.join(temp_dir, 'scaffold.json')
    self._write_json(config_path, {
      'version': 1,
      'commands': [
        {
          'resource': 'app',
          'action': 'create',
          'options': {
            'app_name': 'json-app',
            'app_dir_path': app_dir_path,
            'docker_socket_path': docker_socket_path,
            'quiet': True,
            'runtime': 'local',
          },
        },
      ],
    })

    result = runner.invoke(scaffold, ['apply', '--format', 'json', config_path])
    assert result.exit_code == 0, result.output
    assert os.path.exists(os.path.join(app_dir_path, DATA_DIR_NAME, SERVICES_NAMESPACE))

  def test_missing_version(self, runner: CliRunner, temp_dir: str):
    config_path = os.path.join(temp_dir, 'scaffold.yml')
    self._write_yaml(config_path, {
      'commands': [
        {'resource': 'app', 'action': 'create', 'options': {}},
      ],
    })

    result = runner.invoke(scaffold, ['apply', config_path])
    assert result.exit_code != 0
    assert 'version' in result.output.lower() or 'version' in (result.stderr or '').lower()

  def test_unsupported_version(self, runner: CliRunner, temp_dir: str):
    config_path = os.path.join(temp_dir, 'scaffold.yml')
    self._write_yaml(config_path, {
      'version': 99,
      'commands': [
        {'resource': 'app', 'action': 'create', 'options': {}},
      ],
    })

    result = runner.invoke(scaffold, ['apply', config_path])
    assert result.exit_code != 0
    combined = result.output + (result.stderr or '')
    assert 'Unsupported version' in combined or 'unsupported version' in combined.lower()

  def test_missing_commands(self, runner: CliRunner, temp_dir: str):
    config_path = os.path.join(temp_dir, 'scaffold.yml')
    self._write_yaml(config_path, {'version': 1})

    result = runner.invoke(scaffold, ['apply', config_path])
    assert result.exit_code != 0
    combined = result.output + (result.stderr or '')
    assert 'commands' in combined.lower()

  def test_missing_resource(self, runner: CliRunner, temp_dir: str):
    config_path = os.path.join(temp_dir, 'scaffold.yml')
    self._write_yaml(config_path, {
      'version': 1,
      'commands': [
        {'action': 'create', 'options': {}},
      ],
    })

    result = runner.invoke(scaffold, ['apply', config_path])
    assert result.exit_code != 0
    combined = result.output + (result.stderr or '')
    assert 'resource' in combined.lower()

  def test_unknown_resource(self, runner: CliRunner, temp_dir: str):
    config_path = os.path.join(temp_dir, 'scaffold.yml')
    self._write_yaml(config_path, {
      'version': 1,
      'commands': [
        {'resource': 'not-a-resource', 'action': 'create', 'options': {}},
      ],
    })

    result = runner.invoke(scaffold, ['apply', config_path])
    assert result.exit_code != 0
    combined = result.output + (result.stderr or '')
    assert 'Unknown resource' in combined

  def test_unknown_action(self, runner: CliRunner, temp_dir: str):
    config_path = os.path.join(temp_dir, 'scaffold.yml')
    self._write_yaml(config_path, {
      'version': 1,
      'commands': [
        {'resource': 'app', 'action': 'not-an-action', 'options': {}},
      ],
    })

    result = runner.invoke(scaffold, ['apply', config_path])
    assert result.exit_code != 0
    combined = result.output + (result.stderr or '')
    assert 'Unknown action' in combined

  def test_unknown_option(self, runner: CliRunner, temp_dir: str):
    config_path = os.path.join(temp_dir, 'scaffold.yml')
    self._write_yaml(config_path, {
      'version': 1,
      'commands': [
        {
          'resource': 'app',
          'action': 'create',
          'options': {
            'app_name': 'my-app',
            'not_a_real_option': True,
          },
        },
      ],
    })

    result = runner.invoke(scaffold, ['apply', config_path])
    assert result.exit_code != 0
    combined = result.output + (result.stderr or '')
    assert 'Unknown options' in combined
    assert 'not_a_real_option' in combined

  def test_invalid_accepted_value(self, runner: CliRunner, temp_dir: str):
    config_path = os.path.join(temp_dir, 'scaffold.yml')
    self._write_yaml(config_path, {
      'version': 1,
      'commands': [
        {
          'resource': 'app',
          'action': 'create',
          'options': {
            'app_name': 'my-app',
            'runtime': 'not-a-runtime',
          },
        },
      ],
    })

    result = runner.invoke(scaffold, ['apply', config_path])
    assert result.exit_code != 0
    combined = result.output + (result.stderr or '')
    assert 'Accepted values' in combined or 'accepted values' in combined.lower()
    assert 'not-a-runtime' in combined

  def test_missing_required_argument(self, runner: CliRunner, temp_dir: str):
    config_path = os.path.join(temp_dir, 'scaffold.yml')
    self._write_yaml(config_path, {
      'version': 1,
      'commands': [
        {
          'resource': 'app',
          'action': 'create',
          'options': {
            'quiet': True,
          },
        },
      ],
    })

    result = runner.invoke(scaffold, ['apply', config_path])
    assert result.exit_code != 0
    combined = result.output + (result.stderr or '')
    assert 'app_name' in combined
    assert 'missing required' in combined.lower()

  def test_action_that_is_group(self, runner: CliRunner, temp_dir: str):
    config_path = os.path.join(temp_dir, 'scaffold.yml')
    self._write_yaml(config_path, {
      'version': 1,
      'commands': [
        {'resource': 'request', 'action': 'logs', 'options': {}},
      ],
    })

    result = runner.invoke(scaffold, ['apply', config_path])
    assert result.exit_code != 0
    combined = result.output + (result.stderr or '')
    assert 'is a group' in combined

  def test_missing_file(self, runner: CliRunner, temp_dir: str):
    missing = os.path.join(temp_dir, 'does-not-exist.yml')
    result = runner.invoke(scaffold, ['apply', missing])
    assert result.exit_code != 0

  def test_invoked_command_usage_shows_resource_path(self, runner: CliRunner, temp_dir: str):
    missing_context = os.path.join(temp_dir, 'missing-context')
    config_path = os.path.join(temp_dir, 'scaffold.yml')
    self._write_yaml(config_path, {
      'version': 1,
      'commands': [
        {
          'resource': 'app',
          'action': 'create',
          'options': {
            'app_name': 'my-app',
            'app_dir_path': temp_dir,
            'context_dir_path': [missing_context],
          },
        },
      ],
    })

    result = runner.invoke(scaffold, ['apply', config_path])
    assert result.exit_code != 0
    combined = result.output + (result.stderr or '')
    assert 'scaffold app create' in combined
    # Usage must not nest under apply (e.g. "scaffold apply PATH create")
    assert 'apply PATH create' not in combined
    assert 'context-dir-path' in combined
