import pathlib
import datetime
import pdb
import time

from click.testing import CliRunner

from stoobly_agent.app.cli.scaffold_cli import scaffold
from stoobly_agent.config.data_dir import DATA_DIR_NAME

TMP_E2E_LOG_PATH = "/tmp/stoobly-e2e.log"


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


class LocalScaffoldCliInvoker():

  @staticmethod
  def cli_app_create(runner: CliRunner, app_dir_path: str, app_name: str):
    pathlib.Path(f"{app_dir_path}/{DATA_DIR_NAME}").mkdir(parents=True, exist_ok=True)

    result = runner.invoke(scaffold, ['app', 'create',
      '--app-dir-path', app_dir_path,
      '--proxy-port', '8081',
      '--runtime', 'local',
      '--quiet',
      app_name
    ])

    assert result.exit_code == 0
    output = result.stdout
    assert not output

  @staticmethod
  def cli_service_create(runner: CliRunner, app_dir_path: str, hostname: str, service_name: str, https: bool):
    scheme = 'http'
    port = '80'
    if https == True:
      scheme = 'https'
      port = '443'

    result = runner.invoke(scaffold, ['service', 'create',
      '--app-dir-path', app_dir_path,
      '--env', 'TEST',
      '--hostname', hostname,
      '--scheme', scheme,
      '--port', port,
      '--quiet',
      '--workflow', 'mock',
      '--workflow', 'record',
      '--workflow', 'test',
      service_name
    ])
    assert result.exit_code == 0
    output = result.stdout
    assert not output

  @staticmethod
  def cli_service_create_local(runner: CliRunner, app_dir_path: str, hostname: str, service_name: str, https: bool = False):
    """Create a local service (not external)"""
    result = runner.invoke(scaffold, ['service', 'create',
      '--app-dir-path', app_dir_path,
      '--hostname', hostname,
      '--scheme', 'https' if https else 'http',
      '--port', '3000',  
      '--quiet',
      '--workflow', 'mock',
      '--workflow', 'record',
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
  def cli_workflow_up(runner: CliRunner, app_dir_path: str, target_workflow_name: str):
    command = ['workflow', 'up',
      '--app-dir-path', app_dir_path,
      '--ca-certs-install-confirm', 'y',
      '--context-dir-path', app_dir_path,
      '--hostname-install-confirm', 'y',
      target_workflow_name,
    ]
    result = runner.invoke(scaffold, command)

    if result.exit_code != 0:
      _append_error_to_tmp_log([
        f"cli_workflow_up failed with exit code {result.exit_code}",
        f"Output: {result.output}",
        f"Exception: {result.exception}",
      ])
    else:
      time.sleep(0.5) # Provide some time for the process to start

    assert result.exit_code == 0
    return result

  @staticmethod
  def cli_workflow_logs(runner: CliRunner, app_dir_path: str, target_workflow_name: str):
    command = ['workflow', 'logs',
      '--app-dir-path', app_dir_path,
      target_workflow_name,
    ]
    result = runner.invoke(scaffold, command)

    if result.exit_code != 0:
      _append_error_to_tmp_log([
        f"cli_workflow_logs failed with exit code {result.exit_code}",
        f"Output: {result.output}",
        f"Exception: {result.exception}",
      ])

    assert result.exit_code == 0
    return result

  @staticmethod
  def cli_workflow_down(runner: CliRunner, app_dir_path: str, target_workflow_name: str):
    command = ['workflow', 'down',
      '--app-dir-path', app_dir_path,
      '--context-dir-path', app_dir_path,
      target_workflow_name,
    ]
    result = runner.invoke(scaffold, command)

    if result.exit_code != 0:
      _append_error_to_tmp_log([
        f"cli_workflow_down failed with exit code {result.exit_code}",
        f"Output: {result.output}",
        f"Exception: {result.exception}",
      ])

    assert result.exit_code == 0
    return result
