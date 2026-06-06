import pytest

from unittest.mock import MagicMock

from stoobly_agent.app.cli.scaffold.constants import (
  WORKFLOW_CONTAINER_INIT,
  WORKFLOW_CONTAINER_PROXY,
  WORKFLOW_CONTAINER_SERVICE,
)
from stoobly_agent.app.cli.scaffold.templates.constants import CORE_ENTRYPOINT_SERVICE_NAME, CORE_GATEWAY_SERVICE_NAME
from stoobly_agent.app.cli.scaffold.docker.workflow.run_command import DockerWorkflowRunCommand


@pytest.fixture
def run_command():
  return DockerWorkflowRunCommand.__new__(DockerWorkflowRunCommand)


def _stub_command(service_name, workflow_name, compose_services):
  command = MagicMock()
  command.service_name = service_name
  command.workflow_name = workflow_name
  command.containers = {name: {} for name in compose_services}
  return command


class TestBuildLogCommands:

  def test_reverse_logs_init_then_proxy(self, run_command):
    command = _stub_command('api', 'record', ['api.init', 'api.proxy'])
    log_commands = run_command._build_log_commands(
      command,
      containers=[WORKFLOW_CONTAINER_INIT, WORKFLOW_CONTAINER_PROXY],
      namespace='record',
    )

    assert log_commands == [
      'echo "=== Logging record-api.init-1"',
      'docker logs record-api.init-1',
      'echo "=== Logging record-api.proxy-1"',
      'docker logs record-api.proxy-1',
    ]

  def test_reverse_follow_only_on_proxy(self, run_command):
    command = _stub_command('api', 'record', ['api.init', 'api.proxy'])
    log_commands = run_command._build_log_commands(
      command,
      containers=[WORKFLOW_CONTAINER_INIT, WORKFLOW_CONTAINER_PROXY],
      follow=True,
      namespace='record',
    )

    assert log_commands[1] == 'docker logs record-api.init-1'
    assert log_commands[3] == 'docker logs --follow record-api.proxy-1'

  def test_forward_logs_service_when_init_absent(self, run_command):
    command = _stub_command('gateway', 'record', ['gateway.service'])
    log_commands = run_command._build_log_commands(
      command,
      containers=[WORKFLOW_CONTAINER_INIT, WORKFLOW_CONTAINER_SERVICE],
      namespace='record',
    )

    assert log_commands == [
      'echo "=== Logging record-gateway.service-1"',
      'docker logs record-gateway.service-1',
    ]

  def test_forward_follow_only_on_service(self, run_command):
    command = _stub_command('gateway', 'record', ['gateway.init', 'gateway.service'])
    log_commands = run_command._build_log_commands(
      command,
      containers=[WORKFLOW_CONTAINER_INIT, WORKFLOW_CONTAINER_SERVICE],
      follow=True,
      namespace='record',
    )

    assert log_commands[1] == 'docker logs record-gateway.init-1'
    assert log_commands[3] == 'docker logs --follow record-gateway.service-1'

  def test_skips_missing_init_container(self, run_command):
    command = _stub_command('api', 'record', ['api.proxy'])
    log_commands = run_command._build_log_commands(
      command,
      containers=[WORKFLOW_CONTAINER_INIT, WORKFLOW_CONTAINER_PROXY],
      namespace='record',
    )

    assert log_commands == [
      'echo "=== Logging record-api.proxy-1"',
      'docker logs record-api.proxy-1',
    ]


class TestForwardLogCommandSort:

  def _sort(self, commands):
    return sorted(
      commands,
      key=lambda x: (
        2 if x[0] == CORE_ENTRYPOINT_SERVICE_NAME else 1 if x[0] == CORE_GATEWAY_SERVICE_NAME else 0,
        x[1].service_config.priority,
      ),
    )

  def test_gateway_sorted_second_to_last(self):
    api_command = MagicMock()
    api_command.service_config.priority = 10
    gateway_command = MagicMock()
    gateway_command.service_config.priority = 0
    entrypoint_command = MagicMock()
    entrypoint_command.service_config.priority = 5

    commands = [
      ('gateway', gateway_command),
      ('entrypoint', entrypoint_command),
      ('api', api_command),
    ]
    sorted_commands = self._sort(commands)

    assert [service for service, _ in sorted_commands] == ['api', 'gateway', 'entrypoint']

  def test_gateway_last_when_entrypoint_absent(self):
    api_command = MagicMock()
    api_command.service_config.priority = 10
    gateway_command = MagicMock()
    gateway_command.service_config.priority = 0

    commands = [
      ('gateway', gateway_command),
      ('api', api_command),
    ]
    sorted_commands = self._sort(commands)

    assert [service for service, _ in sorted_commands] == ['api', 'gateway']
