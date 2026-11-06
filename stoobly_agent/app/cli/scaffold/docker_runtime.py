import os
import sys

from stoobly_agent.app.cli.scaffold.app import App
from stoobly_agent.app.cli.scaffold.app_config import AppConfig
from stoobly_agent.app.cli.scaffold.constants import SERVICES_NAMESPACE, STOOBLY_HOME_DIR
from stoobly_agent.config.data_dir import DATA_DIR_NAME


def cli_app_dir_path(argv=None):
  args = sys.argv if argv is None else argv
  for i, arg in enumerate(args):
    if arg == '--app-dir-path' and i + 1 < len(args):
      return args[i + 1]
    if arg.startswith('--app-dir-path='):
      return arg.split('=', 1)[1]
  return None


def cli_is_containerized(argv=None):
  args = sys.argv if argv is None else argv
  return '--containerized' in args


def scaffold_namespace_path_for_runtime_check(argv=None):
  # Inside a container, host --app-dir-path is not mounted; only /home/stoobly/.stoobly is.
  # Resolve the services config from STOOBLY_HOME_DIR so we never DataDir.create() the host path.
  if cli_is_containerized(argv):
    return os.path.join(STOOBLY_HOME_DIR, DATA_DIR_NAME, SERVICES_NAMESPACE)
  return App(cli_app_dir_path(argv)).scaffold_namespace_path


def is_docker_runtime(argv=None):
  return AppConfig(scaffold_namespace_path_for_runtime_check(argv)).runtime_docker
