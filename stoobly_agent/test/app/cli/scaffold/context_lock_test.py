import os
import pytest
import time
import hashlib
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

from stoobly_agent.app.cli.scaffold.app import App
from stoobly_agent.app.cli.scaffold.context_lock import ContextLock, FOLDER_COUNT_INTERVAL_SECONDS
from stoobly_agent.config.data_dir import DataDir
from stoobly_agent.test.test_helper import reset

class TestContextLock():

  @pytest.fixture(scope='class', autouse=True)
  def settings(self):
    return reset()

  @pytest.fixture(scope='class')
  def app_dir_path(self):
    data_dir: DataDir = DataDir.instance()
    path = os.path.abspath(os.path.join(data_dir.tmp_dir_path, '..', '..'))
    yield path

  @pytest.fixture
  def app(self, app_dir_path):
    return App(app_dir_path)

  @pytest.fixture
  def context_lock(self, app):
    return ContextLock(app)

  @pytest.fixture
  def filename_hash(self, app):
    """Get the hash used for filenames"""
    context_path = app.context_data_dir.path
    return hashlib.md5(context_path.encode()).hexdigest()

  class TestAccessCount():
    def test_access_count_returns_zero_when_no_file_exists(self, context_lock):
      """Test that access_count returns 0 when access file doesn't exist"""
      count = context_lock.access_count()
      assert count == 0

    def test_access_count_returns_count_from_file(self, context_lock, filename_hash, app):
      """Test that access_count returns the count from the access file"""
      # Create access file with count
      access_file_path = context_lock.access_file_path()
      current_time = time.time()
      with open(access_file_path, 'w') as f:
        f.write(f"{current_time}:5")
      
      count = context_lock.access_count()
      assert count == 5

    def test_access_count_handles_invalid_format(self, context_lock):
      """Test that access_count handles invalid file format gracefully"""
      # Create access file with invalid format
      access_file_path = context_lock.access_file_path()
      with open(access_file_path, 'w') as f:
        f.write("invalid")
      
      count = context_lock.access_count()
      assert count == 0

  class TestAccess():
    def test_access_creates_file_with_count_one(self, context_lock):
      """Test that access creates access file with count 1 when no file exists"""
      context_lock.access()
      
      access_file_path = context_lock.access_file_path()
      assert os.path.exists(access_file_path)
      
      with open(access_file_path, 'r') as f:
        content = f.read().strip()
        parts = content.split(':', 1)
        assert len(parts) == 2
        timestamp = float(parts[0])
        count = int(parts[1])
        
        assert count == 1
        assert timestamp > 0

    def test_access_increments_count_based_on_folders(self, context_lock, app):
      """Test that access counts folders when 10+ seconds has passed"""
      tmp_dir_path = app.data_dir.tmp_dir_path
      
      # Create folders with pid and timestamp files (any workflow files)
      folder1 = os.path.join(tmp_dir_path, 'folder1')
      folder2 = os.path.join(tmp_dir_path, 'folder2')
      os.makedirs(folder1, exist_ok=True)
      os.makedirs(folder2, exist_ok=True)
      
      # Create pid file in folder1 (any .pid file)
      pid_file1 = os.path.join(folder1, "test-workflow.pid")
      with open(pid_file1, 'w') as f:
        f.write("12345")
      
      # Create timestamp file in folder2 (any .timestamp file)
      timestamp_file2 = os.path.join(folder2, "test-workflow.timestamp")
      with open(timestamp_file2, 'w') as f:
        f.write(str(time.time()))
      
      try:
        # Create access file with old timestamp (more than 10 seconds ago)
        access_file_path = context_lock.access_file_path()
        old_timestamp = time.time() - FOLDER_COUNT_INTERVAL_SECONDS - 1
        with open(access_file_path, 'w') as f:
          f.write(f"{old_timestamp}:1")
        
        context_lock.access()
        
        with open(access_file_path, 'r') as f:
          content = f.read().strip()
          parts = content.split(':', 1)
          count = int(parts[1])
          
          # Should be 2 folders + 1 = 3
          assert count == 3
      finally:
        # Cleanup
        if os.path.exists(pid_file1):
          os.remove(pid_file1)
        if os.path.exists(timestamp_file2):
          os.remove(timestamp_file2)
        if os.path.exists(folder1):
          os.rmdir(folder1)
        if os.path.exists(folder2):
          os.rmdir(folder2)

  class TestRelease():
    def test_release_decrements_count(self, context_lock):
      """Test that release decrements the count"""
      # Create access file with count 3
      access_file_path = context_lock.access_file_path()
      current_time = time.time()
      with open(access_file_path, 'w') as f:
        f.write(f"{current_time}:3")
      
      context_lock.release()
      
      with open(access_file_path, 'r') as f:
        content = f.read().strip()
        parts = content.split(':', 1)
        count = int(parts[1])
        
        assert count == 2

    def test_release_does_not_go_below_zero(self, context_lock):
      """Test that release doesn't decrement below 0"""
      # Create access file with count 0
      access_file_path = context_lock.access_file_path()
      current_time = time.time()
      with open(access_file_path, 'w') as f:
        f.write(f"{current_time}:0")
      
      context_lock.release()
      
      with open(access_file_path, 'r') as f:
        content = f.read().strip()
        parts = content.split(':', 1)
        count = int(parts[1])
        
        assert count == 0

  class TestFilePaths():
    def test_access_file_path(self, context_lock, filename_hash, app):
      """Test that access_file_path returns correct path with hash"""
      expected_path = os.path.join(app.data_dir.tmp_dir_path, f".{filename_hash}.access")
      assert context_lock.access_file_path() == expected_path

    def test_lock_file_path(self, context_lock, filename_hash, app):
      """Test that lock_file_path returns correct path with hash"""
      expected_path = os.path.join(app.data_dir.tmp_dir_path, f".{filename_hash}.lock")
      assert context_lock.lock_file_path() == expected_path

  class TestAccessAndRelease():
    def test_access_and_release_work_together(self, context_lock, app):
      """Test that access and release work together correctly"""
      tmp_dir_path = app.data_dir.tmp_dir_path
      
      # Create a folder with a pid file
      folder1 = os.path.join(tmp_dir_path, 'folder1')
      os.makedirs(folder1, exist_ok=True)
      pid_file1 = os.path.join(folder1, "test-workflow.pid")
      with open(pid_file1, 'w') as f:
        f.write("12345")
      
      try:
        # Initial access - should count 1 folder + 1 = 2
        context_lock.access()
        count1 = context_lock.access_count()
        assert count1 >= 1
        
        # Create another folder with timestamp file
        folder2 = os.path.join(tmp_dir_path, 'folder2')
        os.makedirs(folder2, exist_ok=True)
        timestamp_file2 = os.path.join(folder2, "test-workflow.timestamp")
        with open(timestamp_file2, 'w') as f:
          f.write(str(time.time()))
        
        # Another access - should count 2 folders + 1 = 3
        context_lock.access()
        count2 = context_lock.access_count()
        assert count2 >= count1
        
        # Release - should decrement from count in file
        context_lock.release()
        count3 = context_lock.access_count()
        assert count3 < count2
      finally:
        # Cleanup
        if os.path.exists(pid_file1):
          os.remove(pid_file1)
        if os.path.exists(timestamp_file2):
          os.remove(timestamp_file2)
        if os.path.exists(folder1):
          os.rmdir(folder1)
        if os.path.exists(folder2):
          os.rmdir(folder2)

  class TestLocking():
    def test_concurrent_access_calls(self, context_lock, app):
      """Test that concurrent access() calls are properly locked"""
      tmp_dir_path = app.data_dir.tmp_dir_path
      num_threads = 5
      num_calls_per_thread = 10
      
      # Create folders with pid files
      folders = []
      for i in range(num_threads):
        folder = os.path.join(tmp_dir_path, f'folder{i}')
        os.makedirs(folder, exist_ok=True)
        folders.append(folder)
        pid_file = os.path.join(folder, f"test-workflow{i}.pid")
        with open(pid_file, 'w') as f:
          f.write(f"pid{i}")
      
      try:
        def access_worker():
          """Worker that calls access() multiple times"""
          errors = []
          for _ in range(num_calls_per_thread):
            try:
              context_lock.access()
            except Exception as e:
              errors.append(e)
          return errors
        
        # Run concurrent access() calls
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
          futures = [executor.submit(access_worker) for _ in range(num_threads)]
          results = [future.result() for future in as_completed(futures)]
        
        # Check that no errors occurred
        all_errors = [error for errors in results for error in errors]
        assert len(all_errors) == 0, f"Errors occurred during concurrent access: {all_errors}"
        
        # Verify the access file exists and has valid format
        access_file_path = context_lock.access_file_path()
        assert os.path.exists(access_file_path)
        
        with open(access_file_path, 'r') as f:
          content = f.read().strip()
          parts = content.split(':', 1)
          assert len(parts) == 2
          count = int(parts[1])
          # Since calls happen quickly (less than 10 seconds), they just increment
          # Starting from 0, with num_threads * num_calls_per_thread calls = 50
          expected_count = num_threads * num_calls_per_thread
          assert count == expected_count, f"Expected count {expected_count}, got {count}"
      finally:
        # Cleanup
        for folder in folders:
          for file in os.listdir(folder):
            if file.endswith('.pid'):
              pid_file = os.path.join(folder, file)
              if os.path.exists(pid_file):
                os.remove(pid_file)
          if os.path.exists(folder):
            os.rmdir(folder)

    def test_concurrent_release_calls(self, context_lock):
      """Test that concurrent release() calls are properly locked"""
      num_threads = 5
      num_releases = 3
      
      # Set up initial count
      access_file_path = context_lock.access_file_path()
      current_time = time.time()
      initial_count = num_threads * num_releases + 10
      with open(access_file_path, 'w') as f:
        f.write(f"{current_time}:{initial_count}")
      
      def release_worker():
        """Worker that calls release() multiple times"""
        errors = []
        for _ in range(num_releases):
          try:
            context_lock.release()
          except Exception as e:
            errors.append(e)
        return errors
      
      # Run concurrent release() calls
      with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(release_worker) for _ in range(num_threads)]
        results = [future.result() for future in as_completed(futures)]
      
      # Check that no errors occurred
      all_errors = [error for errors in results for error in errors]
      assert len(all_errors) == 0, f"Errors occurred during concurrent release: {all_errors}"
      
      # Verify the count was decremented correctly
      final_count = context_lock.access_count()
      # Should be initial_count - (num_threads * num_releases)
      expected_count = initial_count - (num_threads * num_releases)
      assert final_count == expected_count, f"Expected count {expected_count}, got {final_count}"

    def test_concurrent_access_count_calls(self, context_lock):
      """Test that concurrent access_count() calls work correctly"""
      num_threads = 10
      num_calls_per_thread = 20
      
      # Set up initial count
      access_file_path = context_lock.access_file_path()
      current_time = time.time()
      initial_count = 5
      with open(access_file_path, 'w') as f:
        f.write(f"{current_time}:{initial_count}")
      
      def access_count_worker():
        """Worker that calls access_count() multiple times"""
        errors = []
        counts = []
        for _ in range(num_calls_per_thread):
          try:
            count = context_lock.access_count()
            counts.append(count)
          except Exception as e:
            errors.append(e)
        return errors, counts
      
      # Run concurrent access_count() calls
      with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(access_count_worker) for _ in range(num_threads)]
        results = [future.result() for future in as_completed(futures)]
      
      # Check that no errors occurred
      all_errors = [error for errors, _ in results for error in errors]
      assert len(all_errors) == 0, f"Errors occurred during concurrent access_count: {all_errors}"
      
      # Verify all counts are correct
      all_counts = [count for _, counts in results for count in counts]
      assert all(count == initial_count for count in all_counts), \
        f"Not all counts match initial count {initial_count}: {set(all_counts)}"

    def test_concurrent_access_and_release(self, context_lock, app):
      """Test that concurrent access() and release() calls are properly locked"""
      tmp_dir_path = app.data_dir.tmp_dir_path
      num_threads = 4
      
      # Create folders with pid files
      folders = []
      for i in range(2):
        folder = os.path.join(tmp_dir_path, f'folder{i}')
        os.makedirs(folder, exist_ok=True)
        folders.append(folder)
        pid_file = os.path.join(folder, f"test-workflow{i}.pid")
        with open(pid_file, 'w') as f:
          f.write(f"pid{i}")
      
      try:
        def access_worker():
          """Worker that calls access()"""
          errors = []
          try:
            context_lock.access()
          except Exception as e:
            errors.append(e)
          return errors
        
        def release_worker():
          """Worker that calls release()"""
          errors = []
          try:
            context_lock.release()
          except Exception as e:
            errors.append(e)
          return errors
        
        # Set up initial count
        access_file_path = context_lock.access_file_path()
        current_time = time.time()
        initial_count = num_threads
        with open(access_file_path, 'w') as f:
          f.write(f"{current_time}:{initial_count}")
        
        # Run concurrent access() and release() calls
        with ThreadPoolExecutor(max_workers=num_threads * 2) as executor:
          access_futures = [executor.submit(access_worker) for _ in range(num_threads)]
          release_futures = [executor.submit(release_worker) for _ in range(num_threads)]
          
          access_results = [future.result() for future in as_completed(access_futures)]
          release_results = [future.result() for future in as_completed(release_futures)]
        
        # Check that no errors occurred
        all_access_errors = [error for errors in access_results for error in errors]
        all_release_errors = [error for errors in release_results for error in errors]
        assert len(all_access_errors) == 0, f"Errors occurred during concurrent access: {all_access_errors}"
        assert len(all_release_errors) == 0, f"Errors occurred during concurrent release: {all_release_errors}"
        
        # Verify the access file exists and has valid format
        assert os.path.exists(access_file_path)
        
        with open(access_file_path, 'r') as f:
          content = f.read().strip()
          parts = content.split(':', 1)
          assert len(parts) == 2
          count = int(parts[1])
          # Count should be non-negative
          assert count >= 0
      finally:
        # Cleanup
        for folder in folders:
          for file in os.listdir(folder):
            if file.endswith('.pid'):
              pid_file = os.path.join(folder, file)
              if os.path.exists(pid_file):
                os.remove(pid_file)
          if os.path.exists(folder):
            os.rmdir(folder)

