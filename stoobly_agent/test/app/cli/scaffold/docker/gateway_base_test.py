import pytest
import yaml

from unittest.mock import MagicMock

from stoobly_agent.app.cli.scaffold.app_config import AppConfig
from stoobly_agent.app.cli.scaffold.constants import (
  APP_PROXY_MODE_ENV,
  APP_PROXY_PORT_ENV,
  APP_RUNTIME_ENV,
  PROXY_MODE_FORWARD,
  RUNTIME_DOCKER,
  SERVICE_HOSTNAME_ENV,
  SERVICE_LOCAL_ENV,
  SERVICE_NAME_ENV,
  SERVICE_PORT_ENV,
  SERVICE_SCHEME_ENV,
  SERVICES_NAMESPACE,
)
from stoobly_agent.app.cli.scaffold.docker.constants import DOCKER_COMPOSE_BASE
from stoobly_agent.app.cli.scaffold.docker.service.gateway_base import GatewayBase
from stoobly_agent.app.cli.scaffold.templates.constants import CORE_GATEWAY_SERVICE_NAME
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


class TestGatewayBaseExtraHostsForLocal():

  @pytest.fixture
  def workflow_name(self):
    return 'record'

  def test_configure_adds_extra_hosts_when_forward_and_local_service(self, tmp_path, workflow_name):
    scaffold = tmp_path / 'scaffold'
    (scaffold / 'gateway').mkdir(parents=True)
    (scaffold / 'myservice').mkdir(parents=True)
    runtime_root = tmp_path / 'runtime'
    (runtime_root / SERVICES_NAMESPACE / CORE_GATEWAY_SERVICE_NAME).mkdir(parents=True)

    with open(scaffold / '.config.yml', 'w') as f:
      yaml.dump(
        {
          APP_PROXY_MODE_ENV: PROXY_MODE_FORWARD,
          APP_RUNTIME_ENV: RUNTIME_DOCKER,
          APP_PROXY_PORT_ENV: 8080,
        },
        f,
      )

    with open(scaffold / 'myservice' / '.config.yml', 'w') as f:
      yaml.dump(
        {
          SERVICE_HOSTNAME_ENV: 'api.example.test',
          SERVICE_PORT_ENV: 4000,
          SERVICE_SCHEME_ENV: 'http',
          SERVICE_LOCAL_ENV: True,
          SERVICE_NAME_ENV: 'myservice',
        },
        f,
      )

    with open(scaffold / 'gateway' / '.docker-compose.base.template.yml', 'w') as f:
      yaml.dump({'services': {'gateway_base': {'image': 'busybox'}}}, f)

    wf_ns = MagicMock(spec=WorkflowNamespace)
    wf_ns.app.runtime_app_data_dir.path = str(runtime_root)

    app_config = AppConfig(str(scaffold))
    gb = GatewayBase(wf_ns, [str(scaffold / 'myservice')])
    gb.with_app_config(app_config)
    gb.no_publish = True

    stub = MagicMock()
    stub.workflow_name = workflow_name
    stub.service_config = MagicMock(url=None)
    gb.with_commands([stub])

    gb.configure()

    out_path = runtime_root / SERVICES_NAMESPACE / CORE_GATEWAY_SERVICE_NAME / DOCKER_COMPOSE_BASE
    assert out_path.is_file()
    with open(out_path) as f:
      out = yaml.safe_load(f)
    gateway_svc = out['services']['gateway_base']
    assert 'extra_hosts' in gateway_svc
    assert 'host.docker.internal:host-gateway' in gateway_svc['extra_hosts']

  def test_configure_skips_extra_hosts_when_no_local_service(self, tmp_path, workflow_name):
    scaffold = tmp_path / 'scaffold2'
    (scaffold / 'gateway').mkdir(parents=True)
    (scaffold / 'remote').mkdir(parents=True)
    runtime_root = tmp_path / 'runtime2'
    (runtime_root / SERVICES_NAMESPACE / CORE_GATEWAY_SERVICE_NAME).mkdir(parents=True)

    with open(scaffold / '.config.yml', 'w') as f:
      yaml.dump(
        {
          APP_PROXY_MODE_ENV: PROXY_MODE_FORWARD,
          APP_RUNTIME_ENV: RUNTIME_DOCKER,
          APP_PROXY_PORT_ENV: 8080,
        },
        f,
      )

    with open(scaffold / 'remote' / '.config.yml', 'w') as f:
      yaml.dump(
        {
          SERVICE_HOSTNAME_ENV: 'api.example.test',
          SERVICE_PORT_ENV: 4000,
          SERVICE_SCHEME_ENV: 'http',
          SERVICE_NAME_ENV: 'remote',
        },
        f,
      )

    with open(scaffold / 'gateway' / '.docker-compose.base.template.yml', 'w') as f:
      yaml.dump({'services': {'gateway_base': {'image': 'busybox'}}}, f)

    wf_ns = MagicMock(spec=WorkflowNamespace)
    wf_ns.app.runtime_app_data_dir.path = str(runtime_root)

    app_config = AppConfig(str(scaffold))
    gb = GatewayBase(wf_ns, [str(scaffold / 'remote')])
    gb.with_app_config(app_config)
    gb.no_publish = True

    stub = MagicMock()
    stub.workflow_name = workflow_name
    stub.service_config = MagicMock(url=None)
    gb.with_commands([stub])

    gb.configure()

    out_path = runtime_root / SERVICES_NAMESPACE / CORE_GATEWAY_SERVICE_NAME / DOCKER_COMPOSE_BASE
    with open(out_path) as f:
      out = yaml.safe_load(f)
    gateway_svc = out['services']['gateway_base']
    extra = gateway_svc.get('extra_hosts') or []
    assert 'host.docker.internal:host-gateway' not in extra
