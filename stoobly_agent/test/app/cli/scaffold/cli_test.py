import os
import pdb
import shutil

from click.testing import CliRunner
import pytest

from stoobly_agent.app.cli.scaffold.app import App
from stoobly_agent.app.cli.scaffold.constants import (
  DOCKER_NAMESPACE,
  WORKFLOW_RECORD_TYPE,
)
from stoobly_agent.app.cli.scaffold.service_docker_compose import ServiceDockerCompose
from stoobly_agent.config.data_dir import DataDir
from stoobly_agent.test.app.cli.scaffold.e2e_test import ScaffoldCliInvoker
from stoobly_agent.test.test_helper import reset


class TestScaffoldCli():

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

  class TestServiceDelete():
    @pytest.fixture(scope='class', autouse=True)
    def target_workflow_name(self):
      yield WORKFLOW_RECORD_TYPE

    @pytest.fixture(scope='class')
    def external_service_docker_compose(self, app_dir_path, target_workflow_name, external_service_name, hostname):
      yield ServiceDockerCompose(app_dir_path=app_dir_path, target_workflow_name=target_workflow_name, service_name=external_service_name, hostname=hostname)
    
    @pytest.fixture(scope='class')
    def external_https_service_docker_compose(self, app_dir_path, target_workflow_name, external_https_service_name, https_service_hostname):
      yield ServiceDockerCompose(app_dir_path=app_dir_path, target_workflow_name=target_workflow_name, service_name=external_https_service_name, hostname=https_service_hostname)

    @pytest.fixture(scope="class", autouse=True)
    def create_setup(self, runner, app_dir_path, app_name, external_service_docker_compose, external_https_service_docker_compose):
      
      ScaffoldCliInvoker.cli_app_create(runner, app_dir_path, app_name)

      # Create external user defined services
      ScaffoldCliInvoker.cli_service_create(runner, app_dir_path, external_service_docker_compose.hostname, external_service_docker_compose.service_name, False)
      ScaffoldCliInvoker.cli_service_create(runner, app_dir_path, external_https_service_docker_compose.hostname, external_https_service_docker_compose.service_name, True)

      # Generate certs
      ScaffoldCliInvoker.cli_app_mkcert(runner, app_dir_path)
    
    @pytest.fixture(scope="class", autouse=True)
    def cleanup_after_all(self, runner, app_dir_path, target_workflow_name):
      yield
      ScaffoldCliInvoker.cli_workflow_down(runner, app_dir_path, target_workflow_name)
      shutil.rmtree(app_dir_path)
    
 
    def test_service_delete(self, runner, app_dir_path, external_service_docker_compose):
      app = App(app_dir_path, DOCKER_NAMESPACE)
      service_name = external_service_docker_compose.service_name
      
      ScaffoldCliInvoker.cli_service_delete(runner, app_dir_path, service_name)

      found = False
      service_paths = app.service_paths
      for service_path in service_paths:
        if service_name in service_path:
          found = True
          break
      if found:
        assert False

    def test_service_delete_https(self, runner, app_dir_path, external_https_service_docker_compose):
      app = App(app_dir_path, DOCKER_NAMESPACE)
      service_name = external_https_service_docker_compose.service_name
      hostname = external_https_service_docker_compose.hostname

      ScaffoldCliInvoker.cli_service_delete(runner, app_dir_path, service_name)

      found = False
      service_paths = app.service_paths
      for service_path in service_paths:
        if service_name in service_path:
          found = True
          break
      if found:
        assert False

      # Certs should be deleted
      certs_dir_path = os.listdir(app.certs_dir_path)
      for cert_file in certs_dir_path:
        if hostname in cert_file:
          assert False

