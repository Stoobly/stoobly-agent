import os
import sys
from typing import Any, Dict

import click
import yaml

from stoobly_agent.app.cli.scaffold.constants import CORE_WORKFLOWS
from stoobly_agent.config.data_dir import DataDir

HTTP_METHODS = ['GET', 'POST', 'OPTIONS', 'PATCH', 'PUT', 'DELETE']


def _rewrite_set_options(name: str) -> Dict[str, Any]:
  return {
    'method': list(HTTP_METHODS),
    'mode': ['record'],
    'name': name,
    'pattern': '.*',
    'type': 'Header',
    'value': '',
    'workflow': ['record'],
  }


def default_scaffold_config(app_name: str = None) -> Dict[str, Any]:
  if app_name is None:
    app_name = os.path.basename(os.path.abspath(os.getcwd())) or 'app'

  return {
    'version': 1,
    'commands': [
      {
        'resource': 'app',
        'action': 'create',
        'options': {
          'app_name': app_name,
        },
      },
      {
        'resource': 'service',
        'action': 'create',
        'options': {
          'service_name': 'backend',
          'hostname': 'local.api',
          'scheme': 'http',
          'port': 80,
          'local': True,
        },
      },
      {
        'resource': 'setting',
        'action': 'rewrite set',
        'options': _rewrite_set_options('authorization'),
      },
      {
        'resource': 'setting',
        'action': 'rewrite set',
        'options': _rewrite_set_options('cookie'),
      },
      {
        'resource': 'intercept',
        'action': 'enable',
        'options': {
          'workflow': list(CORE_WORKFLOWS),
        },
      },
    ],
  }


def create_scaffold_yml(path: str = None, app_name: str = None) -> str:
  """Write default scaffold.yml if missing. Returns the path written.

  Defaults to ``cwd/.stoobly/scaffold.yml`` (not an ancestor data dir) so a new
  project can be initialized from an empty directory.
  """
  scaffold_path = path or DataDir.instance(os.getcwd()).scaffold_file_path

  if os.path.exists(scaffold_path):
    click.echo(f"Error: {scaffold_path} already exists", err=True)
    sys.exit(1)

  parent = os.path.dirname(scaffold_path)
  if parent:
    os.makedirs(parent, exist_ok=True)

  config = default_scaffold_config(app_name=app_name)
  with open(scaffold_path, 'w') as fp:
    yaml.safe_dump(config, fp, default_flow_style=False, sort_keys=False, allow_unicode=True)

  return scaffold_path


# Options that belong to the scaffold CLI only and should not be persisted.
EXCLUDED_SAVE_KWARGS = frozenset({'apply', 'save', 'service_path'})


def build_scaffold_command_step(resource: str, action: str, kwargs: dict) -> Dict[str, Any]:
  """Build a scaffold.yml command step from Click kwargs."""
  options: Dict[str, Any] = {}
  for key, value in kwargs.items():
    if key in EXCLUDED_SAVE_KWARGS:
      continue
    if value is None or value == () or value == []:
      continue
    if isinstance(value, bool) and not value:
      continue
    if isinstance(value, tuple):
      value = list(value)
    options[key] = value

  step: Dict[str, Any] = {
    'resource': resource,
    'action': action,
  }
  if options:
    step['options'] = options
  return step


def save_scaffold_command(path: str, resource: str, action: str, kwargs: dict) -> str:
  """Append a command step to scaffold.yml, creating the file if missing.

  Returns the path written.
  """
  step = build_scaffold_command_step(resource, action, kwargs)

  if os.path.exists(path):
    with open(path, 'r') as fp:
      data = yaml.safe_load(fp)

    if not isinstance(data, dict):
      data = {}

    commands = data.get('commands')
    if not isinstance(commands, list):
      commands = []

    if data.get('version') is None:
      data['version'] = 1

    commands.append(step)
    data['commands'] = commands
  else:
    parent = os.path.dirname(path)
    if parent:
      os.makedirs(parent, exist_ok=True)
    data = {
      'version': 1,
      'commands': [step],
    }

  with open(path, 'w') as fp:
    yaml.safe_dump(data, fp, default_flow_style=False, sort_keys=False, allow_unicode=True)

  return path
