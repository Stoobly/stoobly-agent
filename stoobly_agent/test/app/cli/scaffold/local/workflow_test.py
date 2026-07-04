import os
import pdb
import pytest
import requests
import shutil
import tempfile
import time
import yaml

from click.testing import CliRunner
from pathlib import Path

from stoobly_agent.app.cli.scaffold.app import App
from stoobly_agent.app.cli.scaffold.constants import (
  WORKFLOW_MOCK_TYPE,
  WORKFLOW_NORMALIZE_TYPE,
  WORKFLOW_RECORD_TYPE,
  WORKFLOW_TEST_TYPE,
)
from stoobly_agent.app.cli.scaffold.context_lock import ContextLock
from stoobly_agent.app.cli.scaffold.workflow_command import WorkflowCommand
from stoobly_agent.app.cli.scaffold.workflow_namespace import WorkflowNamespace
from stoobly_agent.app.settings import Settings
from stoobly_agent.config.constants import mode
from stoobly_agent.lib.orm.request import Request
from stoobly_agent.test.app.cli.scaffold.local.cli_invoker import LocalScaffoldCliInvoker
from stoobly_agent.test.test_helper import reset

@pytest.mark.e2e
class TestLocalScaffoldE2e():

  @pytest.fixture(scope='class', autouse=True)
  def settings(self):
    return reset()

  @pytest.fixture(scope='module')
  def runner(self):
    yield CliRunner()

  @pytest.fixture(scope='class')
  def app_name(self):
    yield "local-test-app"

  @pytest.fixture(scope='class')
  def temp_dir(self):
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)

  @pytest.fixture(scope='class')
  def app_dir_path(self, temp_dir, app_name):
    return os.path.join(temp_dir, app_name)

  @pytest.fixture(scope='class')
  def hostname(self):
    yield "api.example.com"

  @pytest.fixture(scope='class')
  def https_service_hostname(self):
    yield "docs.stoobly.com"
  
  @pytest.fixture(scope='class')
  def external_service_name(self):
    yield "external-api"

  @pytest.fixture(scope='class')
  def external_https_service_name(self):
    yield "external-secure-api"

  @pytest.fixture(scope='class')
  def local_hostname(self):
    yield "local-service.dev"

  @pytest.fixture(scope='class')
  def local_service_name(self):
    yield "local-service"

  @pytest.fixture(scope="class", autouse=True)
  def proxy_url(self):
    return "http://localhost:8081"

  class TestRecordWorkflow():
    @pytest.fixture(scope='class', autouse=True)
    def target_workflow_name(self):
      yield WORKFLOW_RECORD_TYPE

    @pytest.fixture(scope="class", autouse=True)
    def create_scaffold_setup(self, runner: CliRunner, app_dir_path: str, app_name: str, external_service_name: str, external_https_service_name: str, local_service_name: str, hostname: str, https_service_hostname: str, local_hostname: str):
      # Create app with local runtime
      LocalScaffoldCliInvoker.cli_app_create(runner, app_dir_path, app_name)

      # Create external user defined services
      LocalScaffoldCliInvoker.cli_service_create(runner, app_dir_path, hostname, external_service_name, False)
      LocalScaffoldCliInvoker.cli_service_create(runner, app_dir_path, https_service_hostname, external_https_service_name, True)

      # Create local user defined service
      LocalScaffoldCliInvoker.cli_service_create_local(runner, app_dir_path, local_hostname, local_service_name)

    @pytest.fixture(scope="class", autouse=True)
    def workflow_up(self, runner: CliRunner, app_dir_path: str, target_workflow_name: str, settings: Settings):
      """Test workflow up command for local execution"""
      LocalScaffoldCliInvoker.cli_workflow_up(runner, app_dir_path, target_workflow_name)
      time.sleep(1)
      settings.load()

    @pytest.fixture(scope="class", autouse=True)
    def test_workflow_down(self, runner: CliRunner, app_dir_path: str, proxy_url: str, target_workflow_name: str):
      """Test workflow down command for local execution"""
      yield

      LocalScaffoldCliInvoker.cli_workflow_down(runner, app_dir_path, target_workflow_name)
      time.sleep(1)

      try:
        requests.get('https://docs.stoobly.com', proxies={'http': proxy_url, 'https': proxy_url}, verify=False)
        assert False, "Expected ProxyError"
      except requests.exceptions.ProxyError as e:
        assert True

    def test_request_proxied(self, proxy_url: str):
      # Use http send request with proxy, do this in python, make the following not check ssl cert
      res = requests.get('https://docs.stoobly.com', proxies={'http': proxy_url, 'https': proxy_url}, verify=False)
      assert res.status_code == 200, "HTTP request with HTTP_PROXY and HTTPS_PROXY set to the local service should succeed"

    def test_app_configuration(self, app_dir_path: str):
      """Test that the app is configured for local execution"""
      app = App(app_dir_path)
      assert app.valid, "App should be valid"
      
      # Verify app is configured for local execution
      from stoobly_agent.app.cli.scaffold.app_config import AppConfig
      app_config = AppConfig(app.scaffold_namespace_path)
      assert app_config.runtime_local, "App should be configured to run locally"

    def test_services_exist(self, app_dir_path: str, external_service_name: str, local_service_name: str):
      """Test that services are created and configured properly"""
      app = App(app_dir_path)
      services = app.services
      
      # Check that our services were created
      assert external_service_name in services, f"External service {external_service_name} should exist"
      assert local_service_name in services, f"Local service {local_service_name} should exist"

    def test_workflow_logs(self, runner: CliRunner, app_dir_path: str, target_workflow_name: str):
      """Test workflow logs command for local execution"""
      LocalScaffoldCliInvoker.cli_workflow_logs(runner, app_dir_path, target_workflow_name)

    def test_intercept_mode_record(self, settings: Settings):
      # Check stoobly-agent intercept show output starts with Mock
      assert settings.proxy.intercept.mode == mode.RECORD

    def test_intercept_mode_not_active(self, settings: Settings):
      assert not settings.proxy.intercept.active

    def test_records(self, settings: Settings, proxy_url: str):
      _requests = Request.all()
      assert len(_requests) == 0, "Expected 0 requests to be recorded"
      settings.proxy.intercept.active = True
      settings.commit()
      time.sleep(1) # Wait for change to propagate
      res = requests.get('https://docs.stoobly.com', proxies={'http': proxy_url, 'https': proxy_url}, verify=False)
      assert res.status_code == 200, "HTTP request with HTTP_PROXY and HTTPS_PROXY set to the local service should succeed"
      _requests = Request.all()
      assert len(_requests) == 1, "Expected 1 request to be recorded"

    def test_access_file_exists(self, app_dir_path: str, target_workflow_name: str):
      """Test that access count is correct after workflow up"""
      app = App(app_dir_path)
      context_lock = ContextLock(app)
      access_count = context_lock.access_count()
      
      assert access_count >= 1, f"Access count should be >= 1, got {access_count}"


  class TestMockWorkflow():
    @pytest.fixture(scope='class', autouse=True)
    def target_workflow_name(self):
      yield WORKFLOW_MOCK_TYPE

    @pytest.fixture(scope="class", autouse=True)
    def create_scaffold_setup(self, runner: CliRunner, app_dir_path: str, app_name: str, external_service_name: str, hostname: str, local_service_name: str, local_hostname: str):
      # Create app with local runtime
      LocalScaffoldCliInvoker.cli_app_create(runner, app_dir_path, app_name)

      # Create external user defined service
      LocalScaffoldCliInvoker.cli_service_create(runner, app_dir_path, hostname, external_service_name, False)

      # Create local user defined service
      LocalScaffoldCliInvoker.cli_service_create_local(runner, app_dir_path, local_hostname, local_service_name)

    @pytest.fixture(scope="class", autouse=True)
    def workflow_up(self, runner: CliRunner, app_dir_path: str, target_workflow_name: str, settings: Settings):
      """Test workflow up command for local execution"""
      LocalScaffoldCliInvoker.cli_workflow_up(runner, app_dir_path, target_workflow_name)
      time.sleep(1)
      settings.load()

    @pytest.fixture(scope="class", autouse=True)
    def workflow_down(self, runner, app_dir_path, proxy_url: str, target_workflow_name):
      yield

      """Test workflow down command for local execution"""
      LocalScaffoldCliInvoker.cli_workflow_down(runner, app_dir_path, target_workflow_name)
      time.sleep(1)

      try:
        requests.get('https://docs.stoobly.com', proxies={'http': proxy_url, 'https': proxy_url}, verify=False)
        assert False, "Expected ProxyError"
      except requests.exceptions.ProxyError as e:
        assert True

    def test_app_configuration(self, app_dir_path):
      """Test that the app is configured for local execution"""
      app = App(app_dir_path)
      assert app.valid, "App should be valid"
      
      # Verify app is configured for local execution
      from stoobly_agent.app.cli.scaffold.app_config import AppConfig
      app_config = AppConfig(app.scaffold_namespace_path)
      assert app_config.runtime_local, "App should be configured to run locally"

    def test_services_exist(self, app_dir_path, external_service_name, local_service_name):
      """Test that services are created and configured properly"""
      app = App(app_dir_path)
      services = app.services
      
      # Check that our services were created
      assert external_service_name in services, f"External service {external_service_name} should exist"
      assert local_service_name in services, f"Local service {local_service_name} should exist"

    def test_workflow_filter(self, proxy_url: str):
      """Test workflow up command for local execution"""
      # Use http send request with proxy, do this in python, make the following not check ssl cert
      res = requests.get('https://www.google.com', proxies={'http': proxy_url, 'https': proxy_url}, verify=False)
      assert res.status_code == 200, "Non-scaffold service should be accessible"

    def test_workflow_up(self, hostname, proxy_url: str):
      """Test workflow up command for local execution"""
      # Use http send request with proxy, do this in python, make the following not check ssl cert
      res = requests.get('http://' + hostname, proxies={'http': proxy_url, 'https': proxy_url}, verify=False)
      assert res.status_code == 499, "HTTP request with HTTP_PROXY and HTTPS_PROXY set to the local service should succeed"

    def test_public_directory(self, app_dir_path: str, local_service_name: str, proxy_url: str, target_workflow_name: str):
      """Test public directory is created"""
      app = App(app_dir_path)
      workflow_command = WorkflowCommand(app, service_name=local_service_name, workflow_name=target_workflow_name)
      assert os.path.exists(workflow_command.public_dir_path), "Public directory should be created"
      # Create an index.html file in the public directory
      with open(os.path.join(workflow_command.public_dir_path, 'index.html'), 'w') as f:
        f.write('Hello World!')
      res = requests.get(
        workflow_command.service_config.url, 
        headers={'Accept': 'text/html'},
        proxies={'http': proxy_url, 'https': proxy_url}, verify=False
      )
      assert res.status_code == 200
      assert res.text == 'Hello World!'

    def test_response_fixtures(self, app_dir_path: str, local_service_name: str, proxy_url: str, target_workflow_name: str):
      """Test response fixtures are created"""
      app = App(app_dir_path)
      workflow_command = WorkflowCommand(app, service_name=local_service_name, workflow_name=target_workflow_name)
      assert os.path.exists(workflow_command.response_fixtures_path), "Response fixtures should be created"

      contents = yaml.dump({'GET': {'/fixtures': {'path': os.path.basename(workflow_command.response_fixtures_path)}}})
      # Create a fixtures.yml file in the response fixtures directory
      with open(os.path.join(workflow_command.response_fixtures_path), 'w') as f:
        f.write(contents)

      res = requests.get(
        workflow_command.service_config.url + '/fixtures', 
        proxies={'http': proxy_url, 'https': proxy_url}, verify=False
      )
      assert res.status_code == 200
      assert res.text == contents

    def test_workflow_logs(self, runner, app_dir_path, target_workflow_name):
      """Test workflow logs command for local execution"""
      LocalScaffoldCliInvoker.cli_workflow_logs(runner, app_dir_path, target_workflow_name)

    def test_lifecycle_hooks(self, app_dir_path: str, local_service_name: str, proxy_url: str, target_workflow_name: str):
      """Write a lifecycle hooks file, send a request, and assert response mutated by hooks."""
      app = App(app_dir_path)
      workflow_command = WorkflowCommand(app, service_name=local_service_name, workflow_name=target_workflow_name)

      # Ensure public dir serves a simple page to trigger a 200 response
      if not os.path.exists(workflow_command.public_dir_path):
        os.makedirs(workflow_command.public_dir_path, exist_ok=True)

      with open(os.path.join(workflow_command.public_dir_path, 'index.html'), 'w') as f:
        f.write('Hello Hooks!')

      # Create a temporary lifecycle hooks file that mutates the response in after_mock
      hooks_file_path = workflow_command.lifecycle_hooks_path
      hooks_content = "\n".join([
        "AFTER_MOCK_RESPONSE_HEADER_NAME = 'X-After-Mock-Response-Header'",
        "AFTER_MOCK_RESPONSE_HEADER_VALUE = 'after-mock-response-value'",
        "def handle_after_mock(context):",
        "  context.flow.response.headers[AFTER_MOCK_RESPONSE_HEADER_NAME] = AFTER_MOCK_RESPONSE_HEADER_VALUE",
      ])
      with open(hooks_file_path, 'w') as f:
        f.write(hooks_content)

      res = requests.get(
        workflow_command.service_config.url,      
        proxies={'http': proxy_url, 'https': proxy_url}, verify=False
      )
      assert res.status_code == 200

      # After mock hook should add a response header
      assert res.headers.get('X-After-Mock-Response-Header') == 'after-mock-response-value'

    def test_intercept_mode_mock(self, settings: Settings):
      # Check starts with Mock
      assert settings.proxy.intercept.mode == mode.MOCK

    def test_intercept_mode_active(self, settings: Settings):
      assert settings.proxy.intercept.active

    def test_access_file_exists(self, app_dir_path: str, target_workflow_name: str):
      """Test that access count is correct after workflow up"""
      app = App(app_dir_path)
      context_lock = ContextLock(app)
      access_count = context_lock.access_count()
      
      assert access_count >= 1, f"Access count should be >= 1, got {access_count}"

  class TestNormalizeWorkflow():
    @pytest.fixture(scope='class', autouse=True)
    def target_workflow_name(self):
      yield WORKFLOW_NORMALIZE_TYPE

    @pytest.fixture(scope="class", autouse=True)
    def create_scaffold_setup(self, runner: CliRunner, app_dir_path: str, app_name: str, external_service_name: str, external_https_service_name: str, local_service_name: str, hostname: str, https_service_hostname: str, local_hostname: str):
      # Create app with local runtime
      LocalScaffoldCliInvoker.cli_app_create(runner, app_dir_path, app_name)

      # Create external user defined services
      LocalScaffoldCliInvoker.cli_service_create(runner, app_dir_path, hostname, external_service_name, False)
      LocalScaffoldCliInvoker.cli_service_create(runner, app_dir_path, https_service_hostname, external_https_service_name, True)

      # Create local user defined service
      LocalScaffoldCliInvoker.cli_service_create_local(runner, app_dir_path, local_hostname, local_service_name)

    @pytest.fixture(scope="class", autouse=True)
    def workflow_up(self, runner: CliRunner, app_dir_path: str, target_workflow_name: str, settings: Settings):
      """Start the normalize workflow"""
      LocalScaffoldCliInvoker.cli_workflow_up(runner, app_dir_path, target_workflow_name)
      time.sleep(1)
      settings.load()

    @pytest.fixture(scope="class", autouse=True)
    def test_workflow_down(self, runner: CliRunner, app_dir_path: str, proxy_url: str, target_workflow_name: str):
      yield

      LocalScaffoldCliInvoker.cli_workflow_down(runner, app_dir_path, target_workflow_name)
      time.sleep(1)

      try:
        requests.get('https://docs.stoobly.com', proxies={'http': proxy_url, 'https': proxy_url}, verify=False)
        assert False, "Expected ProxyError after workflow down"
      except requests.exceptions.ProxyError:
        assert True

    def test_request_proxied(self, proxy_url: str):
      """Normalize mode forwards to the real upstream — expect a real 200"""
      res = requests.get('https://docs.stoobly.com', proxies={'http': proxy_url, 'https': proxy_url}, verify=False)
      assert res.status_code == 200, "Proxied request in normalize mode should forward to the real upstream"

    def test_app_configuration(self, app_dir_path: str):
      """The app should be valid and configured for local execution"""
      app = App(app_dir_path)
      assert app.valid, "App should be valid"

      from stoobly_agent.app.cli.scaffold.app_config import AppConfig
      app_config = AppConfig(app.scaffold_namespace_path)
      assert app_config.runtime_local, "App should be configured to run locally"

    def test_services_exist(self, app_dir_path: str, external_service_name: str, local_service_name: str):
      """Services should be created and present in the app"""
      app = App(app_dir_path)
      services = app.services

      assert external_service_name in services, f"External service {external_service_name} should exist"
      assert local_service_name in services, f"Local service {local_service_name} should exist"

    def test_intercept_mode_normalize(self, settings: Settings):
      """Workflow up should set the intercept mode to normalize"""
      assert settings.proxy.intercept.mode == mode.NORMALIZE

    def test_no_records(self, settings: Settings, proxy_url: str):
      """Normalize mode rewrites and forwards; it does not persist Request records"""
      _requests = Request.all()
      assert len(_requests) == 0, "Expected 0 requests before enabling intercept"
      settings.proxy.intercept.active = True
      settings.commit()
      time.sleep(1)
      res = requests.get('https://docs.stoobly.com', proxies={'http': proxy_url, 'https': proxy_url}, verify=False)
      assert res.status_code == 200
      _requests = Request.all()
      assert len(_requests) == 0, "Normalize mode should not record requests"

    def test_lifecycle_hooks(self, app_dir_path: str, external_https_service_name: str, https_service_hostname: str, proxy_url: str, target_workflow_name: str):
      """Write a handle_after_normalize hook and assert the upstream response is mutated."""
      app = App(app_dir_path)
      workflow_command = WorkflowCommand(app, service_name=external_https_service_name, workflow_name=target_workflow_name)

      hooks_content = "\n".join([
        "HEADER_NAME = 'X-After-Normalize-Header'",
        "HEADER_VALUE = 'after-normalize-value'",
        "def handle_after_normalize(context):",
        "  context.flow.response.headers[HEADER_NAME] = HEADER_VALUE",
      ])
      with open(workflow_command.lifecycle_hooks_path, 'w') as f:
        f.write(hooks_content)

      res = requests.get(
        'https://' + https_service_hostname,
        proxies={'http': proxy_url, 'https': proxy_url}, verify=False
      )
      assert res.status_code == 200
      assert res.headers.get('X-After-Normalize-Header') == 'after-normalize-value'

    def test_workflow_logs(self, runner: CliRunner, app_dir_path: str, target_workflow_name: str):
      """Workflow logs command should succeed"""
      LocalScaffoldCliInvoker.cli_workflow_logs(runner, app_dir_path, target_workflow_name)

    def test_access_file_exists(self, app_dir_path: str, target_workflow_name: str):
      """Access count should be >= 1 after workflow up"""
      app = App(app_dir_path)
      context_lock = ContextLock(app)
      access_count = context_lock.access_count()

      assert access_count >= 1, f"Access count should be >= 1, got {access_count}"


  class TestTestWorkflow():
    @pytest.fixture(scope='class', autouse=True)
    def target_workflow_name(self):
      yield WORKFLOW_TEST_TYPE

    @pytest.fixture(scope='class')
    def assets_service_name(self):
      yield "assets"
    
    @pytest.fixture(scope='class')
    def assets_hostname(self):
      yield "assets.local"

    @pytest.fixture(scope="class", autouse=True)
    def create_scaffold_setup(self, runner: CliRunner, app_name: str, app_dir_path: str, external_service_name: str, hostname: str, local_service_name: str, local_hostname: str):
      # Create app with local runtime
      LocalScaffoldCliInvoker.cli_app_create(runner, app_dir_path, app_name)

      # Create external user defined service
      LocalScaffoldCliInvoker.cli_service_create(runner, app_dir_path, hostname, external_service_name, False)

      # Create local user defined service
      LocalScaffoldCliInvoker.cli_service_create_local(runner, app_dir_path, local_hostname, local_service_name)

    @pytest.fixture(scope="class", autouse=True)
    def workflow_up(self, runner: CliRunner, app_dir_path: str, target_workflow_name: str, settings: Settings):
      """Test workflow up command for local execution"""

      LocalScaffoldCliInvoker.cli_workflow_up(runner, app_dir_path, target_workflow_name)
      time.sleep(1)
      settings.load()

    @pytest.fixture(scope="class", autouse=True)
    def workflow_down(self, runner: CliRunner, app_dir_path: str, proxy_url: str, target_workflow_name: str):
      yield

      """Test workflow down command for local execution"""
      LocalScaffoldCliInvoker.cli_workflow_down(runner, app_dir_path, target_workflow_name)
      time.sleep(1)

      try:
        requests.get('https://docs.stoobly.com', proxies={'http': proxy_url, 'https': proxy_url}, verify=False)
        assert False, "Expected ProxyError"
      except requests.exceptions.ProxyError as e:
        assert True

    def test_app_configuration(self, app_dir_path: str):
      """Test that the app is configured for local execution"""
      app = App(app_dir_path)
      assert app.valid, "App should be valid"
      
      # Verify app is configured for local execution
      from stoobly_agent.app.cli.scaffold.app_config import AppConfig
      app_config = AppConfig(app.scaffold_namespace_path)
      assert app_config.runtime_local, "App should be configured to run locally"

    def test_services_exist(self, app_dir_path: str, external_service_name: str, local_service_name: str):
      """Test that services are created and configured properly"""
      app = App(app_dir_path)
      services = app.services
      
      # Check that our services were created
      assert external_service_name in services, f"External service {external_service_name} should exist"
      assert local_service_name in services, f"Local service {local_service_name} should exist"

    def test_workflow_up(self, hostname: str, proxy_url: str):
      """Test workflow up command for local execution"""
      # Use http send request with proxy, do this in python, make the following not check ssl cert
      res = requests.get('http://' + hostname, proxies={'http': proxy_url, 'https': proxy_url}, verify=False)
      assert res.status_code == 499, "HTTP request with HTTP_PROXY and HTTPS_PROXY set to the local service should succeed"

    def test_intercept_mode_test(self, settings: Settings):
      # Check starts with Test
      assert settings.proxy.intercept.mode == mode.TEST

    def test_intercept_mode_active(self, settings: Settings):
      assert settings.proxy.intercept.active

    def test_access_file_exists(self, app_dir_path: str, target_workflow_name: str):
      """Test that access count is correct after workflow up"""
      app = App(app_dir_path)
      context_lock = ContextLock(app)
      access_count = context_lock.access_count()
      
      assert access_count >= 1, f"Access count should be >= 1, got {access_count}"
