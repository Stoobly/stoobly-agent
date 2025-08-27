import os
import pdb
import subprocess
import signal

from typing import List, TypedDict, Callable, Optional

from ...workflow_run_command import WorkflowRunCommand
from ...workflow_namesapce import WorkflowNamespace
from ...constants import WORKFLOW_NAME_ENV, WORKFLOW_NAMESPACE_ENV
from stoobly_agent.lib.logger import Logger

LOG_ID = 'LocalWorkflowRunCommand'

class LocalWorkflowUpOptions(TypedDict, total=False):
  workflow_namespace: str
  print_service_header: Optional[Callable[[str], None]]
  detached: bool
  # CLI-specific options that get passed through
  containerized: bool
  dry_run: bool
  log_level: str
  script_path: Optional[str]
  service: List[str]

class LocalWorkflowDownOptions(TypedDict, total=False):
  workflow_namespace: str
  print_service_header: Optional[Callable[[str], None]]
  # CLI-specific options that get passed through
  containerized: bool
  dry_run: bool
  log_level: str
  script_path: Optional[str]
  service: List[str]

class LocalWorkflowLogsOptions(TypedDict, total=False):
  print_service_header: Optional[Callable[[str], None]]
  follow: bool
  # CLI-specific options that get passed through
  containerized: bool
  dry_run: bool
  log_level: str
  script_path: Optional[str]
  service: List[str]
  workflow_namespace: str

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
      namespace = WorkflowNamespace(self.app, self.workflow_name)
      self._log_file_path = os.path.join(namespace.path, f"{self.workflow_name}.log")
    return self._log_file_path

  @property
  def pid_file_path(self):
    """Get the path to the PID file for this workflow."""
    if not self._pid_file_path:
      namespace = WorkflowNamespace(self.app, self.workflow_name)
      self._pid_file_path = os.path.join(namespace.path, f"{self.workflow_name}.pid")
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

  def up(self, **options: LocalWorkflowUpOptions):
    """Start the workflow using local stoobly-agent run."""
    detached = options.get('detached', False)
    
    # Build the stoobly-agent run command
    command = ['poetry', 'run', '--directory', '/home/jvlarble/github/stoobly-agent.2' ,'stoobly-agent', 'run']

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
          f"PID=$(cat {self.pid_file_path})",
          f"echo \"Started {self.workflow_name} with PID: $PID\""
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
        print(f"# Start {self.workflow_name} in foreground", file=self.script)
        print(command_str, file=self.script)
      else:
        # Execute directly
        try:
          subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
          Logger.instance(LOG_ID).error(f"Failed to start {self.workflow_name}: {e}")
          return None

  def down(self, **options: LocalWorkflowDownOptions):
    """Stop the workflow by killing the local process."""
    print_service_header = options.get('print_service_header')
    
    if print_service_header:
      print_service_header(self.workflow_name)
    
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
      print(f"rm -f {self.pid_file_path}", file=self.script)
    else:
      try:
        # Try graceful shutdown first
        if self._kill_process(pid, signal.SIGTERM):
          Logger.instance(LOG_ID).info(f"Sent SIGTERM to process {pid} for {self.workflow_name}")
          
          # Wait a bit for graceful shutdown
          import time
          time.sleep(2)
          
          # If still running, force kill
          if self._is_process_running(pid):
            if self._kill_process(pid, signal.SIGKILL):
              Logger.instance(LOG_ID).info(f"Sent SIGKILL to process {pid} for {self.workflow_name}")
        
        # Clean up PID file
        if os.path.exists(self.pid_file_path):
          os.remove(self.pid_file_path)
          
      except Exception as e:
        Logger.instance(LOG_ID).error(f"Failed to stop {self.workflow_name}: {e}")

  def logs(self, **options: LocalWorkflowLogsOptions):
    """Show logs for the local workflow process."""
    print_service_header = options.get('print_service_header')
    follow = options.get('follow', False)
    
    if print_service_header:
      print_service_header(self.workflow_name)
    
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
