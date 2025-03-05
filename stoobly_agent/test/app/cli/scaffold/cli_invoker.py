import pathlib
import pdb

from click.testing import CliRunner

from stoobly_agent.app.cli import scaffold
from stoobly_agent.config.data_dir import DATA_DIR_NAME


class ScaffoldCliInvoker():

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
  def cli_app_mkcert(runner: CliRunner, app_dir_path: str):
    result = runner.invoke(scaffold, ['app', 'mkcert',
      '--app-dir-path', app_dir_path,
      '--context-dir-path', app_dir_path,
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
      '--force',
      '--hostname', hostname,
      '--scheme', scheme,
      '--port', port,
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
    proxy_mode_reverse_spec = f"reverse:{scheme}://{hostname}:8080"

    result = runner.invoke(scaffold, ['service', 'create',
      '--app-dir-path', app_dir_path,
      '--force',
      '--hostname', hostname,
      '--scheme', scheme,
      '--port', port,
      '--proxy-mode', proxy_mode_reverse_spec,
      '--detached',
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
    output = result.stdout
    assert not output

  @staticmethod
  def cli_workflow_up(runner: CliRunner, app_dir_path: str, target_workflow_name: str):
    command = ['workflow', 'up',
      '--app-dir-path', app_dir_path,
      '--context-dir-path', app_dir_path,
      target_workflow_name,
    ]
    result = runner.invoke(scaffold, command)

    assert result.exit_code == 0
    output = result.stdout
    assert output

  @staticmethod
  def cli_workflow_down(runner: CliRunner, app_dir_path: str, target_workflow_name: str):
    command = ['workflow', 'down',
      '--app-dir-path', app_dir_path,
      '--context-dir-path', app_dir_path,
      target_workflow_name,
    ]
    result = runner.invoke(scaffold, command)

    assert result.exit_code == 0
    output = result.stdout
    assert output