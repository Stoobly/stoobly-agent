import os
import shutil
import time

from filelock import FileLock
from stoobly_agent.lib.logger import Logger

from .app import App
from .constants import DOTENV_PATH_ENV, DOTENV_FILE, NAMESERVERS_FILE

LOG_ID = 'WorkflowNamespace'
FOLDER_COUNT_INTERVAL_SECONDS = 10  # Use folder counting if this much time has passed

class WorkflowNamespace():

  def __init__(self, app: App, namespace: str = None):
    self._app = app
    self._namespace = namespace
    self._path = os.path.join(app.data_dir.tmp_dir_path, namespace or '')

    if not os.path.exists(self._path):
      os.makedirs(self._path, exist_ok=True)

  @property
  def app(self):
    return self._app

  @property
  def dotenv_path(self):
    return os.path.join(self.path, DOTENV_FILE)

  @property
  def nameservers_path(self):
    return os.path.join(self.path, NAMESERVERS_FILE)

  @property
  def namespace(self):
    return self._namespace

  @property
  def path(self):
    return self._path

  @property
  def pid_file_extension(self):
    return '.pid'

  @property
  def run_script_path(self):
    return os.path.join(self.path, 'run.sh')

  @property
  def timestamp_file_extension(self):
    return '.timestamp'

  @property
  def traefik_config_path(self):
    return os.path.join(self.path, 'traefik.yml')

  def access_count(self, workflow_name: str):
    """Get the current access count from the lock file.
    
    Uses file locking to protect read operations. Returns the current count
    from the access file.
    
    This method should be used at the start of running a workflow to determine
    if non-thread safe operations, such as snapshot apply and config reset,
    should be done. These operations should only be performed when the access
    count is 1 (i.e., this is the first instance of the workflow).
    
    Args:
      workflow_name: Name of the workflow
      
    Returns:
      int: The current access count
    """
    lock_file_path = self.lock_file_path(workflow_name)
    file_lock = FileLock(lock_file_path)
    
    try:
      with file_lock:
        count, _ = self._read_access_file(workflow_name)
        return count
    except Exception as e:
      Logger.instance(LOG_ID).error(f"Failed to read lock file count: {e}")
      raise

  def access(self, workflow_name: str):
    """Access the lock file and increment the count.
    
    This method should be called when starting a workflow instance. It uses
    file locking to protect read/write operations and increments the access
    count.
    
    The count behavior depends on how much time has passed since the last
    update:
    - If less than 10 seconds has passed: increments the count value read
      from the access file
    - If 10 seconds or more has passed: counts existing workflow instances
      (folders with pid or timestamp files) and adds 1
    
    Args:
      workflow_name: Name of the workflow
    """
    lock_file_path = self.lock_file_path(workflow_name)
    file_lock = FileLock(lock_file_path)
    
    try:
      with file_lock:       
        current_time = time.time()
        
        # Read timestamp and count from access file
        current_count, timestamp = self._read_access_file(workflow_name)
        
        # Check how much time has passed since last update
        if current_time - timestamp >= FOLDER_COUNT_INTERVAL_SECONDS:
          # 10 seconds or more has passed, count folders in tmp path
          tmp_dir_path = self._app.data_dir.tmp_dir_path
          folder_count = 0

          if os.path.exists(tmp_dir_path):
            for folder in os.listdir(tmp_dir_path):
              folder_path = os.path.join(tmp_dir_path, folder)

              # Skip current namespace or else it will count itself twice
              if folder == self._namespace:
                continue
              
              # If the folder is not a directory, skip
              if not os.path.isdir(folder_path):
                continue
              
              # Check if pid file or timestamp file exists for workflow_name in this folder
              pid_file_name = f"{workflow_name}{self.pid_file_extension}"
              timestamp_file_name = f"{workflow_name}{self.timestamp_file_extension}"
              pid_file_path = os.path.join(folder_path, pid_file_name)
              timestamp_file_path = os.path.join(folder_path, timestamp_file_name)
              
              if os.path.exists(pid_file_path) or os.path.exists(timestamp_file_path):
                folder_count += 1

          count = folder_count + 1
        else:
          # Less than 10 seconds has passed, just increment the read count value
          count = current_count + 1
        
        # Write updated timestamp and count
        access_file_path = self.access_file_path(workflow_name)
        with open(access_file_path, 'w') as f:
          f.write(f"{timestamp}:{count}")
          
    except Exception as e:
      Logger.instance(LOG_ID).error(f"Failed to create/update lock file: {e}")
      raise

  def access_file_path(self, workflow_name: str):
    return os.path.join(self._app.data_dir.tmp_dir_path, f".{workflow_name}.access")

  def copy_dotenv(self):
    dotenv_path = os.environ.get(DOTENV_PATH_ENV) or '.env'

    if os.path.isfile(dotenv_path):
      shutil.copy(dotenv_path, self.dotenv_path)

  def lock_file_path(self, workflow_name: str):
    return os.path.join(self._app.data_dir.tmp_dir_path, f".{workflow_name}.lock")

  def log_file_path(self, workflow_name: str):
    """Get the path to the PID file for this workflow."""
    return os.path.join(self.path, f"{workflow_name}.log")

  def pid_file_path(self, workflow_name: str):
    """Get the path to the PID file for this workflow."""
    return os.path.join(self.path, f"{workflow_name}{self.pid_file_extension}")

  def release(self, workflow_name: str):
    """Release the lock file and decrement the count.
    
    Uses file locking to protect read/write operations. Each call decrements
    the count in the file. If the count reaches 0 or below, it stays at 0.
    
    Args:
      workflow_name: Name of the workflow
    """
    lock_file_path = self.lock_file_path(workflow_name)
    file_lock = FileLock(lock_file_path)
    
    try:
      with file_lock:
        current_count, timestamp = self._read_access_file(workflow_name)
        
        # Decrement count (but not below 0)
        count = max(0, current_count - 1)
        # Keep original timestamp
        
        # Write updated timestamp and count
        access_file_path = self.access_file_path(workflow_name)
        with open(access_file_path, 'w') as f:
          f.write(f"{timestamp}:{count}")
          
    except Exception as e:
      Logger.instance(LOG_ID).error(f"Failed to decrement lock file count: {e}")
      raise

  def remove_log_file(self, workflow_name: str):
    log_file_path = self.log_file_path(workflow_name)
    if os.path.exists(log_file_path):
      try:
        os.remove(log_file_path)
      except Exception as e:
        Logger.instance(LOG_ID).warning(f"Failed to remove log file: {e}")

  def remove_pid_file(self, workflow_name: str):
    pid_file_path = self.pid_file_path(workflow_name)
    if os.path.exists(pid_file_path):
      try:
        os.remove(pid_file_path)
      except Exception as e:
        Logger.instance(LOG_ID).warning(f"Failed to remove pid file: {e}")

  def remove_timestamp_file(self, workflow_name: str):
    timestamp_file_path = self.timestamp_file_path(workflow_name)
    if os.path.exists(timestamp_file_path):
      try:
        os.remove(timestamp_file_path)
      except Exception as e:
        Logger.instance(LOG_ID).warning(f"Failed to remove timestamp file: {e}")

  def timestamp_file_name(self, workflow_name: str):
    return f"{workflow_name}{self.timestamp_file_extension}"

  def timestamp_file_path(self, workflow_name: str):
    """Get the path to the timestamp file for this workflow."""
    return os.path.join(self.path, self.timestamp_file_name(workflow_name))

  def traefik_config_relative_path(self, path: str):
    if not path:
      return path
    return self.traefik_config_path.replace(path if path[len(path) - 1] == '/' else path + '/', '', 1)

  def _read_access_file(self, workflow_name: str):
    """Internal method to read lock file without locking.
    
    Args:
      workflow_name: Name of the workflow
      
    Returns:
      tuple: (count, timestamp) where count is int and timestamp is float
    """
    access_file_path = self.access_file_path(workflow_name)
    current_time = time.time()
    count = 0
    timestamp = current_time
    
    # Read existing lock file if it exists
    if os.path.exists(access_file_path):
      try:
        with open(access_file_path, 'r') as f:
          content = f.read().strip()
          if content:
            parts = content.split(':', 1)
            if len(parts) == 2:
              file_timestamp = float(parts[0])
              file_count = int(parts[1])
              count = file_count
              timestamp = file_timestamp
            else:
              # Invalid format, reset
              count = 0
              timestamp = current_time
      except (ValueError, IOError) as e:
        Logger.instance(LOG_ID).warning(f"Failed to read lock file: {e}, resetting count")
        count = 0
        timestamp = current_time
    else:
      # File doesn't exist, start with count 0
      count = 0
      timestamp = current_time
    
    return (count, timestamp)