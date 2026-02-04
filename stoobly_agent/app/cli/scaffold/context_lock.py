import hashlib
import os
import time

from filelock import FileLock
from stoobly_agent.lib.logger import Logger

from .app import App

LOG_ID = 'ContextLock'
FOLDER_COUNT_INTERVAL_SECONDS = 10  # Use folder counting if this much time has passed

class ContextLock:
  """Manages access locking for workflow contexts based on app context data directory."""

  def __init__(self, app: App):
    self._app = app
    # Generate filename using hash of context_data_dir.path
    context_path = app.host_context_dir_path
    self._filename_hash = hashlib.md5(context_path.encode()).hexdigest()

  @property
  def app(self):
    return self._app

  def access_count(self):
    """Get the current access count from the lock file.
    
    Uses file locking to protect read operations. Returns the current count
    from the access file.
    
    This method should be used at the start of running a workflow to determine
    if non-thread safe operations, such as snapshot apply and config reset,
    should be done. These operations should only be performed when the access
    count is 1 (i.e., this is the first instance of the workflow).
    
    Returns:
      int: The current access count
    """
    lock_file_path = self.lock_file_path()
    file_lock = FileLock(lock_file_path)
    
    try:
      with file_lock:
        count, _ = self._read_access_file()
        return count
    except Exception as e:
      Logger.instance(LOG_ID).error(f"Failed to read lock file count: {e}")
      raise

  def access(self):
    """Access the lock file and increment the count.
    
    This method should be called when starting a workflow instance. It uses
    file locking to protect read/write operations and increments the access
    count.
    
    The count behavior depends on how much time has passed since the last
    update:
    - If less than 10 seconds has passed: increments the count value read
      from the access file
    - If 10 seconds or more has passed: reset the count
    """
    lock_file_path = self.lock_file_path()
    file_lock = FileLock(lock_file_path)
    
    try:
      with file_lock:       
        current_time = time.time()
        
        # Read timestamp and count from access file
        current_count, timestamp = self._read_access_file()
        
        # Check how much time has passed since last update
        if current_time - timestamp >= FOLDER_COUNT_INTERVAL_SECONDS:
          # 10 seconds or more has passed, reset the count
          current_count = 0

        count = current_count + 1
        
        # Write updated timestamp and count
        access_file_path = self.access_file_path()
        with open(access_file_path, 'w') as f:
          f.write(f"{current_time}:{count}")
          
    except Exception as e:
      Logger.instance(LOG_ID).error(f"Failed to create/update lock file: {e}")
      raise

  def access_file_path(self):
    """Get the path to the access file."""
    return os.path.join(self._app.data_dir.tmp_dir_path, f".{self._filename_hash}.access")

  def lock_file_path(self):
    """Get the path to the lock file."""
    return os.path.join(self._app.data_dir.tmp_dir_path, f".{self._filename_hash}.lock")

  def release(self):
    """Release the lock file and decrement the count.
    
    Uses file locking to protect read/write operations. Each call decrements
    the count in the file. If the count reaches 0 or below, it stays at 0.
    """
    lock_file_path = self.lock_file_path()
    file_lock = FileLock(lock_file_path)
    
    try:
      with file_lock:
        current_count, timestamp = self._read_access_file()
        
        # Decrement count (but not below 0)
        count = max(0, current_count - 1)
        # Keep original timestamp
        
        # Write updated timestamp and count
        access_file_path = self.access_file_path()
        with open(access_file_path, 'w') as f:
          f.write(f"{timestamp}:{count}")
          
    except Exception as e:
      Logger.instance(LOG_ID).error(f"Failed to decrement lock file count: {e}")
      raise

  def _read_access_file(self):
    """Internal method to read lock file without locking.
    
    Returns:
      tuple: (count, timestamp) where count is int and timestamp is float
    """
    access_file_path = self.access_file_path()
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

