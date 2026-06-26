import os

from typing import List, Callable

from stoobly_agent.app.cli.scaffold.app_config import AppConfig
from stoobly_agent.app.cli.scaffold.workflow_run_command import WorkflowRunCommand
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
    handle_before_entrypoint: Optional callback invoked once before the entrypoint
                              (on the second-to-last command). Receives
                              (public_directory_paths, response_fixtures_paths, openapi_specification_paths, lifecycle_hooks_paths).
    handle_command: Optional callback invoked for each command. Receives (command).
    containerized: Whether to compute relative paths for containerized runs.
  """
  lifecycle_hooks_paths = []
  openapi_specification_paths = []
  public_directory_paths = []
  response_fixtures_paths = []

  for command in commands:
    url = command.service_config.url
    if url:
      if os.path.exists(command.public_dir_path):
        public_directory_paths.append('--public-dir-path')

        if containerized:
          # denormalized paths are mounted as volumes in the container as normalized paths
          # Since this is containerized, use the normalized path 
          public_dir_path = os.path.relpath(
            command.normalize_path(command.public_dir_path),
            command.normalize_path(command.app.dir_path)
          )
        else:
          public_dir_path = command.public_dir_path

        public_directory_paths.append(f"{public_dir_path}:{url}")

      if os.path.exists(command.response_fixtures_path):
        response_fixtures_paths.append('--response-fixtures-path')

        if containerized:
          response_fixtures_path = os.path.relpath(
            command.normalize_path(command.response_fixtures_path),
            command.normalize_path(command.app.dir_path)
          )
        else:
          response_fixtures_path = command.response_fixtures_path

        response_fixtures_paths.append(f"{response_fixtures_path}:{url}")

      openapi_specification_path = command.openapi_specification_path
      if openapi_specification_path and os.path.exists(openapi_specification_path):
        openapi_specification_paths.append('--openapi-specification-path')

        if containerized:
          openapi_specification_path = os.path.relpath(
            command.normalize_path(openapi_specification_path),
            command.normalize_path(command.app.dir_path)
          )

        openapi_specification_paths.append(f"{openapi_specification_path}:{url}")

      # Resolve lifecycle hooks script path from command property
      lifecycle_hooks_path = command.lifecycle_hooks_path
      if os.path.exists(lifecycle_hooks_path):
        lifecycle_hooks_paths.append('--lifecycle-hooks-path')

        if containerized:
          relative_hooks_path = os.path.relpath(
            command.normalize_path(lifecycle_hooks_path),
            command.normalize_path(command.app.dir_path)
          )
        else:
          relative_hooks_path = lifecycle_hooks_path

        lifecycle_hooks_paths.append(f"{relative_hooks_path}:{url}")

  for command in commands:
    if handle_command:
      handle_command(command)

    # If second from last command, run up_command i.e. right before entrypoint
    if len(commands) >= 2 and command == commands[-2]:
      if handle_before_entrypoint:
        handle_before_entrypoint(
          lifecycle_hooks_paths,
          openapi_specification_paths,
          public_directory_paths,
          response_fixtures_paths,
        )

def run_options(app_config: AppConfig, **extra_options):
  """
  Base run options for forward proxy mode for local and docker runtimes.

  Args:
    app_config: AppConfig object
    extra_options: Extra options to add to the run options

  Returns:
    List of run options
  """
  options = []

  # Add log level if provided
  if extra_options.get('log_level'):
    options.extend(['--log-level', extra_options['log_level']])
  
  options.extend(['--proxy-port', f"{app_config.proxy_port}"])
  options.extend(['--ui-port', f"{app_config.ui_port}"])
  options.extend(['--request-log-enable'])
  options.extend(['--settings-watch'])
  options.extend(['--ssl-insecure']) # For local self-signed HTTPS services, insecure SSL/TLS certificates are allowed

  if extra_options.get('public_directory_paths'):
    options.extend(extra_options['public_directory_paths'])

  if extra_options.get('response_fixtures_paths'):
    options.extend(extra_options['response_fixtures_paths'])

  if extra_options.get('openapi_specification_paths'):
    options.extend(extra_options['openapi_specification_paths'])

  if extra_options.get('lifecycle_hooks_paths'):
    options.extend(extra_options['lifecycle_hooks_paths'])

  return options