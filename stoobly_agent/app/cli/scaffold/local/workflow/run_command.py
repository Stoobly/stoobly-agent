import os
import pdb
import shutil
import signal
import subprocess
import sys

from typing import Optional

from stoobly_agent.lib.logger import Logger
from stoobly_agent.app.cli.scaffold.workflow_run_command import WorkflowRunCommand
from stoobly_agent.app.cli.types.workflow_run_command import WorkflowUpOptions, WorkflowDownOptions, WorkflowLogsOptions

LOG_ID = 'LocalWorkflowRunCommand'

class LocalWorkflowRunCommand(WorkflowRunCommand):
  """Local workflow run command that executes stoobly-agent run directly."""

  def __init__(self, app, services=None, script=None, **kwargs):
    super().__init__(app, **kwargs)
    
    self.services = services or []
    self.script = script

    self._log_file_path = None
    self._pid_file_path = None

  @property
  def log_file_path(self):
    """Get the path to the PID file for this workflow."""
    if not self._log_file_path:
      self._log_file_path = os.path.join(self.workflow_namespace.path, f"{self.workflow_name}.log")
    return self._log_file_path

  @property
  def pid_file_path(self):
    """Get the path to the PID file for this workflow."""
    if not self._pid_file_path:
      self._pid_file_path = os.path.join(self.workflow_namespace.path, f"{self.workflow_name}.pid")
    return self._pid_file_path

  def _write_pid(self, pid: int):
    """Write the process PID to the PID file."""
    os.makedirs(os.path.dirname(self.pid_file_path), exist_ok=True)
    with open(self.pid_file_path, 'w') as f:
      f.write(str(pid))

  def _read_pid(self) -> Optional[int]:
    """Read the process PID from the PID file."""
    if not os.path.exists(self.pid_file_path):
      return None
    
    try:
      with open(self.pid_file_path, 'r') as f:
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

  def exec_service_step(self, **options: WorkflowUpOptions):
    set_env = 'set -a; . ./.env; set +a;'
    print_service_header = options.get('print_service_header')

    # Save current working directory
    cwd = os.getcwd()

    # iterate through each service in the workflow
    for service_name in self.services:
      if print_service_header:
        print_service_header(service_name)

      self.__write_service_env(service_name, **options)

      workflow_path = os.path.join(self.app.scaffold_namespace_path, service_name, self.workflow_name)

      # Absolute path to workflow .init script
      # e.g. stoobly_agent/app/cli/scaffold/templates/build/workflows/record/.init
      init_script_path = os.path.join(self.workflow_templates_build_dir, '.init')

      # Change directory to workflow path
      command = [set_env, init_script_path, 'init']
      if self.script:
        command = [f"cd {workflow_path};"] + command
      else:
        os.chdir(workflow_path)

      # Write the command to self.script_path
      if self.script:
        print(' '.join(command), file=self.script)
      else:
        result = subprocess.run(command, check=True)
        if result.returncode != 0:
          Logger.instance(LOG_ID).error(f"Failed to execute {init_script_path} for {service_name}")
          sys.exit(1)

      # Absolute path to workflow .configure script
      # e.g. stoobly_agent/app/cli/scaffold/templates/build/workflows/record/.configure
      configure_script_path = os.path.join(self.workflow_templates_build_dir, '.configure')

      # Change directory to workflow path
      command = [set_env, configure_script_path, 'configure']
      if self.script:
        command = [f"cd {workflow_path};"] + command
      else:
        os.chdir(workflow_path)

      # Write the command to self.script_path
      if self.script:
        print(' '.join(command), file=self.script)
      else:
        result = subprocess.run(command, check=True)
        if result.returncode != 0:
          Logger.instance(LOG_ID).error(f"Failed to execute {configure_script_path} for {service_name}")
          sys.exit(1)

    # Change directory back to cwd
    if self.script:
      print(f"cd {cwd}", file=self.script)
    else:
      os.chdir(cwd)

  def up(self, **options: WorkflowUpOptions):
    """Start the workflow using local stoobly-agent run."""
    detached = options.get('detached', False)

    self.exec_service_step(**options)
    
    # Check if PID file already exists
    if os.path.exists(self.pid_file_path):
      pid = self._read_pid()
      if pid and self._is_process_running(pid):
        Logger.instance(LOG_ID).error(f"Workflow {self.workflow_name} is already running with PID: {pid}")
        Logger.instance(LOG_ID).error(f"Use 'stoobly-agent scaffold workflow down {self.workflow_name}' to stop it first")
        sys.exit(1)
      else:
        # PID file exists but process is not running, clean it up
        os.remove(self.pid_file_path)
    
    # Build the stoobly-agent run command
    command = ['stoobly-agent', 'run']

    # Add log level if provided
    if options.get('log_level'):
      command.extend(['--log-level', options['log_level']])
    
    # Add detached mode if requested
    if detached:
      # Use the PID file path as the detached output file
      command.extend(['--detached', self.log_file_path])
    
    # Convert command to string
    command_str = ' '.join(command)
    
    if detached:
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
      else:
        # Execute directly
        try:
          # Run the command with --detached option
          result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True
          )
          
          # The --detached option prints the PID to stdout
          pid = int(result.stdout.strip())
          
          # Write PID to file
          self._write_pid(pid)
          
          Logger.instance(LOG_ID).info(f"Started {self.workflow_name} with PID: {pid}")
          
        except subprocess.CalledProcessError as e:
          Logger.instance(LOG_ID).error(f"Failed to start {self.workflow_name}: {e}")
          return None
        except ValueError as e:
          Logger.instance(LOG_ID).error(f"Failed to parse PID from output: {e}")
          return None
    else:
      # Run in foreground
      if self.script:
        print(command_str, file=self.script)
      else:
        # Execute directly
        try:
          subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
          Logger.instance(LOG_ID).error(f"Failed to start {self.workflow_name}: {e}")
          return None

  def down(self, **options: WorkflowDownOptions):
    """Stop the workflow by killing the local process."""
    
    pid = self._read_pid()
    if not pid:
      Logger.instance(LOG_ID).warning(f"No PID file found for {self.workflow_name}")
      return
    
    if not self._is_process_running(pid):
      Logger.instance(LOG_ID).info(f"Process {pid} for {self.workflow_name} is not running")
      # Clean up PID file
      if os.path.exists(self.pid_file_path):
        os.remove(self.pid_file_path)
      return
    
    # Kill the process
    if self.script:
      print(f"# Stop {self.workflow_name} (PID: {pid})", file=self.script)
      print(f"kill {pid} || true", file=self.script)
      print("sleep 1", file=self.script)
      print(f"kill -0 {pid} 2>/dev/null && kill {pid} || true", file=self.script)
      print(f"rm -f {self.pid_file_path}", file=self.script)
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
        
        # Clean up PID file
        if os.path.exists(self.pid_file_path):
          os.remove(self.pid_file_path)
          
      except Exception as e:
        Logger.instance(LOG_ID).error(f"Failed to stop {self.workflow_name}: {e}")

  def logs(self, **options: WorkflowLogsOptions):
    """Show logs for the local workflow process."""
    follow = options.get('follow', False)
    
    pid = self._read_pid()
    if not pid:
      Logger.instance(LOG_ID).warning(f"No PID file found for {self.workflow_name}")
      return
    
    if not self._is_process_running(pid):
      Logger.instance(LOG_ID).warning(f"Process {pid} for {self.workflow_name} is not running")
      return
    
    # Build log command
    log_file = f"{self.log_file_path}"
    if self.script:
      print(f"# Show logs for {self.workflow_name}", file=self.script)
      if follow:
        print(f"tail -f {log_file}", file=self.script)
      else:
        print(f"cat {log_file}", file=self.script)
    else:
      try:
        if follow:
          subprocess.run(['tail', '-f', log_file])
        else:
          subprocess.run(['cat', log_file])
      except subprocess.CalledProcessError as e:
        Logger.instance(LOG_ID).error(f"Failed to show logs for {self.workflow_name}: {e}")

  def status(self):
    """Check the status of the local workflow process."""
    pid = self._read_pid()
    if not pid:
      return "not running"
    
    if self._is_process_running(pid):
      return f"running (PID: {pid})"
    else:
      return "not running (stale PID file)"

  def __write_service_env(self, service_name: str, **options: WorkflowUpOptions):
      config = { **options }
      config['service_name'] = service_name
      command = LocalWorkflowRunCommand(self.app, **config)
      command.write_env(**options)
