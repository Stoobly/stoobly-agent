import os
import shlex
import sys
from typing import Any, List

from stoobly_agent.app.cli.scaffold.constants import SERVICES_NAMESPACE
from stoobly_agent.app.cli.scaffold.templates.constants import CORE_BUILD_SERVICE_NAME, CUSTOM_INIT

SCAFFOLD_SETTINGS_DELIMITER_BEGIN = "##### STOOBLY SCAFFOLD SETTINGS BEGIN #####"
SCAFFOLD_SETTINGS_DELIMITER_END = "##### STOOBLY SCAFFOLD SETTINGS END #####"

SCAFFOLD_INTERCEPT_DELIMITER_BEGIN = "##### STOOBLY SCAFFOLD INTERCEPT BEGIN #####"
SCAFFOLD_INTERCEPT_DELIMITER_END = "##### STOOBLY SCAFFOLD INTERCEPT END #####"

# Options that belong to the scaffold CLI, not the emitted stoobly-agent command.
EXCLUDED_SCAFFOLD_KWARGS = frozenset({'workflow', 'app_dir_path'})
EXCLUDED_SETTING_KWARGS = EXCLUDED_SCAFFOLD_KWARGS


def build_init_path(app_data_dir_path: str, workflow_name: str) -> str:
  return os.path.join(
    app_data_dir_path,
    SERVICES_NAMESPACE,
    CORE_BUILD_SERVICE_NAME,
    workflow_name,
    CUSTOM_INIT,
  )


def list_build_workflows(app_data_dir_path: str) -> List[str]:
  """Return workflow names under the build service that have a custom init script."""
  build_path = os.path.join(
    app_data_dir_path,
    SERVICES_NAMESPACE,
    CORE_BUILD_SERVICE_NAME,
  )
  if not os.path.isdir(build_path):
    return []

  workflows = []
  for name in sorted(os.listdir(build_path)):
    init_path = os.path.join(build_path, name, CUSTOM_INIT)
    if os.path.isfile(init_path):
      workflows.append(name)
  return workflows


def resolve_workflows(app_data_dir_path: str, workflows) -> List[str]:
  """Use provided workflows, or all build workflows when none are specified."""
  if workflows:
    return list(workflows)
  return list_build_workflows(app_data_dir_path)


def build_setting_command(subgroup: str, kwargs: dict) -> str:
  """Rebuild `stoobly-agent setting <subgroup> set ...` from click kwargs."""
  parts = ['stoobly-agent', 'setting', subgroup, 'set']
  _append_kwargs_as_options(parts, kwargs, [
    'action',
    'component',
    'hostname',
    'method',
    'mode',
    'name',
    'path',
    'pattern',
    'port',
    'scheme',
    'type',
    'value',
  ])
  return ' '.join(parts)


def build_intercept_command(subcommand: str, kwargs: dict) -> str:
  """Rebuild `stoobly-agent intercept <subcommand> ...` from click kwargs."""
  parts = ['stoobly-agent', 'intercept', subcommand]

  if subcommand == 'set':
    _append_kwargs_as_options(parts, kwargs, [
      'mode',
      'order',
      'policy',
      'strategy',
    ])

  return ' '.join(parts)


def _append_kwargs_as_options(parts: List[str], kwargs: dict, option_order: List[str]) -> None:
  remaining = {
    key: value
    for key, value in kwargs.items()
    if key not in EXCLUDED_SCAFFOLD_KWARGS and value is not None and value != ()
  }

  for key in option_order:
    if key not in remaining:
      continue
    _append_option(parts, key, remaining.pop(key))

  for key in sorted(remaining.keys()):
    _append_option(parts, key, remaining[key])


def _append_option(parts: List[str], key: str, value: Any) -> None:
  option = f"--{key.replace('_', '-')}"

  if isinstance(value, (list, tuple)):
    for item in value:
      if item is None:
        continue
      parts.append(option)
      parts.append(shlex.quote(str(item)))
    return

  if isinstance(value, bool):
    if value:
      parts.append(option)
    return

  parts.append(option)
  parts.append(shlex.quote(str(value)))


def prepend_or_append_setting_command(init_path: str, command: str) -> None:
  """Prepend a SETTINGS marker block or append the command inside an existing block."""
  prepend_or_append_command(
    init_path,
    command,
    SCAFFOLD_SETTINGS_DELIMITER_BEGIN,
    SCAFFOLD_SETTINGS_DELIMITER_END,
  )


def prepend_or_append_intercept_command(init_path: str, command: str) -> None:
  """Prepend an INTERCEPT marker block or append the command inside an existing block."""
  prepend_or_append_command(
    init_path,
    command,
    SCAFFOLD_INTERCEPT_DELIMITER_BEGIN,
    SCAFFOLD_INTERCEPT_DELIMITER_END,
  )


def prepend_or_append_command(init_path: str, command: str, begin: str, end: str) -> None:
  """Prepend a marker block or append the command inside an existing block."""
  if not os.path.exists(init_path):
    print(f"Error: Init script not found at {init_path}", file=sys.stderr)
    sys.exit(1)

  with open(init_path, 'r') as fp:
    contents = fp.read()

  command_line = command if command.endswith('\n') else f"{command}\n"
  updated = _insert_command(contents, command_line, begin, end)

  with open(init_path, 'w') as fp:
    fp.write(updated)


def _insert_command(contents: str, command_line: str, begin: str, end: str) -> str:
  if begin in contents and end in contents:
    return _append_inside_markers(contents, begin, end, command_line)

  return _prepend_marker_block(contents, begin, end, command_line)


def _append_inside_markers(contents: str, begin: str, end: str, command_line: str) -> str:
  begin_index = contents.index(begin)
  end_index = contents.index(end, begin_index)

  before = contents[:end_index]
  after = contents[end_index:]

  if before and not before.endswith('\n'):
    before += '\n'

  return f"{before}{command_line}{after}"


def _prepend_marker_block(contents: str, begin: str, end: str, command_line: str) -> str:
  block = f"{begin}\n{command_line}{end}\n"

  lines = contents.splitlines(keepends=True)
  if lines and lines[0].startswith('#!'):
    shebang = lines[0]
    rest = ''.join(lines[1:])
    # Keep a blank line after shebang when the rest of the file is non-empty.
    if rest and not rest.startswith('\n'):
      rest = f"\n{rest}"
    elif not rest:
      rest = '\n'
    return f"{shebang}\n{block}{rest}" if not shebang.endswith('\n') else f"{shebang}{block}{rest}"

  if contents and not contents.endswith('\n'):
    contents = f"{contents}\n"

  if contents:
    return f"{block}\n{contents}"
  return block
