import os
import pdb
import signal
import subprocess
import sys
import time

from types import FunctionType
from typing import Optional, List

from stoobly_agent.app.cli.scaffold.templates.constants import CORE_BUILD_SERVICE_NAME, CORE_ENTRYPOINT_SERVICE_NAME, CUSTOM_CONFIGURE, CUSTOM_INIT, CUSTOM_RUN, MAINTAINED_CONFIGURE, MAINTAINED_INIT, MAINTAINED_RUN
from stoobly_agent.app.cli.scaffold.workflow_run_command import WorkflowRunCommand
from stoobly_agent.app.cli.types.workflow_run_command import WorkflowUpOptions, WorkflowDownOptions, WorkflowLogsOptions
from stoobly_agent.app.cli.scaffold.run import iter_commands, run_options
from stoobly_agent.config.data_dir import DATA_DIR_NAME
from stoobly_agent.lib.logger import Logger

LOG_ID = 'LocalWorkflowRunCommand'

class LocalWorkflowRunCommand(WorkflowRunCommand):
  """Local workflow run command that executes stoobly-agent run directly."""

  def __init__(self, app, services=None, script=None, **kwargs):
    if not kwargs.get('service_name'):
      kwargs['service_name'] = CORE_ENTRYPOINT_SERVICE_NAME

    super().__init__(app, **kwargs)
    
    self.services = services or []
    self.script = script

    self._log_file_path = None
    self._pid_file_path = None

  @property
  def log_file_path(self):
    """Get the path to the PID file for this workflow."""
    if not self._log_file_path:
      self._log_file_path = self.workflow_namespace.log_file_path(self.workflow_name)
    return self._log_file_path

  @property
  def pid_file_extension(self):
    return self.workflow_namespace.pid_file_extension

  @property
  def pid_file_path(self):
    """Get the path to the PID file for this workflow."""
    if not self._pid_file_path:
      self._pid_file_path = self.workflow_namespace.pid_file_path(self.workflow_name)
    return self._pid_file_path

  def _read_pid(self, file_path = None) -> Optional[int]:
    """Read the process PID from the PID file."""
    file_path = file_path or self.pid_file_path
    if not os.path.exists(file_path):
      return None
    
    try:
      with open(file_path, 'r') as f:
        return int(f.read().strip())
    except (ValueError, IOError):
      return None

  def _kill_process(self, pid: int, signal_type=signal.SIGTERM):
    """Kill a process by PID."""
    try:
      os.kill(pid, signal_type)
      return True
    except (OSError, ProcessLookupError):
      return False

  def _is_process_running(self, pid: int) -> bool:
    """Check if a process is still running."""
    try:
      os.kill(pid, 0)  # Signal 0 doesn't kill the process, just checks if it exists
      return True
    except (OSError, ProcessLookupError):
      return False

  def exec_service_script(self, step_script_path: str, args: List[str], cwd = None):
    workflow_path = cwd or self.workflow_path

    # Change directory to workflow path
    command = [step_script_path] + args
    if self.script:
      command = [f"cd \"{workflow_path}\";"] + command

    # Write the command to self.script_path
    if self.script:
      print(' '.join(command), file=self.script)

    if self.dry_run:
      print(' '.join(command))
    else:
      result = subprocess.run(['sh', '-c', ' '.join(command)], cwd=workflow_path)
      if result.returncode != 0:
        sys.exit(1)

  def service_up(self, **options: WorkflowUpOptions):
    print_service_header = options.get('print_service_header')
    service_name = self.service_name
    workflow_template = self.workflow_template

    if print_service_header:
      print_service_header(service_name)

    self.write_env(**options)

    # If service is build or entrypoint, use path in templates/build/services/SERVICE_NAME/.init
    if service_name in [CORE_BUILD_SERVICE_NAME, CORE_ENTRYPOINT_SERVICE_NAME]:
      init_script_path = os.path.join(self.service_templates_root_dir, service_name, workflow_template, MAINTAINED_INIT)
      configure_script_path = os.path.join(self.service_templates_root_dir, service_name, workflow_template, MAINTAINED_CONFIGURE)
      run_script_path = os.path.join(self.workflow_path, MAINTAINED_RUN)
      
      if not os.path.exists(run_script_path):
        run_script_path = os.path.join(self.service_templates_root_dir, service_name, workflow_template, MAINTAINED_RUN)
    else:
      # Absolute path to workflow .init script
      # e.g. stoobly_agent/app/cli/scaffold/templates/build/workflows/record/.init
      init_script_path = os.path.join(self.workflow_templates_build_dir, MAINTAINED_INIT)

      # Absolute path to workflow .configure script
      # e.g. stoobly_agent/app/cli/scaffold/templates/build/workflows/record/.configure
      configure_script_path = os.path.join(self.workflow_templates_build_dir, MAINTAINED_CONFIGURE)

      run_script_path = os.path.join(self.workflow_templates_build_dir, MAINTAINED_RUN)

    self.exec_service_script(init_script_path, [CUSTOM_INIT])
    self.exec_service_script(configure_script_path, [CUSTOM_CONFIGURE])

    # Run script is the entrypoint, run in current working directory
    entrypoint_path = os.path.join(DATA_DIR_NAME, self.workflow_relative_path, CUSTOM_RUN)
    self.exec_service_script(run_script_path, [entrypoint_path], cwd=os.getcwd())

  def up(self, **options: WorkflowUpOptions):
    """Start the workflow using local stoobly-agent run."""
    detached = options.get('detached', False)

    if not self.dry_run:
      self.__iterate_active_workflows(handle_active=self.__handle_up_active, handle_stale=self.__handle_up_stale)
      self.context_lock.access()

    # iterate through each service in the workflow
    commands = self.workflow_service_commands(**options)
   
    def on_service_up(command):
      command.service_up(**options)

    def on_before_entrypoint(public_directory_paths, response_fixtures_paths):
      self.__up_command(public_directory_paths, response_fixtures_paths, **options)

    iter_commands(
      commands,
      handle_command=on_service_up,
      handle_before_entrypoint=on_before_entrypoint,
    )

  def down(self, **options: WorkflowDownOptions):
    """Stop the workflow by killing the local process."""

    # Intentially run this during dry run, we need the PID to be returned
    pid = self.__find_and_verify_workflow_pid()
    if not pid:
      return
    
    # Kill the process
    if self.script:
      self.__dry_run_down(pid, self.script)

    if self.dry_run:
      self.__dry_run_down(pid, sys.stdout)
    else:
      try:
        # Try graceful shutdown first with SIGTERM
        Logger.instance(LOG_ID).info(f"Sending SIGTERM to process {pid} for {self.workflow_name}")
        self._kill_process(pid, signal.SIGTERM)
 
        # Wait a bit for graceful shutdown
        import time
        time.sleep(2)
        
        # Check if process still exists
        if self._is_process_running(pid):
          Logger.instance(LOG_ID).info(f"Process {pid} still running, sending SIGKILL")
          self._kill_process(pid, signal.SIGKILL)
          
          # Wait a bit more for SIGKILL to take effect
          time.sleep(1)
          
          # Final check
          if self._is_process_running(pid):
            Logger.instance(LOG_ID).warning(f"Process {pid} may still be running after SIGKILL")
          else:
            Logger.instance(LOG_ID).info(f"Successfully stopped process {pid} for {self.workflow_name}")
        else:
          Logger.instance(LOG_ID).info(f"Successfully stopped process {pid} for {self.workflow_name}")

        self.__release()  
      except Exception as e:
        Logger.instance(LOG_ID).error(f"Failed to stop {self.workflow_name}: {e}")

    if self.app_config.copy_on_workflow_up:
      self.app.denormalize_down(
        self.workflow_namespace,
        dry_run=self.dry_run,
        script=self.script if self.script else sys.stdout
      )
      
  def logs(self, **options: WorkflowLogsOptions):
    """Show logs for the local workflow process."""
    follow = options.get('follow', False)

    if not self.dry_run:
      self.__find_and_verify_workflow_pid()
    
    # Build log command
    log_file = f"{self.log_file_path}"
    if self.script:
      self.__dry_run_logs(log_file, self.script, follow)

    if self.dry_run:
      self.__dry_run_logs(log_file, sys.stdout, follow)
    else:
      try:
        if follow:
          subprocess.run(['tail', '-f', log_file])
        else:
          subprocess.run(['cat', log_file])
      except subprocess.CalledProcessError as e:
        Logger.instance(LOG_ID).error(f"Failed to show logs for {self.workflow_name}: {e}")

  def workflow_service_commands(self, **options: WorkflowUpOptions):
    commands = list(map(lambda service_name: LocalWorkflowRunCommand(self.app, service_name=service_name, **options), self.services))
    commands.sort(key=lambda command: command.service_config.priority)
    return commands

  def __create_pid_file(self, pid: int):
    """Write the process PID to the PID file."""
    os.makedirs(os.path.dirname(self.pid_file_path), exist_ok=True)
    with open(self.pid_file_path, 'w') as f:
      f.write(str(pid))

  def __dry_run_down(self, pid: int, output_file: str):
    print(f"# Stop {self.workflow_name} (PID: {pid})", file=output_file)
    print(f"kill {pid} || true", file=output_file)
    print("sleep 1", file=output_file)
    print(f"kill -0 {pid} 2>/dev/null && kill {pid} || true", file=output_file)
    print(f"rm -f {self.pid_file_path}", file=output_file)

  def __dry_run_logs(self, log_file: str, output_file: str, follow: bool):
    print(f"# Show logs for {self.workflow_name}", file=output_file)
    if follow:
      print(f"tail -f {log_file}", file=output_file)
    else:
      print(f"cat {log_file}", file=output_file)

  def __find_and_verify_workflow_pid(self):
    # Find and verify the workflow PID
    pid = self._read_pid()

    if not pid:
      Logger.instance(LOG_ID).error(f"Workflow {self.workflow_name} is not running.")

      # If the workflow name does not match the workflow namespace, then recommend with --namespace option
      if self.workflow_name != self.workflow_namespace.namespace:
        Logger.instance(LOG_ID).error(f"Run `stoobly-agent scaffold workflow up {self.workflow_name} --namespace {self.workflow_namespace.namespace}` to start it first.")
      else:
        Logger.instance(LOG_ID).error(f"Run `stoobly-agent scaffold workflow up {self.workflow_name}` to start it first.")

      sys.exit(1)
    
    if not self._is_process_running(pid):
      Logger.instance(LOG_ID).info(f"Process {pid} for {self.workflow_name} is not running")
      if not self.dry_run:
        self.__release()
      return None

    return pid

  def __handle_up_active(self, folder: str, pid: str, pid_file_path: str):
    # Allow re-running the same workflow, bring workflow down first
    if pid_file_path == self.pid_file_path and os.path.exists(pid_file_path):
      self.down()
    else:
      file_name = os.path.basename(pid_file_path)
      workflow_name = self.workflow_name

      # If the folder is not the same as the workflow name, then the workflow is namespaced, get the real workflow name
      if folder != self.workflow_name:
        workflow_name = file_name.split(self.pid_file_extension)[0]

      # If the workflow is namespaced, allow it to run at the same time
      # Same workflow with same namespace is covered by pid_file_path check
      if workflow_name == self.workflow_name:
        return

      Logger.instance(LOG_ID).error(f"Workflow {workflow_name} is already running with PID {pid}")

      if folder != workflow_name:
        Logger.instance(LOG_ID).error(f"Run `stoobly-agent scaffold workflow down {workflow_name} --namespace {folder}` to stop it first.")
      else:
        Logger.instance(LOG_ID).error(f"Run `stoobly-agent scaffold workflow down {workflow_name}` to stop it first.")

      sys.exit(1)

  def __handle_up_stale(self, folder: str, pid: str, pid_file_path: str):
    # PID file exists but process is not running, clean it up
    os.remove(pid_file_path)

  def __iterate_active_workflows(self, **kwargs):
    handle_active: FunctionType = kwargs.get('handle_active')
    handle_stale: FunctionType = kwargs.get('handle_stale')
    tmp_dir_path = self.app.data_dir.tmp_dir_path

    # For each folder in self.app.data_dir.tmp_dir_path
    for folder in os.listdir(tmp_dir_path):
      folder_path = os.path.join(tmp_dir_path, folder)

      # If the folder is not a directory, skip
      if not os.path.isdir(folder_path):
        continue

      # For each file in folder_path that ends with .pid
      for file in os.listdir(folder_path):
        if not file.endswith(self.pid_file_extension):
          continue
          
        # If the folder contains a .pid file, then another workflow is running
        pid_file_path = os.path.join(folder_path, file)
        pid = self._read_pid(pid_file_path)
        if pid and self._is_process_running(pid):
          if handle_active:
            handle_active(folder, pid, pid_file_path)
        else:
          if handle_stale:
            handle_stale(folder, pid, pid_file_path)

  def __up_command(self, public_directory_paths: List[str], response_fixtures_paths: List[str], **options: WorkflowUpOptions):
    # Write .env before starting proxy so it can load WORKFLOW_NAME, etc.
    self.write_env(**options)

    # Build the stoobly-agent run command
    command = ['stoobly-agent', 'run']

    # Use the log file path as the detached output file
    command.extend(['--detached', self.log_file_path])

    options = run_options(
      self.app_config,
      log_level=options.get('log_level'),
      public_directory_paths=public_directory_paths,
      response_fixtures_paths=response_fixtures_paths,
    )

    command.extend(options)

    # Convert command to string
    command_str = ' '.join(command)

    # Run in background using the main run command's --detached option
    if self.script:
      # Write to script for detached execution
      script_lines = [
        f"# Start {self.workflow_name} in background using --detached",
        f"{command_str} > {self.pid_file_path}",
        f"echo \"Started {self.workflow_name} with PID: $(cat {self.pid_file_path})\""
      ]
      for line in script_lines:
        print(line, file=self.script)

    if self.dry_run or self.app.containerized:
      print(command_str)
    else:
      # Execute directly
      try:
        # Run the command with --detached option
        result = subprocess.run(
          command,
          capture_output=True,
          text=True,
          cwd=self.workflow_path,
        )

        # Provide some time for the process to start
        time.sleep(0.5)

        if result.returncode != 0:
          self.__handle_up_error()

        # The --detached option prints the PID to stdout
        pid = int(result.stdout.strip())

        if not self._is_process_running(pid):
          self.__handle_up_error()

        # Write PID to file
        self.__create_pid_file(pid)

        Logger.instance(LOG_ID).info(f"Started {self.workflow_name} with PID: {pid}")
      except subprocess.CalledProcessError as e:
        self.__handle_up_error()
      except ValueError as e:
        Logger.instance(LOG_ID).error(f"Failed to parse PID from output: {e}")
        self.__handle_up_error()

  def __handle_up_error(self):
    if not self.dry_run:
      self.__release()

    log_file = f"{self.log_file_path}"
    # Read log file it exists and print to stderr
    if os.path.exists(log_file):
      with open(log_file, 'r') as f:
        print(f.read(), file=sys.stderr)
    sys.exit(1)

  def __release(self):
    self.workflow_namespace.remove_pid_file(self.workflow_name)
    self.context_lock.release()