"""Validate scaffold Click interfaces against scaffold.opencli.yaml."""

from typing import Any, Dict, Iterable, List, Optional, Tuple

import click
import pytest
import yaml

from stoobly_agent.app.cli.scaffold.apply_command import OPENCLI_PATH, _kebab_to_snake
from stoobly_agent.app.cli.scaffold_cli import scaffold


def _load_opencli() -> Dict[str, Any]:
  with open(OPENCLI_PATH, 'r') as fp:
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


def _resolve_click(path: Tuple[str, ...]) -> Optional[click.Command]:
  assert path[0] == 'scaffold'
  cmd: click.Command = scaffold
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

  for name in sorted(set(opencli_args) - set(click_args)):
    errors.append(f"{label}: OpenCLI argument '{name}' missing in Click")
  for name in sorted(set(click_args) - set(opencli_args)):
    errors.append(f"{label}: Click argument '{name}' missing in OpenCLI")
  for name in sorted(set(opencli_opts) - set(click_opts)):
    errors.append(f"{label}: OpenCLI option '{name}' missing in Click")
  for name in sorted(set(click_opts) - set(opencli_opts)):
    errors.append(f"{label}: Click option '{name}' missing in OpenCLI")

  for name, oc_arg in opencli_args.items():
    click_arg = click_args.get(name)
    if click_arg is None:
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

  for name, oc_opt in opencli_opts.items():
    click_opt = click_opts.get(name)
    if click_opt is None:
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
    if oc_hidden != bool(click_opt.hidden):
      errors.append(
        f"{label}: option '{name}' hidden OpenCLI={oc_hidden} Click={click_opt.hidden}"
      )

    accepted = _opencli_accepted_values(oc_opt)
    choices = _click_choice_values(click_opt)
    if accepted is not None and choices is not None:
      if set(map(str, accepted)) != set(map(str, choices)):
        errors.append(
          f"{label}: option '{name}' acceptedValues OpenCLI={accepted} Click={choices}"
        )
    elif accepted is not None and choices is None:
      # Non-flag bool options are documented with true/false accepted values.
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


class TestScaffoldOpencliInterface:
  @pytest.fixture(scope='class')
  def opencli(self):
    return _load_opencli()

  def test_opencli_file_exists(self):
    assert OPENCLI_PATH.is_file(), f"Missing OpenCLI description at {OPENCLI_PATH}"

  def test_root_command_matches_scaffold_group(self, opencli: Dict[str, Any]):
    root = opencli['command']
    assert root['name'] == 'scaffold'
    assert isinstance(scaffold, click.Group)
    assert (scaffold.name or 'scaffold') == 'scaffold'

  def test_command_tree_and_interfaces_match_click(self, opencli: Dict[str, Any]):
    errors: List[str] = []

    for path, opencli_cmd in _walk_opencli_commands(opencli['command']):
      click_cmd = _resolve_click(path)
      label = ' '.join(path)

      if click_cmd is None:
        errors.append(f"{label}: missing in Click")
        continue

      children = opencli_cmd.get('commands') or []
      if children:
        if not isinstance(click_cmd, click.Group):
          errors.append(f"{label}: OpenCLI group is not a Click group")
          continue

        opencli_children = {child['name'] for child in children if 'name' in child}
        click_children = set(click_cmd.commands.keys())
        for name in sorted(opencli_children - click_children):
          errors.append(f"{label}: OpenCLI subcommand '{name}' missing in Click")
        for name in sorted(click_children - opencli_children):
          errors.append(f"{label}: Click subcommand '{name}' missing in OpenCLI")
      else:
        errors.extend(_compare_leaf(path, opencli_cmd, click_cmd))

    assert not errors, 'OpenCLI / Click interface drift:\n' + '\n'.join(errors)
