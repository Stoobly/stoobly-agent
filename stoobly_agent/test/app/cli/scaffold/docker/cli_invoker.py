import os
import pathlib
import datetime
import pdb
import subprocess

from click.testing import CliRunner

from stoobly_agent.app.cli.scaffold.constants import CONTEXT_DIR_ENV
from stoobly_agent.app.cli.scaffold_cli import scaffold
from stoobly_agent.config.data_dir import DATA_DIR_NAME

TMP_E2E_LOG_PATH = "/tmp/stoobly-agent-test/e2e.log"


def _append_error_to_tmp_log(lines):
  """Append e2e failure details to a stable location for debugging."""
  try:
    timestamp = datetime.datetime.utcnow().isoformat(timespec='seconds') + "Z"
    with open(TMP_E2E_LOG_PATH, 'a', encoding='utf-8') as f:
      f.write(f"[{timestamp}] e2e error\n")
      for line in lines:
        f.write(f"{line}\n")
      f.write("\n")
  except Exception:
    # Avoid masking the original failure if logging itself fails.
    pass


def _dump_docker_state():
  """Write docker ps and per-container logs into the e2e log for post-mortem debugging."""
  try:
    ps = subprocess.run(['docker', 'ps', '-a'], capture_output=True, text=True, timeout=15)
    _append_error_to_tmp_log(["=== docker ps -a ===", ps.stdout or "(empty)"])

    ids = subprocess.run(['docker', 'ps', '-aq'], capture_output=True, text=True, timeout=15)
    for cid in ids.stdout.strip().splitlines():
      if not cid:
        continue
      name_r = subprocess.run(
        ['docker', 'inspect', '--format', '{{.Name}}', cid],
        capture_output=True, text=True, timeout=10,
      )
      name = name_r.stdout.strip().lstrip('/')
      logs_r = subprocess.run(
        ['docker', 'logs', '--tail', '200', cid],
        capture_output=True, text=True, timeout=15,
      )
      _append_error_to_tmp_log([
        f"=== docker logs {name} ({cid}) ===",
        logs_r.stdout or "(no stdout)",
        logs_r.stderr or "(no stderr)",
      ])
  except Exception:
    pass


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
      _append_error_to_tmp_log([
        f"cli_workflow_up failed with exit code {result.exit_code}",
        f"Output: {result.output}",
        f"Exception: {result.exception}",
      ])
      _dump_docker_state()

    assert result.exit_code == 0

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