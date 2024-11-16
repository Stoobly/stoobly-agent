import os
from pathlib import Path
import pathlib
import pdb
import shutil
import tempfile

from click.testing import CliRunner
import docker
import pytest

from stoobly_agent.app.cli import scaffold
from stoobly_agent.app.cli.scaffold.app import App
from stoobly_agent.app.cli.scaffold.constants import (
  WORKFLOW_RECORD_TYPE,
  WORKFLOW_TEST_TYPE,
)
from stoobly_agent.app.cli.scaffold.constants import DOCKER_NAMESPACE
from stoobly_agent.app.cli.scaffold.core_components_composite import (
  CoreComponentsComposite,
)
from stoobly_agent.app.cli.scaffold.service_composite import ServiceComposite
from stoobly_agent.app.cli.scaffold.service_validate_command import (
  ServiceValidateCommand,
)
from stoobly_agent.app.cli.scaffold.workflow_validate_command import (
  WorkflowValidateCommand,
)
from stoobly_agent.config.data_dir import DATA_DIR_NAME


class TestScaffoldE2e():
  @pytest.fixture(scope='module')
  def runner(self):
    return CliRunner()

  @pytest.fixture(scope='class')
  def docker_client(self):
    yield docker.from_env()

  @pytest.fixture(scope='class')
  def app_name(self):
    yield "0.0.1"

  @pytest.fixture(scope='class', autouse=True)
  def app_dir_path(self, docker_client, app_name):
    temp_dir = tempfile.TemporaryDirectory()
    yield temp_dir.name
    temp_dir.cleanup()

    temp_dir_name = os.path.basename(temp_dir.name)
    docker_network = docker_client.networks.get(temp_dir_name)
    docker_network.remove()

  @pytest.fixture(scope='class')
  def mock_data_directory_path(self):
    return Path(__file__).parent.parent.parent.parent / 'mock_data'
  
  @pytest.fixture(scope='class')
  def local_service_mock_docker_compose_path(self, mock_data_directory_path):
    path = mock_data_directory_path / "scaffold" / "docker-compose-local-service.yml"
    return path

  @pytest.fixture(scope='class')
  def hostname(self):
    yield "http.badssl.com"
  
  @pytest.fixture(scope='class')
  def external_service_name(self):
    yield "external-service"

  @pytest.fixture(scope='class')
  def local_hostname(self):
    yield "my-httpbin.com"

  @pytest.fixture(scope='class')
  def local_service_name(self):
    yield "my-httpbin"

  
  class TestRecordWorkflow():
    @pytest.fixture(scope='class', autouse=True)
    def target_workflow_name(self):
      yield WORKFLOW_RECORD_TYPE

    @pytest.fixture(scope='class')
    def core_components_composite(self, target_workflow_name):
      yield CoreComponentsComposite(target_workflow_name=target_workflow_name)
    
    @pytest.fixture(scope='class')
    def external_service_composite(self, app_dir_path, target_workflow_name, external_service_name, hostname):
      yield ServiceComposite(app_dir_path=app_dir_path, target_workflow_name=target_workflow_name, service_name=external_service_name, hostname=hostname)

    @pytest.fixture(scope='class')
    def local_service_composite(self, app_dir_path, target_workflow_name, local_service_name, local_hostname):
      yield ServiceComposite(app_dir_path=app_dir_path, target_workflow_name=target_workflow_name, service_name=local_service_name, hostname=local_hostname)

    @pytest.fixture(scope='class', autouse=True)
    def setup_composites(self, core_components_composite, external_service_composite, local_service_composite):
      self.core_components_composite = core_components_composite
      self.external_service_composite = external_service_composite
      self.local_service_composite = local_service_composite

    @pytest.fixture(scope="class", autouse=True)
    def create_scaffold_setup(self, runner, app_dir_path, app_name, target_workflow_name, external_service_composite, local_service_composite, local_service_mock_docker_compose_path):
      TestScaffoldE2e.cli_app_create(runner, app_dir_path, app_name)

      # Create external user defined service
      TestScaffoldE2e.cli_service_create(runner, app_dir_path, external_service_composite.hostname, external_service_composite.service_name)

      # Create local user defined service
      TestScaffoldE2e.cli_service_create(runner, app_dir_path, local_service_composite.hostname, local_service_composite.service_name)

      # Validate docker-compose path exists
      destination_path = Path(local_service_composite.docker_compose_path)
      assert destination_path.is_file()
      # Add user defined Docker Compose file for the local service
      shutil.copyfile(local_service_mock_docker_compose_path, destination_path)

      # Record workflow doesn't have a fixtures folder

      TestScaffoldE2e.cli_workflow_run(runner, app_dir_path, target_workflow_name)

    @pytest.fixture(scope="class", autouse=True)
    def cleanup_after_all(self, runner, app_dir_path, target_workflow_name):
      yield
      TestScaffoldE2e.cli_workflow_stop(runner, app_dir_path, target_workflow_name)


    def test_core_components(self, app_dir_path, target_workflow_name):
      app = App(app_dir_path, DOCKER_NAMESPACE)
      config = {
        'workflow_name': target_workflow_name,
        'service_name': 'build'
      }

      command = WorkflowValidateCommand(app, **config)
      command.validate()

    def test_external_service(self, external_service_composite: ServiceComposite, app_dir_path, target_workflow_name):
      app = App(app_dir_path, DOCKER_NAMESPACE)
      config = {
        'workflow_name': target_workflow_name,
        'service_name': external_service_composite.service_name 
      }

      command = ServiceValidateCommand(app, **config)
      command.validate()

    def test_local_service(self, app_dir_path, target_workflow_name, local_service_composite: ServiceComposite):
      app = App(app_dir_path, DOCKER_NAMESPACE)
      config = {
        'workflow_name': target_workflow_name,
        'service_name': local_service_composite.service_name 
      }

      command = ServiceValidateCommand(app, **config)
      command.validate()


  class TestTestWorkflow():
    @pytest.fixture(scope='class')
    def assets_service_mock_docker_compose_path(self, mock_data_directory_path):
      path = mock_data_directory_path / "scaffold" / "docker-compose-assets-service.yml"
      return path

    @pytest.fixture(scope='class')
    def assets_service_assets_path(self, mock_data_directory_path):
      path = mock_data_directory_path / "scaffold" / "index.html"
      return path
    
    @pytest.fixture(scope='class', autouse=True)
    def target_workflow_name(self):
      yield WORKFLOW_TEST_TYPE

    @pytest.fixture(scope='class')
    def assets_service_name(self):
      yield "assets"
    
    @pytest.fixture(scope='class')
    def assets_hostname(self):
      yield "assets"

    @pytest.fixture(scope='class')
    def core_components_composite(self, target_workflow_name):
      yield CoreComponentsComposite(target_workflow_name=target_workflow_name)
    
    @pytest.fixture(scope='class')
    def external_service_composite(self, app_dir_path, target_workflow_name, external_service_name, hostname):
      yield ServiceComposite(app_dir_path=app_dir_path, target_workflow_name=target_workflow_name, service_name=external_service_name, hostname=hostname)

    @pytest.fixture(scope='class')
    def local_service_composite(self, app_dir_path, target_workflow_name, local_service_name, local_hostname):
      yield ServiceComposite(app_dir_path=app_dir_path, target_workflow_name=target_workflow_name, service_name=local_service_name, hostname=local_hostname)
    
    @pytest.fixture(scope='class')
    def assets_service_composite(self, app_dir_path, target_workflow_name, assets_service_name, assets_hostname):
      yield ServiceComposite(app_dir_path=app_dir_path, target_workflow_name=target_workflow_name, service_name=assets_service_name, hostname=assets_hostname)

    @pytest.fixture(scope='class', autouse=True)
    def setup_composites(self, core_components_composite, external_service_composite, local_service_composite, assets_service_composite):
      self.core_components_composite = core_components_composite
      self.external_service_composite = external_service_composite
      self.local_service_composite = local_service_composite
      self.assets_service_composite = assets_service_composite

    @pytest.fixture(scope="class", autouse=True)
    def create_scaffold_setup(self, runner, app_name, app_dir_path, target_workflow_name, external_service_composite, local_service_composite, assets_service_composite, mock_data_directory_path, assets_service_mock_docker_compose_path):

      TestScaffoldE2e.cli_app_create(runner, app_dir_path, app_name)

      # Create external user defined service
      TestScaffoldE2e.cli_service_create(runner, app_dir_path, external_service_composite.hostname, external_service_composite.service_name)
      # Create local user defined services
      TestScaffoldE2e.cli_service_create(runner, app_dir_path, local_service_composite.hostname, local_service_composite.service_name)
      TestScaffoldE2e.cli_service_create_assets(runner, app_dir_path, assets_service_composite.hostname, assets_service_composite.service_name)

      # Don't run the local user defined service in the 'test' workflow
      # So don't copy the Docker Compose file over

      # Add user defined Docker Compose file for the assets service
      destination_path = Path(assets_service_composite.docker_compose_path)
      assert destination_path.is_file()
      shutil.copyfile(assets_service_mock_docker_compose_path, destination_path)

      TestScaffoldE2e.cli_service_create_assets(runner, app_dir_path, assets_service_composite.hostname, assets_service_composite.service_name)

      # Add assets for assets service
      destination_assets_path = f"{app_dir_path}/{DATA_DIR_NAME}/docker/{assets_service_composite.service_name}/{target_workflow_name}/index.html"
      destination_path = Path(destination_assets_path)
      assets_mock_path = mock_data_directory_path / "scaffold" / "index.html"
      shutil.copyfile(assets_mock_path, destination_path)

      # Created shared file in fixtures folder
      app = App(app_dir_path, DOCKER_NAMESPACE)
      config = {
        'workflow_name': target_workflow_name,
        'service_name': external_service_composite.service_name 
      }
      command = ServiceValidateCommand(app, **config)
      with open(f"{command.fixtures_dir_path}/shared_file.txt", 'w') as file:
        file.write('this is a shared file')

      TestScaffoldE2e.cli_workflow_run(runner, app_dir_path, target_workflow_name=target_workflow_name)
    
    @pytest.fixture(scope="class", autouse=True)
    def cleanup_after_all(self, runner, app_dir_path, target_workflow_name):
      yield
      TestScaffoldE2e.cli_workflow_stop(runner, app_dir_path, target_workflow_name)
    

    def test_no_core_components(self, app_dir_path, target_workflow_name):
      app = App(app_dir_path, DOCKER_NAMESPACE)
      config = {
        'workflow_name': target_workflow_name,
        'service_name': 'build'
      }

      command = WorkflowValidateCommand(app, **config)
      command.validate()

    def test_user_services(self, app_dir_path, target_workflow_name, external_service_composite, local_service_composite):
      app = App(app_dir_path, DOCKER_NAMESPACE)

      config = {
        'workflow_name': target_workflow_name,
        'service_name': external_service_composite.service_name 
      }
      command = ServiceValidateCommand(app, **config)
      command.validate()

      config = {
        'workflow_name': target_workflow_name,
        'service_name': local_service_composite.service_name 
      }
      command = ServiceValidateCommand(app, **config)
      command.validate()

    def test_tests(self):
      # This is covered by test_assets
      pass

    def test_assets(self, app_dir_path, target_workflow_name):

      app = App(app_dir_path, DOCKER_NAMESPACE)
      config = {
        'workflow_name': target_workflow_name,
        'service_name': 'assets'
      }

      command = ServiceValidateCommand(app, **config)
      command.validate()

  @staticmethod
  def cli_app_create(runner: CliRunner, app_dir_path: str, app_name: str):
    pathlib.Path(f"{app_dir_path}/{DATA_DIR_NAME}").mkdir(parents=True, exist_ok=True)

    result = runner.invoke(scaffold, ['app', 'create',
      '--app-dir-path', app_dir_path,
      '--force',
      app_name
    ])

    assert result.exit_code == 0
    output = result.stdout
    assert not output

  @staticmethod
  def cli_service_create(runner: CliRunner, app_dir_path: str, hostname: str, service_name: str):
    result = runner.invoke(scaffold, ['service', 'create',
      '--app-dir-path', app_dir_path,
      '--env', 'TEST',
      '--force',
      '--hostname', hostname,
      '--scheme', 'http',
      '--port', '80',
      '--workflow', 'mock',
      '--workflow', 'record',
      '--workflow', 'test',
      service_name
    ])
    assert result.exit_code == 0
    output = result.stdout
    assert not output
 
  # Specific flags for assets
  @staticmethod
  def cli_service_create_assets(runner: CliRunner, app_dir_path: str, hostname: str, service_name: str):
    result = runner.invoke(scaffold, ['service', 'create',
      '--app-dir-path', app_dir_path,
      '--force',
      '--hostname', hostname,
      '--scheme', 'http',
      '--port', '80',
      '--proxy-mode', f"reverse:http://{hostname}:8080",
      '--detached',
      '--workflow', 'test',
      service_name
    ])
    assert result.exit_code == 0
    output = result.stdout
    assert not output
  
  @staticmethod
  def cli_workflow_create(runner: CliRunner, app_dir_path: str, service_name: str):
    result = runner.invoke(scaffold, ['workflow', 'create',
      '--app-dir-path', app_dir_path,
      '--service', service_name,
      '--template', 'mock',
      'ci',
    ])

    assert result.exit_code == 0
    output = result.stdout
    assert not output

  @staticmethod
  def cli_workflow_run(runner: CliRunner, app_dir_path: str, target_workflow_name: str):
    command = ['workflow', 'run',
      '--app-dir-path', app_dir_path,
      '--context-dir-path', app_dir_path,
      target_workflow_name,
    ]
    result = runner.invoke(scaffold, command)

    assert result.exit_code == 0
    output = result.stdout
    assert output
  
  @staticmethod
  def cli_workflow_stop(runner: CliRunner, app_dir_path: str, target_workflow_name: str):
    command = ['workflow', 'stop',
      '--app-dir-path', app_dir_path,
      '--context-dir-path', app_dir_path,
      target_workflow_name,
    ]
    result = runner.invoke(scaffold, command)

    assert result.exit_code == 0
    output = result.stdout
    assert output

