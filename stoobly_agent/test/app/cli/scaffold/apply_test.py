import json
import logging
import os
import shutil
import tempfile

import pytest
import yaml
from click.testing import CliRunner

from stoobly_agent.app.cli.scaffold.app import App
from stoobly_agent.app.cli.scaffold.apply_command import LOG_ID, sort_init_section_commands
from stoobly_agent.app.cli.scaffold.constants import SERVICES_NAMESPACE
from stoobly_agent.app.cli.scaffold.service import Service
from stoobly_agent.app.cli.scaffold.settings_init_manager import (
  SCAFFOLD_INIT_DELIMITER_BEGIN,
  SCAFFOLD_INIT_DELIMITER_END,
)
from stoobly_agent.app.cli.scaffold.templates.constants import CORE_BUILD_SERVICE_NAME, CUSTOM_INIT
from stoobly_agent.app.cli.scaffold_cli import scaffold
from stoobly_agent.config.app_data_dir import SERVICES_CONFIG_FILE_PATH, AppDataDir
from stoobly_agent.config.constants.env_vars import LOG_LEVEL
from stoobly_agent.config.data_dir import DATA_DIR_NAME, DataDir
from stoobly_agent.lib.logger import Logger
from stoobly_agent.test.test_helper import reset


class TestScaffoldApply:

  @pytest.fixture(scope='module', autouse=True)
  @classmethod
  def settings(cls):
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

  def test_nested_setting_rewrite_set_dry_run(self, runner: CliRunner, temp_dir: str):
    config_path = os.path.join(temp_dir, 'scaffold.yml')
    self._write_yaml(config_path, {
      'version': 1,
      'commands': [
        {
          'resource': 'setting',
          'action': 'rewrite set',
          'options': {
            'method': ['GET'],
            'mode': ['record'],
            'name': 'authorization',
            'pattern': '.*',
            'type': 'Header',
            'value': '',
            'workflow': ['record'],
          },
        },
      ],
    })

    result = runner.invoke(scaffold, ['apply', config_path, '--dry-run'])
    assert result.exit_code == 0, result.output
    combined = result.output + (result.stderr or '')
    assert 'would apply setting rewrite set' in combined

  def test_intercept_enable_dry_run(self, runner: CliRunner, temp_dir: str):
    config_path = os.path.join(temp_dir, 'scaffold.yml')
    self._write_yaml(config_path, {
      'version': 1,
      'commands': [
        {
          'resource': 'intercept',
          'action': 'enable',
          'options': {
            'workflow': ['develop', 'mock', 'record', 'test'],
          },
        },
      ],
    })

    result = runner.invoke(scaffold, ['apply', config_path, '--dry-run'])
    assert result.exit_code == 0, result.output
    combined = result.output + (result.stderr or '')
    assert 'would apply intercept enable' in combined

  def test_sort_init_section_commands_puts_enable_last(self):
    commands = [
      {'resource': 'app', 'action': 'create', 'options': {}},
      {'resource': 'intercept', 'action': 'enable', 'options': {}},
      {'resource': 'setting', 'action': 'rewrite set', 'options': {'name': 'a'}},
      {'resource': 'service', 'action': 'create', 'options': {}},
      {'resource': 'setting', 'action': 'rewrite set', 'options': {'name': 'b'}},
    ]

    sorted_commands = sort_init_section_commands(commands)

    assert [c['resource'] for c in sorted_commands] == ['app', 'setting', 'setting', 'service', 'intercept']
    assert sorted_commands[1]['action'] == 'rewrite set'
    assert sorted_commands[1]['options']['name'] == 'a'
    assert sorted_commands[2]['action'] == 'rewrite set'
    assert sorted_commands[2]['options']['name'] == 'b'
    assert sorted_commands[4]['action'] == 'enable'

  def test_apply_sorts_enable_last_and_overwrites_on_first_setting(self, runner: CliRunner, temp_dir: str):
    DataDir._instances = None
    AppDataDir._instance = None

    app_dir = os.path.join(temp_dir, 'overwrite-app')
    os.makedirs(os.path.join(app_dir, DATA_DIR_NAME, SERVICES_NAMESPACE), exist_ok=True)
    services_config = os.path.join(app_dir, DATA_DIR_NAME, SERVICES_CONFIG_FILE_PATH)
    os.makedirs(os.path.dirname(services_config), exist_ok=True)
    with open(services_config, 'w') as fp:
      fp.write('')

    init_path = os.path.join(
      app_dir, DATA_DIR_NAME, SERVICES_NAMESPACE, CORE_BUILD_SERVICE_NAME, 'record', CUSTOM_INIT
    )
    os.makedirs(os.path.dirname(init_path), exist_ok=True)
    with open(init_path, 'w') as fp:
      fp.write(
        "#! /bin/bash\n"
        f"{SCAFFOLD_INIT_DELIMITER_BEGIN}\n"
        "stoobly-agent setting filter set --action exclude --method GET --mode record --pattern '.*'\n"
        f"{SCAFFOLD_INIT_DELIMITER_END}\n"
        "\n# Add custom initialization here\n"
      )

    config_path = os.path.join(temp_dir, 'scaffold.yml')
    self._write_yaml(config_path, {
      'version': 1,
      'commands': [
        {
          'resource': 'intercept',
          'action': 'enable',
          'options': {
            'workflow': ['record'],
            'app_dir_path': app_dir,
          },
        },
        {
          'resource': 'setting',
          'action': 'rewrite set',
          'options': {
            'method': ['GET'],
            'mode': ['record'],
            'name': 'authorization',
            'pattern': '.*',
            'type': 'Header',
            'value': '',
            'workflow': ['record'],
            'app_dir_path': app_dir,
          },
        },
      ],
    })

    result = runner.invoke(scaffold, ['apply', config_path])
    assert result.exit_code == 0, result.output
    combined = result.output + (result.stderr or '')
    assert combined.index('applying setting rewrite set') < combined.index('applying intercept enable')

    with open(init_path) as fp:
      contents = fp.read()

    assert contents.count(SCAFFOLD_INIT_DELIMITER_BEGIN) == 1
    assert contents.count(SCAFFOLD_INIT_DELIMITER_END) == 1

    init_begin = contents.index(SCAFFOLD_INIT_DELIMITER_BEGIN)
    init_end = contents.index(SCAFFOLD_INIT_DELIMITER_END)
    init_block = contents[init_begin:init_end + len(SCAFFOLD_INIT_DELIMITER_END)]

    assert 'stoobly-agent setting rewrite set' in init_block
    assert 'stoobly-agent setting filter set' not in init_block
    assert 'stoobly-agent intercept enable' in init_block
    assert init_block.index('stoobly-agent setting rewrite set') < init_block.index('stoobly-agent intercept enable')

  def test_apply_clears_union_of_init_workflows_on_reapply(self, runner: CliRunner, temp_dir: str):
    """Setting steps may target only record while intercept enable targets all CORE_WORKFLOWS.

    Re-apply must clear the union so non-record workflows do not accumulate duplicate
    enable lines or keep stale init commands.
    """
    DataDir._instances = None
    AppDataDir._instance = None

    app_dir = os.path.join(temp_dir, 'union-clear-app')
    os.makedirs(os.path.join(app_dir, DATA_DIR_NAME, SERVICES_NAMESPACE), exist_ok=True)
    services_config = os.path.join(app_dir, DATA_DIR_NAME, SERVICES_CONFIG_FILE_PATH)
    os.makedirs(os.path.dirname(services_config), exist_ok=True)
    with open(services_config, 'w') as fp:
      fp.write('')

    stale_line = "stoobly-agent setting filter set --action exclude --method GET --mode record --pattern '.*'\n"
    init_paths = {}
    for workflow_name in ('record', 'mock'):
      init_path = os.path.join(
        app_dir, DATA_DIR_NAME, SERVICES_NAMESPACE, CORE_BUILD_SERVICE_NAME, workflow_name, CUSTOM_INIT
      )
      os.makedirs(os.path.dirname(init_path), exist_ok=True)
      with open(init_path, 'w') as fp:
        fp.write(
          "#! /bin/bash\n"
          f"{SCAFFOLD_INIT_DELIMITER_BEGIN}\n"
          f"{stale_line}"
          "stoobly-agent intercept enable\n"
          f"{SCAFFOLD_INIT_DELIMITER_END}\n"
          "\n# Add custom initialization here\n"
        )
      init_paths[workflow_name] = init_path

    config_path = os.path.join(temp_dir, 'scaffold.yml')
    self._write_yaml(config_path, {
      'version': 1,
      'commands': [
        {
          'resource': 'setting',
          'action': 'rewrite set',
          'options': {
            'method': ['GET'],
            'mode': ['record'],
            'name': 'authorization',
            'pattern': '.*',
            'type': 'Header',
            'value': '',
            'workflow': ['record'],
            'app_dir_path': app_dir,
          },
        },
        {
          'resource': 'intercept',
          'action': 'enable',
          'options': {
            'workflow': ['record', 'mock'],
            'app_dir_path': app_dir,
          },
        },
      ],
    })

    for _ in range(2):
      result = runner.invoke(scaffold, ['apply', config_path])
      assert result.exit_code == 0, result.output

    with open(init_paths['record']) as fp:
      record_contents = fp.read()
    with open(init_paths['mock']) as fp:
      mock_contents = fp.read()

    record_begin = record_contents.index(SCAFFOLD_INIT_DELIMITER_BEGIN)
    record_end = record_contents.index(SCAFFOLD_INIT_DELIMITER_END)
    record_block = record_contents[record_begin:record_end + len(SCAFFOLD_INIT_DELIMITER_END)]

    mock_begin = mock_contents.index(SCAFFOLD_INIT_DELIMITER_BEGIN)
    mock_end = mock_contents.index(SCAFFOLD_INIT_DELIMITER_END)
    mock_block = mock_contents[mock_begin:mock_end + len(SCAFFOLD_INIT_DELIMITER_END)]

    assert record_block.count('stoobly-agent intercept enable') == 1
    assert 'stoobly-agent setting rewrite set' in record_block
    assert 'stoobly-agent setting filter set' not in record_block

    assert mock_block.count('stoobly-agent intercept enable') == 1
    assert 'stoobly-agent setting filter set' not in mock_block
    assert 'stoobly-agent setting rewrite set' not in mock_block

  def test_incomplete_nested_action_is_group(self, runner: CliRunner, temp_dir: str):
    config_path = os.path.join(temp_dir, 'scaffold.yml')
    self._write_yaml(config_path, {
      'version': 1,
      'commands': [
        {
          'resource': 'setting',
          'action': 'rewrite',
          'options': {},
        },
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
