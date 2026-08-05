import json
import logging
import os
import sys

from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import click
import yaml

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
  if logger.level == logging.NOTSET:
    level_name = (os.getenv(LOG_LEVEL) or INFO).lower()
    logger.setLevel(_LEVELS.get(level_name, logging.INFO))
  return logger

SUPPORTED_VERSIONS = {1}
YAML_FORMAT = 'yaml'
JSON_FORMAT = 'json'
APPLY_FORMATS = [YAML_FORMAT, JSON_FORMAT]

OPENCLI_PATH = Path(__file__).resolve().parent.parent / 'scaffold.opencli.yaml'

PATH_OPTION_KEYS = frozenset({
  'app_dir_path',
  'context_dir_path',
  'script_path',
  'ca_certs_dir_path',
  'certs_dir_path',
  'docker_socket_path',
})


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


def validate_command_step(step: Dict[str, Any], index: int, opencli_commands: Dict[str, Dict[str, Any]]) -> None:
  prefix = f"commands[{index}]"
  resource = step['resource']
  action = step['action']
  options = step['options']

  resource_spec = opencli_commands.get(str(resource))
  if resource_spec is None:
    raise ApplyConfigError(f"Unknown resource: {resource}")

  resource_commands = _commands_by_name(resource_spec.get('commands'))
  if not resource_commands:
    raise ApplyConfigError(f"Resource '{resource}' is not a command group")

  action_spec = resource_commands.get(str(action))
  if action_spec is None:
    raise ApplyConfigError(f"Unknown action '{action}' for resource '{resource}'")

  if _commands_by_name(action_spec.get('commands')):
    raise ApplyConfigError(f"Action '{action}' for resource '{resource}' is a group, not a command")

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


def resolve_command(scaffold_group: click.Group, resource: str, action: str) -> click.Command:
  resource_cmd = scaffold_group.commands.get(resource)
  if resource_cmd is None:
    raise ApplyConfigError(f"Unknown resource: {resource}")

  if not isinstance(resource_cmd, click.Group):
    raise ApplyConfigError(f"Resource '{resource}' is not a command group")

  action_cmd = resource_cmd.commands.get(action)
  if action_cmd is None:
    raise ApplyConfigError(f"Unknown action '{action}' for resource '{resource}'")

  if isinstance(action_cmd, click.Group):
    raise ApplyConfigError(f"Action '{action}' for resource '{resource}' is a group, not a command")

  return action_cmd


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
  command: click.Command,
  argv: List[str],
) -> None:
  resource_cmd = scaffold_group.commands[resource]
  scaffold_ctx = _scaffold_parent_context(ctx, scaffold_group)

  # Parent chain must be scaffold → resource → action so Click usage/help shows
  # e.g. "stoobly-agent scaffold app create", not "scaffold apply PATH create".
  resource_ctx = click.Context(resource_cmd, info_name=resource, parent=scaffold_ctx)
  try:
    with command.make_context(command.name, argv, parent=resource_ctx) as cmd_ctx:
      command.invoke(cmd_ctx)
  except click.ClickException as e:
    e.show()
    raise SystemExit(e.exit_code) from e


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

  config_dir = os.path.dirname(os.path.abspath(path))

  for index, step in enumerate(commands):
    resource = step['resource']
    action = step['action']
    options = expand_options(step.get('options') or {}, config_dir)

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
      invoke_step(ctx, scaffold_group, str(resource), command, option_argv + positionals)
    except SystemExit as e:
      code = e.code if isinstance(e.code, int) else (1 if e.code else 0)
      if code != 0:
        logger.error(f"commands[{index}] failed with exit code {code}")
        sys.exit(code)
