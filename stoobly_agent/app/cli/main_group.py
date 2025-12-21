import click
import collections

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
    # Cache for lazily loaded commands
    self.__loaded_commands = {}

  def list_commands(self, ctx):
    # Return all available command names for help/autocomplete
    # Commands defined in cli.py itself are already in self.commands
    base_commands = list(self.commands.keys())
    
    # Add lazy-loadable commands
    lazy_commands = [
      'ca-cert', 'config', 'endpoint', 'feature', 'intercept',
      'request', 'scaffold', 'scenario', 'snapshot'
    ]
    
    if self.__settings.cli.features.dev_tools:
      lazy_commands.append('dev-tools')
    
    if self.__settings.cli.features.remote:
      lazy_commands.extend(['project', 'report', 'trace'])
    
    # Combine and deduplicate
    all_commands = list(set(base_commands + lazy_commands))
    return sorted(all_commands)

  def get_command(self, ctx, name):
    # First check if command is already loaded
    if name in self.commands:
      return self.commands.get(name)
    
    # Check if we've already loaded it lazily
    if name in self.__loaded_commands:
      return self.__loaded_commands[name]
    
    # Lazy load the command
    command = self.__lazy_load_command(name)
    if command:
      self.__loaded_commands[name] = command
      return command
    
    return None

  def __lazy_load_command(self, name: str):
    """Lazy load a command module only when it's requested."""
    command_map = {
      'ca-cert': ('ca_cert_cli', 'ca_cert'),
      'config': ('config_cli', 'config'),
      'endpoint': ('endpoint_cli', 'endpoint'),
      'feature': ('feature_cli', 'feature'),
      'intercept': ('intercept_cli', 'intercept'),
      'request': ('request_cli', 'request'),
      'scaffold': ('scaffold_cli', 'scaffold'),
      'scenario': ('scenario_cli', 'scenario'),
      'snapshot': ('snapshot_cli', 'snapshot'),
    }
    
    if self.__settings.cli.features.dev_tools and name == 'dev-tools':
      command_map['dev-tools'] = ('dev_tools_cli', 'dev_tools')
    
    if self.__settings.cli.features.remote:
      if name == 'project':
        command_map['project'] = ('project_cli', 'project')
      elif name == 'report':
        command_map['report'] = ('report_cli', 'report')
      elif name == 'trace':
        command_map['trace'] = ('trace_cli', 'trace')
    
    if name not in command_map:
      return None
    
    module_name, command_name = command_map[name]
    try:
      module = __import__(f'stoobly_agent.app.cli.{module_name}', fromlist=[command_name])
      return getattr(module, command_name)
    except (ImportError, AttributeError):
      return None

  def format_commands(self, ctx, formatter):
    super().get_usage(ctx)

    command_groups: List[CommandGroup] = [
      {
        'name': 'Commands',
        'commands': ['dev-tools', 'exec', 'init', 'mock', 'record', 'scaffold'],
      },
      {
        'name': 'Proxy Commands',
        'commands': ['ca-cert', 'config', 'intercept', 'run'],
      },
      {
        'name': 'Resource Commands',
        'commands': ['endpoint' , 'request', 'scenario', 'snapshot'],
      },
    ]

    if self.__settings.cli.features.remote:
      command_groups.append({
        'name': 'Remote Resource Commands',
        'commands': ['project', 'report', 'trace'],
      })

    self.__print(formatter, command_groups)

  def __print(self, formatter, command_groups: List[CommandGroup]):
    command_names = []
    for command_group in command_groups:
      command_names += command_group['commands']

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
    # Load commands lazily if needed for help display
    commands = []
    for name in command_names:
      cmd = self.get_command(None, name)
      if cmd:
        commands.append(cmd)
    return commands
