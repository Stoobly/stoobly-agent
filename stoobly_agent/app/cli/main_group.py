import click
import collections
import pdb

from functools import reduce
from typing import List, TypedDict

from stoobly_agent.app.settings import Settings

class CommandGroup(TypedDict):
  commands: List[str]
  name: str

class MainGroup(click.Group):

  def __init__(self, name=None, commands=None, **attrs):
    super(MainGroup, self).__init__(name, commands, **attrs)
    self.commands = commands or collections.OrderedDict()
    self.__settings = Settings.instance()

  def list_commands(self, ctx):
    return self.commands

  def format_commands(self, ctx, formatter):
    super().get_usage(ctx)

    command_groups: List[CommandGroup] = [
      {
        'name': 'Commands',
        'commands': ['ca-cert', 'config', 'dev-tools', 'exec', 'feature'],
      }  
    ]

    if self.__settings.features.get('remote'):
      command_groups.append({
        'name': 'Remote Commands',
        'commands': ['project', 'report', 'scenario', 'request', 'run'],
      })
    else:
      command_groups.append({
        'name': 'Local Commands',
        'commands': ['request', 'run'],
      })

    self.__print(formatter, command_groups)

  def __print(self, formatter, command_groups: List[CommandGroup]):
    command_names = reduce(lambda a, b: a['commands'] + b['commands'], command_groups)
    longest_length_command_length = len(max(command_names, key=len))

    for command_group in command_groups:
      command_names = command_group['commands']
      commands = self.__get_commands(command_names)

      if len(commands) == 0:
        continue

      with formatter.section(command_group['name']):
        for command in commands:
          gap_length = longest_length_command_length - len(command.name) + 2
          formatter.write_text(f"{command.name}{' ' * gap_length}{command.get_short_help_str()}")

  def __get_commands(self, command_names: List[str]):
    return list(filter(
      lambda c: c != None, 
      map(lambda c: self.commands.get(c), command_names)
    ))