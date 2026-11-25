import os
import sys
from typing import Any, Dict, List, Optional, Tuple

import click
from ruamel.yaml import YAML

from stoobly_agent import COMMAND
from stoobly_agent.app.cli.scaffold.constants import CORE_WORKFLOWS
from stoobly_agent.config.data_dir import DataDir

HTTP_METHODS = ['GET', 'POST', 'OPTIONS', 'PATCH', 'PUT', 'DELETE']

# Sentinel identity value for omitted intercept --workflow (means all workflows).
_WORKFLOW_ALL = None

_CREATE_NAME_KEYS = {
  ('app', 'create'): 'app_name',
  ('service', 'create'): 'service_name',
  ('workflow', 'create'): 'workflow_name',
}

_SETTING_PATTERN_ACTIONS = frozenset({'filter set', 'match set', 'rewrite set'})


def _scaffold_yaml() -> YAML:
  """Round-trip YAML so scaffold.yml updates keep comments and key order."""
  yaml = YAML()
  yaml.default_flow_style = False
  yaml.preserve_quotes = True
  yaml.width = 4096
  return yaml


def _assign_mapping(target: dict, source: dict) -> None:
  """Update target to match source in place (preserves ruamel comments)."""
  for key in list(target.keys()):
    if key not in source:
      del target[key]

  for key, value in source.items():
    existing = target.get(key) if key in target else None
    # Unchanged values may be the same object as the target's (shallow-copied options),
    # so clearing a list below would also empty its source
    if key in target and existing == value:
      continue

    if isinstance(existing, dict) and isinstance(value, dict):
      _assign_mapping(existing, value)
    elif (
      isinstance(existing, list)
      and isinstance(value, list)
      and not isinstance(value, (str, bytes))
    ):
      del existing[:]
      existing.extend(value)
    else:
      target[key] = value


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
    _scaffold_yaml().dump(config, fp)

  return scaffold_path


# Options that belong to the scaffold CLI only and should not be persisted.
EXCLUDED_SAVE_KWARGS = frozenset({'apply', 'save', 'service_path'})

# Update-only kwargs that must not be written into a create step.
EXCLUDED_UPDATE_KWARGS = frozenset({'apply', 'save', 'service_path', 'name'})


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


def _build_update_option_patch(kwargs: dict) -> Dict[str, Any]:
  """Build option patch from update kwargs, including False bools to clear flags."""
  patch: Dict[str, Any] = {}
  for key, value in kwargs.items():
    if key in EXCLUDED_UPDATE_KWARGS:
      continue
    if value is None or value == () or value == []:
      continue
    if isinstance(value, tuple):
      value = list(value)
    patch[key] = value
  return patch


def _merge_options_into_create(existing_options: dict, patch: dict) -> Dict[str, Any]:
  """Merge update patch into create options. False bools remove create flags."""
  merged = dict(existing_options)
  for key, value in patch.items():
    if isinstance(value, bool) and not value:
      merged.pop(key, None)
    else:
      merged[key] = value
  return merged


def _option_frozenset(options: dict, key: str) -> Optional[frozenset]:
  value = options.get(key)
  if value is None or value == () or value == []:
    return None
  if isinstance(value, str):
    return frozenset([value])
  return frozenset(value)


def scaffold_command_identity(step: dict) -> Optional[Tuple]:
  """Return a uniqueness key for a scaffold.yml step, or None if not upserted.

  Identity rules:
  - app/service/workflow create: name field
  - setting filter/match set: action + pattern + method
  - setting rewrite set: action + pattern + method + type + name
  - intercept enable/disable/set: action + workflow (omitted or CORE_WORKFLOWS means all)
  """
  if not isinstance(step, dict):
    return None

  resource = step.get('resource')
  action = step.get('action')
  options = step.get('options') or {}
  if not isinstance(options, dict):
    options = {}

  name_key = _CREATE_NAME_KEYS.get((resource, action))
  if name_key is not None:
    name = options.get(name_key)
    if name is None or name == '':
      return None
    return (resource, action, name)

  if resource == 'setting' and action in _SETTING_PATTERN_ACTIONS:
    pattern = options.get('pattern')
    methods = _option_frozenset(options, 'method')
    if pattern is None or methods is None:
      return None
    if action == 'rewrite set':
      return (resource, action, pattern, methods, options.get('type'), options.get('name'))
    return (resource, action, pattern, methods)

  if resource == 'intercept' and action in ('enable', 'disable', 'set'):
    workflows = _option_frozenset(options, 'workflow')
    # Default scaffold.yml lists CORE_WORKFLOWS; CLI omit means all. Treat as one identity
    # so `intercept enable` does not append a second enable next to the default step.
    if workflows is None or workflows == frozenset(CORE_WORKFLOWS):
      return (resource, action, _WORKFLOW_ALL)
    return (resource, action, workflows)

  return None


def _upsert_scaffold_command(commands: List[dict], step: dict) -> None:
  identity = scaffold_command_identity(step)
  if identity is not None:
    match_indexes = [
      i for i, existing in enumerate(commands)
      if scaffold_command_identity(existing) == identity
    ]
    if match_indexes:
      existing = commands[match_indexes[0]]
      if isinstance(existing, dict):
        _assign_mapping(existing, step)
      else:
        commands[match_indexes[0]] = step
      for i in reversed(match_indexes[1:]):
        del commands[i]
      return
  commands.append(step)


def _load_scaffold_data(path: str) -> Dict[str, Any]:
  if os.path.exists(path):
    with open(path, 'r') as fp:
      data = _scaffold_yaml().load(fp)

    if not isinstance(data, dict):
      data = {}

    commands = data.get('commands')
    if not isinstance(commands, list):
      commands = []

    if data.get('version') is None:
      data['version'] = 1

    data['commands'] = commands
    return data

  parent = os.path.dirname(path)
  if parent:
    os.makedirs(parent, exist_ok=True)

  return {
    'version': 1,
    'commands': [],
  }


def _write_scaffold_data(path: str, data: Dict[str, Any]) -> str:
  with open(path, 'w') as fp:
    _scaffold_yaml().dump(data, fp)
  return path


def echo_scaffold_yml_updated(scaffold_path: str) -> None:
  """Print that scaffold.yml was updated and how to apply it."""
  relative_path = os.path.relpath(scaffold_path)
  click.echo(
    f"Updated {relative_path}, run `{COMMAND} scaffold apply {relative_path}` to apply the changes"
  )


def save_scaffold_command(path: str, resource: str, action: str, kwargs: dict) -> str:
  """Upsert a command step into scaffold.yml, creating the file if missing.

  Steps with a uniqueness identity replace a matching existing step in place;
  otherwise the step is appended. Returns the path written.
  """
  step = build_scaffold_command_step(resource, action, kwargs)
  data = _load_scaffold_data(path)
  _upsert_scaffold_command(data['commands'], step)
  return _write_scaffold_data(path, data)


def update_scaffold_create_command(path: str, resource: str, kwargs: dict) -> str:
  """Merge an update into the matching create step in scaffold.yml.

  Finds the create step by name identity, merges provided options in place, and
  applies rename via ``name`` when present. If no matching create exists, appends
  a create step. Always writes (update has no --apply). Returns the path written.
  """
  name_key = _CREATE_NAME_KEYS.get((resource, 'create'))
  if name_key is None:
    raise ValueError(f"No create identity for resource: {resource}")

  current_name = kwargs.get(name_key)
  if current_name is None or current_name == '':
    raise ValueError(f"Missing {name_key} for {resource} update")

  patch = _build_update_option_patch(kwargs)
  # Do not let the current identity name be overwritten by a no-op in patch;
  # rename is handled separately via kwargs['name'].
  patch.pop(name_key, None)

  new_name = kwargs.get('name')
  target_name = new_name if new_name else current_name

  data = _load_scaffold_data(path)
  commands = data['commands']
  identity = (resource, 'create', current_name)

  for existing in commands:
    if scaffold_command_identity(existing) != identity:
      continue

    if not isinstance(existing, dict):
      continue

    existing_options = existing.get('options') or {}
    if not isinstance(existing_options, dict):
      existing_options = {}

    merged = _merge_options_into_create(dict(existing_options), patch)
    merged[name_key] = target_name

    _assign_mapping(existing, {
      'resource': resource,
      'action': 'create',
      'options': merged,
    })
    return _write_scaffold_data(path, data)

  create_kwargs = dict(kwargs)
  create_kwargs[name_key] = target_name
  if 'name' in create_kwargs:
    del create_kwargs['name']
  step = build_scaffold_command_step(resource, 'create', create_kwargs)
  options = step.setdefault('options', {})
  options[name_key] = target_name
  commands.append(step)
  return _write_scaffold_data(path, data)


def remove_scaffold_create_command(path: str, resource: str, kwargs: dict) -> str:
  """Remove the matching create step from scaffold.yml.

  Finds create step(s) by name identity and deletes them. If the file does not
  exist and nothing is removed, does not create an empty file. Always writes
  when the file already existed (delete has no --apply). Returns the path.
  """
  name_key = _CREATE_NAME_KEYS.get((resource, 'create'))
  if name_key is None:
    raise ValueError(f"No create identity for resource: {resource}")

  current_name = kwargs.get(name_key)
  if current_name is None or current_name == '':
    raise ValueError(f"Missing {name_key} for {resource} delete")

  file_existed = os.path.exists(path)
  data = _load_scaffold_data(path)
  commands = data['commands']
  identity = (resource, 'create', current_name)

  match_indexes = [
    i for i, existing in enumerate(commands)
    if scaffold_command_identity(existing) == identity
  ]
  if not match_indexes and not file_existed:
    return path

  for i in reversed(match_indexes):
    del commands[i]

  return _write_scaffold_data(path, data)
