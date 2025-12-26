import os
import pathlib
import pdb
import subprocess

from click.testing import CliRunner

from stoobly_agent.app.cli.scaffold_cli import scaffold
from stoobly_agent.config.data_dir import DATA_DIR_NAME

class ScaffoldCliInvoker():

  @staticmethod
  def cli_app_create(runner: CliRunner, app_dir_path: str, app_name: str):
    pathlib.Path(f"{app_dir_path}/{DATA_DIR_NAME}").mkdir(parents=True, exist_ok=True)

    result = runner.invoke(scaffold, ['app', 'create',
      '--app-dir-path', app_dir_path,
      '--quiet',
      '--runtime', 'docker',
      app_name
    ])

    if result.exit_code != 0:
      print(f"Command failed with exit code {result.exit_code}")
      print(f"Output: {result.output}")
      print(f"Exception: {result.exception}")

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
  def cli_workflow_up(runner: CliRunner, app_dir_path: str, target_workflow_name: str):
    command = ['workflow', 'up',
      '--app-dir-path', app_dir_path,
      '--context-dir-path', app_dir_path,
      '--hostname-install-confirm', 'n',
      target_workflow_name,
    ]
    result = runner.invoke(scaffold, command)

    if result.exit_code != 0:
      print(f"Command failed with exit code {result.exit_code}")
      print(f"Output: {result.output}")
      print(f"Exception: {result.exception}")

    assert result.exit_code == 0

  @staticmethod
  def cli_workflow_down(runner: CliRunner, app_dir_path: str, target_workflow_name: str):
    command = ['workflow', 'down',
      '--app-dir-path', app_dir_path,
      '--context-dir-path', app_dir_path,
      '--hostname-uninstall-confirm', 'n',
      target_workflow_name,
    ]
    result = runner.invoke(scaffold, command)

    if result.exit_code != 0:
      print(f"Down command failed with exit code {result.exit_code}")
      print(f"Output: {result.output}")
      print(f"Exception: {result.exception}")

    assert result.exit_code == 0

  @staticmethod
  def makefile_workflow_up(runner: CliRunner, app_dir_path: str, target_workflow_name: str):
    command = ['make', '-f', os.path.join(app_dir_path, '.stoobly', 'services', 'Makefile'),
      target_workflow_name,
    ]

    # Run the command using subprocess
    # Instead of piping, print to stdout and stderr
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if result.returncode != 0:
      print(f"Command failed with exit code {result.returncode}")
      print(f"Output: {result.stdout}")
      print(f"Exception: {result.stderr}")

    assert result.returncode == 0

  @staticmethod
  def makefile_workflow_down(runner: CliRunner, app_dir_path: str, target_workflow_name: str):
    command = ['make', '-f', os.path.join(app_dir_path, '.stoobly', 'services', 'Makefile'),
      f"{target_workflow_name}/down"
    ]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if result.returncode != 0:
      print(f"Command failed with exit code {result.returncode}")
      print(f"Output: {result.stdout}")
      print(f"Exception: {result.stderr}")

    assert result.returncode == 0