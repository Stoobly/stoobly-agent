import pytest

from unittest.mock import MagicMock

from stoobly_agent.app.cli.scaffold.app_config import AppConfig
from stoobly_agent.app.cli.scaffold.constants import PROXY_MODE_FORWARD
from stoobly_agent.app.cli.scaffold.docker.service.gateway_base import GatewayBase
from stoobly_agent.app.cli.scaffold.workflow_namespace import WorkflowNamespace


# with_run_options() is the forward proxy code path only.
# Reverse proxy uses with_traefik_config() and already injects env_file via DockerWorkflowBuilder.build_proxy().
class TestGatewayBaseWithRunOptions():

  @pytest.fixture
  def workflow_name(self):
    return 'record'

  @pytest.fixture
  def app_config(self, tmp_path):
    config = AppConfig.__new__(AppConfig)
    config._AppConfig__proxy_hostname = None
    config._AppConfig__copy_on_workflow_up = False
    config._AppConfig__docker_socket_path = '/var/run/docker.sock'
    config._AppConfig__name = None
    config._AppConfig__plugins = None
    config._AppConfig__proxy_mode = PROXY_MODE_FORWARD
    config._AppConfig__proxy_port = 8080
    config._AppConfig__runtime = None
    config._AppConfig__ui_port = None
    config._Config__dir = str(tmp_path)
    return config

  @pytest.fixture
  def stub_command(self, workflow_name):
    service_config = MagicMock()
    service_config.url = None
    service_config.upstream_hostname = 'example.com'
    service_config.upstream_port = 80
    service_config.upstream_scheme = 'http'
    service_config.hostname = 'example.com'
    service_config.port = 80
    service_config.scheme = 'http'

    command = MagicMock()
    command.workflow_name = workflow_name
    command.service_config = service_config
    return command

  @pytest.fixture
  def workflow_namespace(self):
    return MagicMock(spec=WorkflowNamespace)

  @pytest.fixture
  def gateway_base(self, workflow_namespace, app_config, stub_command):
    gateway_base = GatewayBase(workflow_namespace, service_paths=[])
    gateway_base.with_app_config(app_config)
    gateway_base.with_commands([stub_command])
    return gateway_base

  def test_with_run_options_sets_env_file(self, gateway_base, workflow_name):
    """env_file must be set so WORKFLOW_NAME is available in the gateway container,
    causing ScaffoldInterceptedRequestsLogger to be used instead of SimpleInterceptedRequestsLogger."""
    compose = {}
    gateway_base.with_run_options(compose)

    assert 'env_file' in compose, (
      "gateway_base compose missing env_file — WORKFLOW_NAME won't be set in the container"
    )
    assert compose['env_file'] == [f'{workflow_name}/.env']
