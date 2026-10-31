"""Validate OpenCLI YAML contracts against live Click interfaces.

OpenCLI documents the full contract including feature-gated (local/remote) options,
so it may be a *superset* of the Click tree in the current process. Every Click
command/option/argument must still appear in OpenCLI.
"""

from typing import Any, Dict, Iterable, List, Optional, Tuple

import click
import pytest
import yaml

from stoobly_agent.app.cli.endpoint_cli import endpoint
from stoobly_agent.app.cli.helpers.opencli_resolve import list_groups, resolve_path
from stoobly_agent.app.cli.intercept_cli import intercept
from stoobly_agent.app.cli.request_cli import request
from stoobly_agent.app.cli.scenario_cli import scenario
from stoobly_agent.app.cli.setting_cli import setting
from stoobly_agent.app.cli.snapshot_cli import snapshot

# Groups with OpenCLI contracts (scaffold keeps its dedicated docker-aware test).
OPENCLI_CLICK_GROUPS = {
  'endpoint': endpoint,
  'intercept': intercept,
  'request': request,
  'scenario': scenario,
  'setting': setting,
  'snapshot': snapshot,
}


def _kebab_to_snake(name: str) -> str:
  return name.replace('-', '_')


def _load_opencli(group: str) -> Dict[str, Any]:
  with open(resolve_path(group), 'r') as fp:
    data = yaml.safe_load(fp)
  assert isinstance(data, dict), 'OpenCLI root must be a mapping'
  assert data.get('opencli') == '0.1'
  assert isinstance(data.get('command'), dict)
  return data


def _walk_opencli_commands(
  cmd: Dict[str, Any],
  path: Tuple[str, ...] = (),
) -> Iterable[Tuple[Tuple[str, ...], Dict[str, Any]]]:
  name = cmd['name']
  current = path + (name,)
  children = cmd.get('commands') or []
  if children:
    yield current, cmd
    for child in children:
      yield from _walk_opencli_commands(child, current)
  else:
    yield current, cmd


def _resolve_click(root: click.Group, path: Tuple[str, ...]) -> Optional[click.Command]:
  cmd: click.Command = root
  for part in path[1:]:
    if not isinstance(cmd, click.Group):
      return None
    next_cmd = cmd.commands.get(part)
    if next_cmd is None:
      return None
    cmd = next_cmd
  return cmd


def _click_choice_values(param: click.Parameter) -> Optional[List[str]]:
  if isinstance(param.type, click.Choice):
    return list(param.type.choices)
  return None


def _opencli_accepted_values(entry: Dict[str, Any]) -> Optional[List[Any]]:
  if 'acceptedValues' in entry:
    return list(entry['acceptedValues'])
  for argument in entry.get('arguments') or []:
    if 'acceptedValues' in argument:
      return list(argument['acceptedValues'])
  return None


def _is_opencli_flag(option: Dict[str, Any]) -> bool:
  return not option.get('arguments')


def _bool_accepted_values(accepted: List[Any]) -> bool:
  return {str(v).lower() for v in accepted} == {'true', 'false'}


def _opencli_aliases(entry: Dict[str, Any]) -> List[str]:
  return [str(a) for a in (entry.get('aliases') or [])]


def _click_short_aliases(option: click.Option) -> List[str]:
  aliases = []
  for opt in option.opts:
    if opt.startswith('--'):
      continue
    if opt.startswith('-') and len(opt) == 2:
      aliases.append(opt[1:])
    else:
      aliases.append(opt.lstrip('-'))
  return aliases


def _compare_leaf(path: Tuple[str, ...], opencli_cmd: Dict[str, Any], click_cmd: click.Command) -> List[str]:
  """Require Click params ⊆ OpenCLI; allow OpenCLI-only (feature-gated) extras."""
  label = ' '.join(path)
  errors: List[str] = []

  if isinstance(click_cmd, click.Group):
    errors.append(f"{label}: OpenCLI leaf is a Click group")
    return errors

  opencli_args = {
    _kebab_to_snake(arg['name']): arg
    for arg in (opencli_cmd.get('arguments') or [])
    if 'name' in arg
  }
  opencli_opts = {
    _kebab_to_snake(opt['name']): opt
    for opt in (opencli_cmd.get('options') or [])
    if 'name' in opt
  }

  click_args = {p.name: p for p in click_cmd.params if isinstance(p, click.Argument)}
  click_opts = {p.name: p for p in click_cmd.params if isinstance(p, click.Option)}

  for name in sorted(set(click_args) - set(opencli_args)):
    errors.append(f"{label}: Click argument '{name}' missing in OpenCLI")
  for name in sorted(set(click_opts) - set(opencli_opts)):
    errors.append(f"{label}: Click option '{name}' missing in OpenCLI")

  for name, click_arg in click_args.items():
    oc_arg = opencli_args.get(name)
    if oc_arg is None:
      continue

    oc_required = bool(oc_arg.get('required', False))
    if bool(click_arg.required) != oc_required:
      errors.append(
        f"{label}: argument '{name}' required OpenCLI={oc_required} Click={click_arg.required}"
      )

    accepted = _opencli_accepted_values(oc_arg)
    choices = _click_choice_values(click_arg)
    if accepted is not None and choices is not None and set(map(str, accepted)) != set(map(str, choices)):
      errors.append(
        f"{label}: argument '{name}' acceptedValues OpenCLI={accepted} Click={choices}"
      )

  for name, click_opt in click_opts.items():
    oc_opt = opencli_opts.get(name)
    if oc_opt is None:
      continue

    oc_flag = _is_opencli_flag(oc_opt)
    if oc_flag != click_opt.is_flag:
      errors.append(
        f"{label}: option '{name}' flag OpenCLI={oc_flag} Click.is_flag={click_opt.is_flag}"
      )

    oc_required = bool(oc_opt.get('required', False))
    if oc_required and not click_opt.required:
      errors.append(
        f"{label}: option '{name}' required OpenCLI=True Click={click_opt.required}"
      )

    oc_hidden = bool(oc_opt.get('hidden', False))
    click_hidden = bool(click_opt.hidden)
    if oc_hidden != click_hidden:
      errors.append(
        f"{label}: option '{name}' hidden OpenCLI={oc_hidden} Click={click_hidden}"
      )

    accepted = _opencli_accepted_values(oc_opt)
    choices = _click_choice_values(click_opt)
    if accepted is not None and choices is not None:
      if set(map(str, accepted)) != set(map(str, choices)):
        errors.append(
          f"{label}: option '{name}' acceptedValues OpenCLI={accepted} Click={choices}"
        )
    elif accepted is not None and choices is None:
      if not (_bool_accepted_values(accepted) and click_opt.type.name == 'boolean'):
        errors.append(
          f"{label}: option '{name}' acceptedValues {accepted} but Click type is {click_opt.type}"
        )

    oc_aliases = set(_opencli_aliases(oc_opt))
    click_aliases = set(_click_short_aliases(click_opt))
    if oc_aliases != click_aliases:
      errors.append(
        f"{label}: option '{name}' aliases OpenCLI={sorted(oc_aliases)} Click={sorted(click_aliases)}"
      )

  return errors


@pytest.mark.parametrize('group', sorted(OPENCLI_CLICK_GROUPS.keys()))
class TestOpencliInterface:
  def test_opencli_file_exists(self, group: str):
    assert resolve_path(group).is_file()

  def test_root_command_matches_click_group(self, group: str):
    opencli = _load_opencli(group)
    root = opencli['command']
    click_root = OPENCLI_CLICK_GROUPS[group]
    assert root['name'] == group
    assert isinstance(click_root, click.Group)
    assert (click_root.name or group) == group

  def test_click_interfaces_covered_by_opencli(self, group: str):
    opencli = _load_opencli(group)
    click_root = OPENCLI_CLICK_GROUPS[group]
    errors: List[str] = []

    opencli_by_path = {path: cmd for path, cmd in _walk_opencli_commands(opencli['command'])}

    # Every Click command path must exist in OpenCLI.
    def walk_click(cmd: click.Command, path: Tuple[str, ...]):
      nonlocal errors
      label = ' '.join(path)
      opencli_cmd = opencli_by_path.get(path)
      if opencli_cmd is None:
        errors.append(f"{label}: Click command missing in OpenCLI")
        return

      if isinstance(cmd, click.Group):
        opencli_children = {child['name'] for child in (opencli_cmd.get('commands') or []) if 'name' in child}
        for name, child in cmd.commands.items():
          if name not in opencli_children:
            errors.append(f"{label}: Click subcommand '{name}' missing in OpenCLI")
          walk_click(child, path + (name,))
      else:
        errors.extend(_compare_leaf(path, opencli_cmd, cmd))

    walk_click(click_root, (group,))
    assert not errors, f'{group} OpenCLI / Click interface drift:\n' + '\n'.join(errors)


class TestOpencliRegistry:
  def test_new_groups_registered(self):
    groups = set(list_groups())
    assert set(OPENCLI_CLICK_GROUPS) <= groups
