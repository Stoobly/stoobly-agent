import json
import logging
import os
import sys

from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import click
import yaml

from stoobly_agent.app.cli.helpers.opencli_resolve import resolve_path
from stoobly_agent.config.constants.env_vars import LOG_LEVEL
from stoobly_agent.lib.logger import DEBUG, ERROR, INFO, Logger, WARNING

LOG_ID = 'Scaffold'

_LEVELS = {
  DEBUG: logging.DEBUG,
  INFO: logging.INFO,
  WARNING: logging.WARNING,
  ERROR: logging.ERROR,
}


def _logger() -> logging.Logger:
  logger = Logger.instance(LOG_ID)
  # Named loggers inherit root; set from env (default info) so info is not dropped
  # when root remains at WARNING (basicConfig no-op if handlers already exist).
  # Always re-apply: other CLI commands can mutate LOG_LEVEL and the named logger
  # retains a prior level after handlers are cleared.
  level_name = (os.getenv(LOG_LEVEL) or INFO).lower()
  logger.setLevel(_LEVELS.get(level_name, logging.INFO))
  return logger

SUPPORTED_VERSIONS = {1}
YAML_FORMAT = 'yaml'
JSON_FORMAT = 'json'
APPLY_FORMATS = [YAML_FORMAT, JSON_FORMAT]

OPENCLI_PATH = resolve_path('scaffold')

PATH_OPTION_KEYS = frozenset({
  'app_dir_path',
  'context_dir_path',
  'script_path',
  'ca_certs_dir_path',
  'certs_dir_path',
  'docker_socket_path',
})

# Commands that write to build init SETTINGS / INTERCEPT sections.
INIT_SECTION_RESOURCES = frozenset({'setting', 'intercept'})


class ApplyConfigError(Exception):
  pass


def load_config(path: str, format: str = YAML_FORMAT) -> Dict[str, Any]:
  with open(path, 'r') as fp:
    if format == JSON_FORMAT:
      data = json.load(fp)
    elif format == YAML_FORMAT:
      data = yaml.safe_load(fp)
    else:
      raise ApplyConfigError(f"Unsupported format: {format}. Supported formats: {', '.join(APPLY_FORMATS)}")

  if data is None:
    raise ApplyConfigError("Config file is empty")

  if not isinstance(data, dict):
    raise ApplyConfigError("Config root must be a mapping")

  return data


def _kebab_to_snake(name: str) -> str:
  return name.replace('-', '_')


def _cli_param_name(entry: Dict[str, Any]) -> str:
  return _kebab_to_snake(str(entry['name']))


def _is_flag_option(option: Dict[str, Any]) -> bool:
  return not option.get('arguments')


def _accepted_values(entry: Dict[str, Any]) -> Optional[List[Any]]:
  for argument in entry.get('arguments') or []:
    accepted = argument.get('acceptedValues')
    if accepted is not None:
      return list(accepted)
  return None


def _normalize_accepted_value(value: Any) -> str:
  if isinstance(value, bool):
    return 'true' if value else 'false'
  return str(value)


def _commands_by_name(entries: Optional[List[Dict[str, Any]]]) -> Dict[str, Dict[str, Any]]:
  return {str(entry['name']): entry for entry in (entries or []) if 'name' in entry}


@lru_cache(maxsize=1)
def load_opencli_commands(path: Optional[str] = None) -> Dict[str, Dict[str, Any]]:
  opencli_path = Path(path) if path else OPENCLI_PATH
  try:
    with open(opencli_path, 'r') as fp:
      data = yaml.safe_load(fp)
  except OSError as e:
    raise ApplyConfigError(f"Failed to load OpenCLI description at {opencli_path}: {e}") from e
  except yaml.YAMLError as e:
    raise ApplyConfigError(f"Failed to parse OpenCLI description at {opencli_path}: {e}") from e

  if not isinstance(data, dict) or not isinstance(data.get('command'), dict):
    raise ApplyConfigError(f"Invalid OpenCLI description at {opencli_path}: missing command")

  return _commands_by_name(data['command'].get('commands'))


def _validate_option_values(
  prefix: str,
  key: str,
  value: Any,
  entry: Dict[str, Any],
  is_flag: bool,
) -> None:
  if is_flag:
    if not isinstance(value, bool):
      raise ApplyConfigError(f"{prefix}.options.{key} must be a boolean flag")
    return

  accepted = _accepted_values(entry)
  if accepted is None:
    return

  accepted_normalized = {_normalize_accepted_value(item) for item in accepted}
  values = value if isinstance(value, list) else [value]
  for item in values:
    if _normalize_accepted_value(item) not in accepted_normalized:
      allowed = ', '.join(str(v) for v in accepted)
      raise ApplyConfigError(
        f"{prefix}.options.{key} has invalid value {item!r}. Accepted values: {allowed}"
      )


def _action_segments(action: str) -> List[str]:
  return [segment for segment in str(action).split() if segment]


def _resolve_opencli_action(
  resource: str,
  action: str,
  opencli_commands: Dict[str, Dict[str, Any]],
) -> Dict[str, Any]:
  resource_spec = opencli_commands.get(str(resource))
  if resource_spec is None:
    raise ApplyConfigError(f"Unknown resource: {resource}")

  current_commands = _commands_by_name(resource_spec.get('commands'))
  if not current_commands:
    raise ApplyConfigError(f"Resource '{resource}' is not a command group")

  segments = _action_segments(action)
  if not segments:
    raise ApplyConfigError(f"Unknown action '{action}' for resource '{resource}'")

  action_spec: Optional[Dict[str, Any]] = None
  walked: List[str] = []
  for segment in segments:
    walked.append(segment)
    action_spec = current_commands.get(segment)
    if action_spec is None:
      walked_action = ' '.join(walked)
      raise ApplyConfigError(f"Unknown action '{walked_action}' for resource '{resource}'")
    nested = _commands_by_name(action_spec.get('commands'))
    if nested:
      current_commands = nested
    else:
      current_commands = {}

  assert action_spec is not None
  if _commands_by_name(action_spec.get('commands')):
    raise ApplyConfigError(f"Action '{action}' for resource '{resource}' is a group, not a command")

  return action_spec


def validate_command_step(step: Dict[str, Any], index: int, opencli_commands: Dict[str, Dict[str, Any]]) -> None:
  prefix = f"commands[{index}]"
  resource = step['resource']
  action = step['action']
  options = step['options']

  action_spec = _resolve_opencli_action(str(resource), str(action), opencli_commands)

  allowed: Dict[str, Tuple[Dict[str, Any], bool, bool]] = {}
  for argument in action_spec.get('arguments') or []:
    allowed[_cli_param_name(argument)] = (argument, False, bool(argument.get('required')))
  for option in action_spec.get('options') or []:
    allowed[_cli_param_name(option)] = (option, _is_flag_option(option), bool(option.get('required')))

  unknown = sorted(set(options) - set(allowed))
  if unknown:
    raise ApplyConfigError(f"{prefix}: Unknown options for command: {', '.join(unknown)}")

  for key, value in options.items():
    entry, is_flag, _required = allowed[key]
    _validate_option_values(prefix, key, value, entry, is_flag)

  missing = [
    key for key, (_entry, _is_flag, required) in allowed.items()
    if required and key not in options
  ]
  if missing:
    raise ApplyConfigError(
      f"{prefix} missing required option(s): {', '.join(sorted(missing))}"
    )


def validate_config(
  data: Dict[str, Any],
  opencli_path: Optional[str] = None,
) -> List[Dict[str, Any]]:
  if 'version' not in data:
    raise ApplyConfigError("Missing required property: version")

  version = data['version']
  if version not in SUPPORTED_VERSIONS:
    supported = ', '.join(str(v) for v in sorted(SUPPORTED_VERSIONS))
    raise ApplyConfigError(f"Unsupported version: {version}. Supported versions: {supported}")

  if 'commands' not in data:
    raise ApplyConfigError("Missing required property: commands")

  commands = data['commands']
  if not isinstance(commands, list) or len(commands) == 0:
    raise ApplyConfigError("commands must be a non-empty list")

  opencli_commands = load_opencli_commands(opencli_path)

  for index, step in enumerate(commands):
    if not isinstance(step, dict):
      raise ApplyConfigError(f"commands[{index}] must be a mapping")

    if 'resource' not in step:
      raise ApplyConfigError(f"commands[{index}] missing required property: resource")

    if 'action' not in step:
      raise ApplyConfigError(f"commands[{index}] missing required property: action")

    options = step.get('options', {})
    if options is None:
      options = {}
    if not isinstance(options, dict):
      raise ApplyConfigError(f"commands[{index}].options must be a mapping")

    step['options'] = options
    validate_command_step(step, index, opencli_commands)

  return commands


def expand_path_value(value: Any, config_dir: str) -> Any:
  if not isinstance(value, str):
    return value

  expanded = os.path.expanduser(value)
  if not os.path.isabs(expanded):
    expanded = os.path.normpath(os.path.join(config_dir, expanded))
  return expanded


def expand_options(options: Dict[str, Any], config_dir: str) -> Dict[str, Any]:
  expanded = {}
  for key, value in options.items():
    if key in PATH_OPTION_KEYS:
      if isinstance(value, list):
        expanded[key] = [expand_path_value(item, config_dir) for item in value]
      else:
        expanded[key] = expand_path_value(value, config_dir)
    else:
      expanded[key] = value
  return expanded


def resolve_command_path(
  scaffold_group: click.Group,
  resource: str,
  action: str,
) -> Tuple[List[click.Command], click.Command]:
  """Resolve nested Click path: scaffold → resource → action segments → leaf.

  Returns (intermediate_groups, leaf_command) where intermediate_groups starts
  with the resource group and includes any nested groups before the leaf.
  """
  resource_cmd = scaffold_group.commands.get(resource)
  if resource_cmd is None:
    raise ApplyConfigError(f"Unknown resource: {resource}")

  if not isinstance(resource_cmd, click.Group):
    raise ApplyConfigError(f"Resource '{resource}' is not a command group")

  segments = _action_segments(action)
  if not segments:
    raise ApplyConfigError(f"Unknown action '{action}' for resource '{resource}'")

  groups: List[click.Command] = [resource_cmd]
  current: click.Command = resource_cmd
  walked: List[str] = []

  for segment in segments:
    walked.append(segment)
    if not isinstance(current, click.Group):
      walked_action = ' '.join(walked)
      raise ApplyConfigError(f"Unknown action '{walked_action}' for resource '{resource}'")

    next_cmd = current.commands.get(segment)
    if next_cmd is None:
      walked_action = ' '.join(walked)
      raise ApplyConfigError(f"Unknown action '{walked_action}' for resource '{resource}'")

    current = next_cmd
    if isinstance(current, click.Group):
      groups.append(current)

  if isinstance(current, click.Group):
    raise ApplyConfigError(f"Action '{action}' for resource '{resource}' is a group, not a command")

  return groups, current


def resolve_command(scaffold_group: click.Group, resource: str, action: str) -> click.Command:
  _groups, leaf = resolve_command_path(scaffold_group, resource, action)
  return leaf


def _option_flag_name(param: click.Option) -> str:
  # Prefer long option names
  for opt in param.opts:
    if opt.startswith('--'):
      return opt
  return param.opts[0]


def options_to_argv(command: click.Command, options: Dict[str, Any]) -> Tuple[List[str], List[str]]:
  remaining = dict(options)
  argv: List[str] = []
  positionals: List[str] = []

  for param in command.params:
    if param.name not in remaining:
      continue

    value = remaining.pop(param.name)

    if isinstance(param, click.Argument):
      if value is None:
        continue
      if isinstance(value, list):
        positionals.extend(str(v) for v in value)
      else:
        positionals.append(str(value))
      continue

    if not isinstance(param, click.Option):
      continue

    flag = _option_flag_name(param)

    if param.is_flag:
      if value:
        argv.append(flag)
      continue

    if param.multiple:
      if value is None:
        continue
      values = value if isinstance(value, list) else [value]
      for item in values:
        argv.extend([flag, str(item)])
      continue

    if value is None:
      continue

    argv.extend([flag, str(value)])

  if remaining:
    unknown = ', '.join(sorted(remaining.keys()))
    raise ApplyConfigError(f"Unknown options for command: {unknown}")

  return argv, positionals


def _scaffold_parent_context(ctx: click.Context, scaffold_group: click.Group) -> click.Context:
  # Prefer the real scaffold group context so usage matches direct CLI invocation.
  # Fall back when apply is invoked without that parent (e.g. unit tests).
  if ctx.parent is not None and ctx.parent.command is scaffold_group:
    return ctx.parent
  return click.Context(scaffold_group, info_name=scaffold_group.name or 'scaffold', parent=ctx.parent)


def invoke_step(
  ctx: click.Context,
  scaffold_group: click.Group,
  resource: str,
  action: str,
  argv: List[str],
) -> None:
  scaffold_ctx = _scaffold_parent_context(ctx, scaffold_group)
  groups, leaf = resolve_command_path(scaffold_group, resource, action)

  # Parent chain must be scaffold → resource → … → leaf so Click usage/help shows
  # e.g. "stoobly-agent scaffold setting rewrite set", not nested under apply.
  parent_ctx = scaffold_ctx
  for group in groups:
    parent_ctx = click.Context(group, info_name=group.name, parent=parent_ctx)

  try:
    with leaf.make_context(leaf.name, argv, parent=parent_ctx) as cmd_ctx:
      leaf.invoke(cmd_ctx)
  except click.ClickException as e:
    e.show()
    raise SystemExit(e.exit_code) from e


def _is_init_section_step(step: Dict[str, Any]) -> bool:
  return str(step.get('resource') or '') in INIT_SECTION_RESOURCES


def _is_enable_action(step: Dict[str, Any]) -> bool:
  segments = _action_segments(str(step.get('action') or ''))
  return bool(segments) and segments[-1] == 'enable'


def sort_init_section_commands(commands: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
  """Keep non-init steps fixed; among setting/intercept steps, put enable last."""
  indices = [i for i, step in enumerate(commands) if _is_init_section_step(step)]
  if not indices:
    return commands

  subset = [commands[i] for i in indices]
  # Stable: non-enable first, enable last; relative order within each group preserved.
  subset_sorted = sorted(subset, key=lambda step: 1 if _is_enable_action(step) else 0)

  result = list(commands)
  for index, step in zip(indices, subset_sorted):
    result[index] = step
  return result


def apply_config(
  ctx: click.Context,
  scaffold_group: click.Group,
  path: str,
  format: str = YAML_FORMAT,
  dry_run: bool = False,
) -> None:
  logger = _logger()

  try:
    data = load_config(path, format)
    commands = validate_config(data)
  except ApplyConfigError as e:
    logger.error(f"{e}")
    sys.exit(1)
  except (json.JSONDecodeError, yaml.YAMLError) as e:
    logger.error(f"Failed to parse config file: {e}")
    sys.exit(1)
  except OSError as e:
    logger.error(f"Failed to read config file: {e}")
    sys.exit(1)

  commands = sort_init_section_commands(commands)
  config_dir = os.path.dirname(os.path.abspath(path))
  overwrite_init_section = True

  for index, step in enumerate(commands):
    resource = step['resource']
    action = step['action']
    options = expand_options(step.get('options') or {}, config_dir)

    if _is_init_section_step(step) and overwrite_init_section:
      options = {**options, 'overwrite': True}
      overwrite_init_section = False

    try:
      command = resolve_command(scaffold_group, str(resource), str(action))
      option_argv, positionals = options_to_argv(command, options)
    except ApplyConfigError as e:
      logger.error(f"commands[{index}]: {e}")
      sys.exit(1)

    prefix = 'would apply' if dry_run else 'applying'
    applying = f"{prefix} {resource} {action}"
    if positionals:
      applying = f"{applying} {' '.join(positionals)}"
    logger.info(applying)

    if dry_run:
      continue

    try:
      invoke_step(
        ctx,
        scaffold_group,
        str(resource),
        str(action),
        option_argv + positionals,
      )
    except SystemExit as e:
      code = e.code if isinstance(e.code, int) else (1 if e.code else 0)
      if code != 0:
        logger.error(f"commands[{index}] failed with exit code {code}")
        sys.exit(code)
