from pathlib import Path
import pdb
import shutil

from click.testing import CliRunner
import pytest

from stoobly_agent.app.cli.scaffold.app import App
from stoobly_agent.app.cli.scaffold.constants import (
  DOCKER_NAMESPACE,
  WORKFLOW_RECORD_TYPE,
  WORKFLOW_TEST_TYPE,
)
from stoobly_agent.app.cli.scaffold.managed_services_docker_compose import (
  ManagedServicesDockerCompose,
)
from stoobly_agent.app.cli.scaffold.service_docker_compose import ServiceDockerCompose
from stoobly_agent.app.cli.scaffold.service_workflow_validate_command import (
  ServiceWorkflowValidateCommand,
)
from stoobly_agent.app.cli.scaffold.workflow_validate_command import (
  WorkflowValidateCommand,
)
from stoobly_agent.config.data_dir import DataDir
from stoobly_agent.test.app.cli.scaffold.cli_invoker import ScaffoldCliInvoker
from stoobly_agent.test.test_helper import reset


@pytest.mark.e2e
class TestScaffoldE2e():

  @pytest.fixture(scope='module', autouse=True)
  def settings(self):
    return reset()

  @pytest.fixture(scope='module')
  def runner(self):
    yield CliRunner()

  @pytest.fixture(scope='class')
  def app_name(self):
    yield "0.0.1"

  @pytest.fixture(scope='class', autouse=True)
  def temp_dir(self):
    data_dir_path = DataDir.instance().path
    tmp_path = data_dir_path[:data_dir_path.rfind('/')]

    yield tmp_path

  @pytest.fixture(scope='class', autouse=True)
  def app_dir_path(self, temp_dir, app_name):
    yield temp_dir

  @pytest.fixture(scope='class')
  def mock_data_directory_path(self):
    yield Path(__file__).parent.parent.parent.parent / 'mock_data'
  
  @pytest.fixture(scope='class')
  def local_service_mock_docker_compose_path(self, mock_data_directory_path):
    path = mock_data_directory_path / "scaffold" / "docker-compose-local-service.yml"
    yield path

  @pytest.fixture(scope='class')
  def hostname(self):
    yield "http.badssl.com"

  @pytest.fixture(scope='class')
  def https_service_hostname(self):
    yield "example.com"
  
  @pytest.fixture(scope='class')
  def external_service_name(self):
    yield "external-service"

  @pytest.fixture(scope='class')
  def external_https_service_name(self):
    yield "external-https-service"

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
    def managed_services_docker_compose(self, target_workflow_name):
      yield ManagedServicesDockerCompose(target_workflow_name=target_workflow_name)

    @pytest.fixture(scope='class')
    def external_service_docker_compose(self, app_dir_path, target_workflow_name, external_service_name, hostname):
      yield ServiceDockerCompose(app_dir_path=app_dir_path, target_workflow_name=target_workflow_name, service_name=external_service_name, hostname=hostname)
    
    @pytest.fixture(scope='class')
    def external_https_service_docker_compose(self, app_dir_path, target_workflow_name, external_https_service_name, https_service_hostname):
      yield ServiceDockerCompose(app_dir_path=app_dir_path, target_workflow_name=target_workflow_name, service_name=external_https_service_name, hostname=https_service_hostname)

    @pytest.fixture(scope='class')
    def local_service_docker_compose(self, app_dir_path, target_workflow_name, local_service_name, local_hostname):
      yield ServiceDockerCompose(app_dir_path=app_dir_path, target_workflow_name=target_workflow_name, service_name=local_service_name, hostname=local_hostname)

    @pytest.fixture(scope="class", autouse=True)
    def create_scaffold_setup(self, runner, app_dir_path, app_name, target_workflow_name, external_service_docker_compose, external_https_service_docker_compose, local_service_docker_compose, local_service_mock_docker_compose_path):
      ScaffoldCliInvoker.cli_app_create(runner, app_dir_path, app_name)

      # Create external user defined service
      ScaffoldCliInvoker.cli_service_create(runner, app_dir_path, external_service_docker_compose.hostname, external_service_docker_compose.service_name, False)
      ScaffoldCliInvoker.cli_service_create(runner, app_dir_path, external_https_service_docker_compose.hostname, external_https_service_docker_compose.service_name, True)

      # Create local user defined service
      ScaffoldCliInvoker.cli_service_create(runner, app_dir_path, local_service_docker_compose.hostname, local_service_docker_compose.service_name, False)

      # Validate docker-compose path exists
      destination_path = Path(local_service_docker_compose.docker_compose_path)
      assert destination_path.is_file()
      # Add user defined Docker Compose file for the local service
      shutil.copyfile(local_service_mock_docker_compose_path, destination_path)

      # Record workflow doesn't have a public folder

      # Generate certs
      ScaffoldCliInvoker.cli_app_mkcert(runner, app_dir_path)

      ScaffoldCliInvoker.cli_workflow_up(runner, app_dir_path, target_workflow_name)

    @pytest.fixture(scope="class", autouse=True)
    def cleanup_after_all(self, runner, app_dir_path, target_workflow_name):
      yield
      ScaffoldCliInvoker.cli_workflow_down(runner, app_dir_path, target_workflow_name)
      shutil.rmtree(app_dir_path)

    def test_core_components(self, app_dir_path, target_workflow_name):
      app = App(app_dir_path, DOCKER_NAMESPACE)
      config = {
        'workflow_name': target_workflow_name,
        'service_name': 'build'
      }

      command = WorkflowValidateCommand(app, **config)
      command.validate()

    def test_external_service(self, external_service_docker_compose: ServiceDockerCompose, app_dir_path, target_workflow_name):
      app = App(app_dir_path, DOCKER_NAMESPACE)
      config = {
        'workflow_name': target_workflow_name,
        'service_name': external_service_docker_compose.service_name 
      }

      command = ServiceWorkflowValidateCommand(app, **config)
      command.validate()

    def test_local_service(self, app_dir_path, target_workflow_name, local_service_docker_compose: ServiceDockerCompose):
      app = App(app_dir_path, DOCKER_NAMESPACE)
      config = {
        'workflow_name': target_workflow_name,
        'service_name': local_service_docker_compose.service_name 
      }

      command = ServiceWorkflowValidateCommand(app, **config)
      command.validate()


  class TestTestWorkflow():
    @pytest.fixture(scope='class')
    def assets_service_mock_docker_compose_path(self, mock_data_directory_path):
      path = mock_data_directory_path / "scaffold" / "docker-compose-assets-service.yml"
      yield path

    @pytest.fixture(scope='class')
    def assets_service_assets_path(self, mock_data_directory_path):
      path = mock_data_directory_path / "scaffold" / "index.html"
      yield path
    
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
    def managed_services_docker_compose(self, target_workflow_name):
      yield ManagedServicesDockerCompose(target_workflow_name=target_workflow_name)
    
    @pytest.fixture(scope='class')
    def external_service_docker_compose(self, app_dir_path, target_workflow_name, external_service_name, hostname):
      yield ServiceDockerCompose(app_dir_path=app_dir_path, target_workflow_name=target_workflow_name, service_name=external_service_name, hostname=hostname)

    @pytest.fixture(scope='class')
    def local_service_docker_compose(self, app_dir_path, target_workflow_name, local_service_name, local_hostname):
      yield ServiceDockerCompose(app_dir_path=app_dir_path, target_workflow_name=target_workflow_name, service_name=local_service_name, hostname=local_hostname)
    
    @pytest.fixture(scope='class')
    def assets_service_docker_compose(self, app_dir_path, target_workflow_name, assets_service_name, assets_hostname):
      yield ServiceDockerCompose(app_dir_path=app_dir_path, target_workflow_name=target_workflow_name, service_name=assets_service_name, hostname=assets_hostname)

    @pytest.fixture(scope='class', autouse=True)
    def setup_docker_composes(self, managed_services_docker_compose, external_service_docker_compose, local_service_docker_compose, assets_service_docker_compose):
      self.managed_services_docker_compose = managed_services_docker_compose
      self.external_service_docker_compose = external_service_docker_compose
      self.local_service_docker_compose = local_service_docker_compose
      self.assets_service_docker_compose = assets_service_docker_compose

    @pytest.fixture(scope="class", autouse=True)
    def create_scaffold_setup(self, runner, app_name, app_dir_path, target_workflow_name, external_service_docker_compose, local_service_docker_compose, assets_service_docker_compose, mock_data_directory_path, assets_service_mock_docker_compose_path):

      ScaffoldCliInvoker.cli_app_create(runner, app_dir_path, app_name)

      # Create external user defined service
      ScaffoldCliInvoker.cli_service_create(runner, app_dir_path, external_service_docker_compose.hostname, external_service_docker_compose.service_name, False)
      # Create local user defined services
      ScaffoldCliInvoker.cli_service_create(runner, app_dir_path, local_service_docker_compose.hostname, local_service_docker_compose.service_name, False)
      ScaffoldCliInvoker.cli_service_create_assets(runner, app_dir_path, assets_service_docker_compose.hostname, assets_service_docker_compose.service_name, False)

      # Don't run the local user defined service in the 'test' workflow
      # So don't copy the Docker Compose file over

      # Add user defined Docker Compose file for the assets service
      destination_path = Path(assets_service_docker_compose.docker_compose_path)
      assert destination_path.is_file()
      shutil.copyfile(assets_service_mock_docker_compose_path, destination_path)

      ScaffoldCliInvoker.cli_service_create_assets(runner, app_dir_path, assets_service_docker_compose.hostname, assets_service_docker_compose.service_name, False)

      # Add assets for assets service
      data_dir_path = DataDir.instance().path
      destination_assets_path = f"{data_dir_path}/docker/{assets_service_docker_compose.service_name}/{target_workflow_name}/index.html"
      destination_path = Path(destination_assets_path)
      assets_mock_path = mock_data_directory_path / "scaffold" / "index.html"
      shutil.copyfile(assets_mock_path, destination_path)

      # Created shared file in fixtures folder
      app = App(app_dir_path, DOCKER_NAMESPACE)
      config = {
        'workflow_name': target_workflow_name,
        'service_name': external_service_docker_compose.service_name 
      }
      command = ServiceWorkflowValidateCommand(app, **config)
      with open(f"{command.public_dir_path}/shared_file.txt", 'w') as file:
        file.write('this is a shared file')

      ScaffoldCliInvoker.cli_workflow_up(runner, app_dir_path, target_workflow_name=target_workflow_name)
    
    @pytest.fixture(scope="class", autouse=True)
    def cleanup_after_all(self, runner, app_dir_path, target_workflow_name):
      yield
      ScaffoldCliInvoker.cli_workflow_down(runner, app_dir_path, target_workflow_name)
      shutil.rmtree(app_dir_path)

    def test_no_core_components(self, app_dir_path, target_workflow_name):
      app = App(app_dir_path, DOCKER_NAMESPACE)
      config = {
        'workflow_name': target_workflow_name,
        'service_name': 'build'
      }

      command = WorkflowValidateCommand(app, **config)
      command.validate()

    def test_user_services(self, app_dir_path, target_workflow_name, external_service_docker_compose, local_service_docker_compose):
      app = App(app_dir_path, DOCKER_NAMESPACE)

      config = {
        'workflow_name': target_workflow_name,
        'service_name': external_service_docker_compose.service_name 
      }
      command = ServiceWorkflowValidateCommand(app, **config)
      command.validate()

      config = {
        'workflow_name': target_workflow_name,
        'service_name': local_service_docker_compose.service_name 
      }
      command = ServiceWorkflowValidateCommand(app, **config)
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

      command = ServiceWorkflowValidateCommand(app, **config)
      command.validate()

