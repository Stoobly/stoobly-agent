import os

from typing import List, Callable

from stoobly_agent.app.cli.helpers.set_rewrite_rule_service import set_rewrite_rule
from stoobly_agent.app.cli.scaffold.app_config import AppConfig
from stoobly_agent.app.cli.scaffold.workflow_run_command import WorkflowRunCommand
from stoobly_agent.app.settings import Settings
from stoobly_agent.config.constants import method, mode
from stoobly_agent.lib.api.keys.project_key import ProjectKey

def iter_commands(
  commands: List[WorkflowRunCommand],
  handle_before_entrypoint: Callable = None,
  handle_command: Callable = None,
  containerized: bool = False
):
  """
  Iterate through commands and process them.
  
  Args:
    commands: List of command objects to process
    handle_command: Callback function called for each command.
                   Receives (command,  public_directory_paths, response_fixtures_paths)
  """
  public_directory_paths = []
  response_fixtures_paths = []

  for command in commands:
    url = command.service_config.url
    if url:
      if os.path.exists(command.public_dir_path):
        public_directory_paths.append('--public-directory-path')

        if containerized:
          public_dir_path = os.path.relpath(command.public_dir_path, command.context_dir_path)
        else:
          public_dir_path = command.public_dir_path

        public_directory_paths.append(f"{public_dir_path}:{url}")

      if os.path.exists(command.response_fixtures_path):
        response_fixtures_paths.append('--response-fixtures-path')

        if containerized:
          response_fixtures_path = os.path.relpath(command.response_fixtures_path, command.context_dir_path)
        else:
          response_fixtures_path = command.response_fixtures_path

        response_fixtures_paths.append(f"{response_fixtures_path}:{url}")

  for command in commands:
    if handle_command:
      handle_command(command)

    upstream_hostname = command.service_config.upstream_hostname
    upstream_port = command.service_config.upstream_port
    upstream_scheme = command.service_config.upstream_scheme

    # If upstream hostname, port, scheme, or url is different from service hostname, port, scheme, or url,
    # update settings rewrite rules to rewrite url to upstream url
    if upstream_hostname != command.service_config.hostname or upstream_port != command.service_config.port or upstream_scheme != command.service_config.scheme:
      settings: Settings = Settings.instance()
      project_key = ProjectKey(settings.proxy.intercept.project_key)
      set_rewrite_rule(
        project_key.id,
        pattern=f'{command.service_config.url}/?.*?',
        method=[method.GET, method.PATCH, method.POST, method.PUT, method.DELETE, method.OPTIONS],
        mode=[mode.REPLAY],
        hostname=upstream_hostname,
        port=upstream_port,
        scheme=upstream_scheme
      )

    # If second from last command, run up_command i.e. right before entrypoint
    if len(commands) >= 2 and command == commands[-2]:
      if handle_before_entrypoint:
        handle_before_entrypoint(public_directory_paths, response_fixtures_paths)

def run_options(app_config: AppConfig, **extra_options):
  options = []

  # Add log level if provided
  if extra_options.get('log_level'):
    options.extend(['--log-level', extra_options['log_level']])
  
  options.extend(['--proxy-port', f"{app_config.proxy_port}"])
  options.extend(['--ui-port', f"{app_config.ui_port}"])
  options.extend(['--request-log-enable'])

  if extra_options.get('public_directory_paths'):
    options.extend(extra_options['public_directory_paths'])

  if extra_options.get('response_fixtures_paths'):
    options.extend(extra_options['response_fixtures_paths'])

  return options