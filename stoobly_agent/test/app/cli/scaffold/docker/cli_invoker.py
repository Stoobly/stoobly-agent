import os
import pathlib
import datetime
import pdb
import subprocess

import docker

from click.testing import CliRunner

from stoobly_agent.app.cli.scaffold_cli import scaffold
from stoobly_agent.config.data_dir import DATA_DIR_NAME

TMP_E2E_LOG_PATH = "/tmp/stoobly-agent-test/e2e.log"


def _append_error_to_tmp_log(lines):
  """Append e2e failure details to a stable location for debugging."""
  try:
    timestamp = datetime.datetime.utcnow().isoformat(timespec='seconds') + "Z"
    with open(TMP_E2E_LOG_PATH, 'a', encoding='utf-8') as f:
      f.write(f"[{timestamp}] E2E Test Error\n")
      for line in lines:
        f.write(f"{line}\n")
      f.write("\n")
  except Exception:
    # Avoid masking the original failure if logging itself fails.
    pass


def _dump_docker_state():
  """Write all container states and logs into the e2e log for post-mortem debugging."""
  client = None
  try:
    client = docker.from_env()
    containers = client.containers.list(all=True)

    summary = "\n".join(
      f"  {c.name} ({c.short_id}) status={c.status}" for c in containers
    ) or "(no containers)"
    _append_error_to_tmp_log(["=== Docker containers ===", summary])

    for container in containers:
      logs = container.logs(tail=200, stdout=True, stderr=True).decode('utf-8', errors='replace')
      _append_error_to_tmp_log([
        f"=== Container logs: {container.name} ({container.short_id}) ===",
        logs or "(empty)",
      ])
  except Exception:
    pass
  finally:
    if client:
      client.close()


def _enable_intercept_for_namespace(namespace: str):
  """Enable intercept in gateway/proxy containers for the given compose namespace."""
  client = None
  try:
    client = docker.from_env()
    for container in client.containers.list():
      name = container.name
      if name == f'{namespace}-gateway.service-1' or (
        name.startswith(f'{namespace}-') and name.endswith('.proxy-1')
      ):
        container.exec_run(
          ['stoobly-agent', 'intercept', 'enable'],
          user='stoobly',
        )
  except Exception:
    pass
  finally:
    if client:
      client.close()


class ScaffoldCliInvoker():

  @staticmethod
  def cli_app_create(runner: CliRunner, app_dir_path: str, app_name: str, proxy_mode: str = 'reverse', proxy_port: int = None, ui_port: int = None):
    pathlib.Path(f"{app_dir_path}/{DATA_DIR_NAME}").mkdir(parents=True, exist_ok=True)

    command = ['app', 'create',
      '--app-dir-path', app_dir_path,
      '--copy-on-workflow-up',
      '--quiet',
      '--runtime', 'docker',
      '--proxy-mode', proxy_mode,
    ]
    if proxy_port is not None:
      command += ['--proxy-port', str(proxy_port)]
    if ui_port is not None:
      command += ['--ui-port', str(ui_port)]
    command.append(app_name)

    result = runner.invoke(scaffold, command)

    if result.exit_code != 0:
      _append_error_to_tmp_log([
        f"cli_app_create failed with exit code {result.exit_code}",
        f"Output: {result.output}",
        f"Exception: {result.exception}",
      ])

    assert result.exit_code == 0
    output = result.stdout
    assert not output

  @staticmethod
  def cli_service_create(runner: CliRunner, app_dir_path: str, hostname: str, service_name: str, https: bool, port: int = None):
    scheme = 'http'
    default_port = '80'
    if https == True:
      scheme = 'https'
      default_port = '443'

    actual_port = str(port) if port is not None else default_port

    result = runner.invoke(scaffold, ['service', 'create',
      '--app-dir-path', app_dir_path,
      '--env', 'TEST',
      '--hostname', hostname,
      '--scheme', scheme,
      '--port', actual_port,
      '--quiet',
      '--workflow', 'mock',
      '--workflow', 'normalize',
      '--workflow', 'record',
      '--workflow', 'test',
      service_name
    ])
    assert result.exit_code == 0
    output = result.stdout
    assert not output

  # Specific flags for assets
  @staticmethod
  def cli_service_create_assets(runner: CliRunner, app_dir_path: str, hostname: str, service_name: str, https: bool):
    scheme = 'http'
    port = '80'
    if https == True:
      scheme = 'https'
      port = '443'

    result = runner.invoke(scaffold, ['service', 'create',
      '--app-dir-path', app_dir_path,
      '--hostname', hostname,
      '--scheme', scheme,
      '--port', port,
      '--upstream-hostname', hostname,
      '--upstream-port', 80,
      '--upstream-scheme', 'http',
      '--detached',
      '--quiet',
      '--workflow', 'test',
      service_name
    ])
    assert result.exit_code == 0
    output = result.stdout
    assert not output

  @staticmethod
  def cli_service_delete(runner: CliRunner, app_dir_path: str, service_name: str):
    result = runner.invoke(scaffold, ['service', 'delete',
      '--app-dir-path', app_dir_path,
      service_name
    ])
    assert result.exit_code == 0
    output = result.stdout
    assert 'error' not in output.lower()

  @staticmethod
  def cli_workflow_create(runner: CliRunner, app_dir_path: str, service_name: str):
    result = runner.invoke(scaffold, ['workflow', 'create',
      '--app-dir-path', app_dir_path,
      '--service', service_name,
      '--template', 'mock',
      'ci',
    ])

    assert result.exit_code == 0

  @staticmethod
  def cli_workflow_up(runner: CliRunner, app_dir_path: str, target_workflow_name: str, namespace: str = None):
    command = ['workflow', 'up',
      '--app-dir-path', app_dir_path,
      '--ca-certs-install-confirm', 'n',
      '--context-dir-path', app_dir_path,
      '--hostname-install-confirm', 'n',
    ]
    if namespace is not None:
      command += ['--namespace', namespace]
    command.append(target_workflow_name)

    result = runner.invoke(scaffold, command)

    if result.exit_code != 0:
      pdb.set_trace()
      _append_error_to_tmp_log([
        f"cli_workflow_up failed with exit code {result.exit_code}",
        f"Output: {result.output}",
        f"Exception: {result.exception}",
      ])
      _dump_docker_state()

    assert result.exit_code == 0

    _enable_intercept_for_namespace(namespace or target_workflow_name)

  @staticmethod
  def cli_workflow_down(runner: CliRunner, app_dir_path: str, target_workflow_name: str, namespace: str = None):
    command = ['workflow', 'down',
      '--app-dir-path', app_dir_path,
      '--context-dir-path', app_dir_path,
      '--hostname-uninstall-confirm', 'n',
    ]
    if namespace is not None:
      command += ['--namespace', namespace]
    command.append(target_workflow_name)

    result = runner.invoke(scaffold, command)

    if result.exit_code != 0:
      pdb.set_trace()
      _append_error_to_tmp_log([
        f"cli_workflow_down failed with exit code {result.exit_code}",
        f"Output: {result.output}",
        f"Exception: {result.exception}",
      ])

    assert result.exit_code == 0

  @staticmethod
  def makefile_workflow_up(runner: CliRunner, app_dir_path: str, target_workflow_name: str):
    command = ['make', '-f', os.path.join(app_dir_path, '.stoobly', 'services', 'Makefile'),
      target_workflow_name,
    ]

    # Run the command using subprocess and capture output for debugging.
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=app_dir_path)

    if result.returncode != 0:
      _append_error_to_tmp_log([
        f"makefile_workflow_up failed with exit code {result.returncode}",
        f"Output: {result.stdout}",
        f"Exception: {result.stderr}",
      ])

    assert result.returncode == 0

    _enable_intercept_for_namespace(target_workflow_name)

  @staticmethod
  def makefile_workflow_down(runner: CliRunner, app_dir_path: str, target_workflow_name: str):
    command = ['make', '-f', os.path.join(app_dir_path, '.stoobly', 'services', 'Makefile'),
      f"{target_workflow_name}/down"
    ]

    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=app_dir_path)

    if result.returncode != 0:
      _append_error_to_tmp_log([
        f"makefile_workflow_down failed with exit code {result.returncode}",
        f"Output: {result.stdout}",
        f"Exception: {result.stderr}",
      ])

    assert result.returncode == 0