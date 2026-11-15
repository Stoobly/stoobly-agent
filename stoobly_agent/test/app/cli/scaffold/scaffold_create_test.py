import os
import shutil
import tempfile

import pytest
import yaml
from click.testing import CliRunner

from stoobly_agent.app.cli.scaffold.constants import CORE_WORKFLOWS
from stoobly_agent.app.cli.scaffold_cli import scaffold
from stoobly_agent.config.data_dir import DATA_DIR_NAME, DataDir
from stoobly_agent.test.test_helper import reset


class TestScaffoldCreate:

  @pytest.fixture(scope='module', autouse=True)
  @classmethod
  def settings(cls):
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
  def temp_dir(self):
    temp_dir = tempfile.mkdtemp()
    cwd = os.getcwd()
    os.chdir(temp_dir)
    DataDir._instances = None
    yield temp_dir
    os.chdir(cwd)
    DataDir._instances = None
    shutil.rmtree(temp_dir)

  def test_help_loads(self, runner: CliRunner):
    result = runner.invoke(scaffold, ['create', '--help'])
    assert result.exit_code == 0
    assert 'scaffold.yml' in result.output

  def test_creates_scaffold_yml_when_missing(self, runner: CliRunner, temp_dir: str):
    expected_path = os.path.join(temp_dir, DATA_DIR_NAME, 'scaffold.yml')
    assert not os.path.exists(expected_path)

    result = runner.invoke(scaffold, ['create'])
    assert result.exit_code == 0, result.output
    assert os.path.exists(expected_path)
    assert f"Created {expected_path}" in result.output
    assert 'Review the file, then run: stoobly-agent scaffold apply' in result.output

    with open(expected_path) as fp:
      data = yaml.safe_load(fp)

    assert data['version'] == 1
    commands = data['commands']
    assert len(commands) == 5

    app_step = commands[0]
    assert app_step['resource'] == 'app'
    assert app_step['action'] == 'create'
    assert app_step['options']['app_name'] == os.path.basename(temp_dir)

    service_step = commands[1]
    assert service_step['resource'] == 'service'
    assert service_step['action'] == 'create'
    assert service_step['options'] == {
      'service_name': 'backend',
      'hostname': 'local.api',
      'scheme': 'http',
      'port': 80,
      'local': True,
    }

    rewrite_steps = commands[2:4]
    assert [step['resource'] for step in rewrite_steps] == ['setting', 'setting']
    assert [step['action'] for step in rewrite_steps] == ['rewrite set', 'rewrite set']
    assert [step['options']['name'] for step in rewrite_steps] == ['authorization', 'cookie']

    for step in rewrite_steps:
      options = step['options']
      assert options['method'] == ['GET', 'POST', 'OPTIONS', 'PATCH', 'PUT', 'DELETE']
      assert options['mode'] == ['record']
      assert options['pattern'] == '.*'
      assert options['type'] == 'Header'
      assert options['value'] == ''
      assert options['workflow'] == ['record']

    intercept_step = commands[4]
    assert intercept_step['resource'] == 'setting'
    assert intercept_step['action'] == 'intercept enable'
    assert intercept_step['options']['workflow'] == list(CORE_WORKFLOWS)

  def test_errors_when_scaffold_yml_exists(self, runner: CliRunner, temp_dir: str):
    expected_path = os.path.join(temp_dir, DATA_DIR_NAME, 'scaffold.yml')
    os.makedirs(os.path.dirname(expected_path), exist_ok=True)
    with open(expected_path, 'w') as fp:
      fp.write('version: 1\ncommands: []\n')

    result = runner.invoke(scaffold, ['create'])
    assert result.exit_code != 0
    combined = result.output + (result.stderr or '')
    assert 'already exists' in combined
    assert expected_path in combined
