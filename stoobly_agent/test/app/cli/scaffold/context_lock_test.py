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
    context_path = app.host_context_dir_path
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

    def test_access_resets_count_when_10_seconds_passed(self, context_lock):
      """Test that access resets count when 10+ seconds has passed"""
      access_file_path = context_lock.access_file_path()
      
      # Create access file with old timestamp (more than 10 seconds ago)
      old_timestamp = time.time() - FOLDER_COUNT_INTERVAL_SECONDS - 1
      old_count = 5
      with open(access_file_path, 'w') as f:
        f.write(f"{old_timestamp}:{old_count}")
      
      context_lock.access()
      
      with open(access_file_path, 'r') as f:
        content = f.read().strip()
        parts = content.split(':', 1)
        assert len(parts) == 2
        timestamp = float(parts[0])
        count = int(parts[1])
        
        # When 10+ seconds passed, current_count is reset to 0, then incremented to 1
        assert count == 1
        # Timestamp should be updated to current time
        assert timestamp > old_timestamp

    def test_access_increments_count_when_less_than_10_seconds_passed(self, context_lock):
      """Test that access increments count when less than 10 seconds has passed"""
      access_file_path = context_lock.access_file_path()
      
      # Create access file with recent timestamp (less than 10 seconds ago)
      recent_timestamp = time.time() - 5
      initial_count = 3
      with open(access_file_path, 'w') as f:
        f.write(f"{recent_timestamp}:{initial_count}")
      
      context_lock.access()
      
      with open(access_file_path, 'r') as f:
        content = f.read().strip()
        parts = content.split(':', 1)
        assert len(parts) == 2
        timestamp = float(parts[0])
        count = int(parts[1])
        
        # Should increment from 3 to 4
        assert count == initial_count + 1
        # Timestamp should be updated to current time
        assert timestamp > recent_timestamp

  class TestRelease():
    def test_release_decrements_count(self, context_lock):
      """Test that release decrements the count and preserves timestamp"""
      # Create access file with count 3
      access_file_path = context_lock.access_file_path()
      original_timestamp = time.time() - 5  # 5 seconds ago
      with open(access_file_path, 'w') as f:
        f.write(f"{original_timestamp}:3")
      
      context_lock.release()
      
      with open(access_file_path, 'r') as f:
        content = f.read().strip()
        parts = content.split(':', 1)
        assert len(parts) == 2
        timestamp = float(parts[0])
        count = int(parts[1])
        
        assert count == 2
        # Timestamp should be preserved
        assert timestamp == original_timestamp

    def test_release_does_not_go_below_zero(self, context_lock):
      """Test that release doesn't decrement below 0 and preserves timestamp"""
      # Create access file with count 0
      access_file_path = context_lock.access_file_path()
      original_timestamp = time.time() - 5  # 5 seconds ago
      with open(access_file_path, 'w') as f:
        f.write(f"{original_timestamp}:0")
      
      context_lock.release()
      
      with open(access_file_path, 'r') as f:
        content = f.read().strip()
        parts = content.split(':', 1)
        assert len(parts) == 2
        timestamp = float(parts[0])
        count = int(parts[1])
        
        assert count == 0
        # Timestamp should be preserved
        assert timestamp == original_timestamp

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
    def test_access_and_release_work_together(self, context_lock):
      """Test that access and release work together correctly"""
      # Initial access - should create file with count 1
      context_lock.access()
      count1 = context_lock.access_count()
      assert count1 == 1
      
      # Another access - should increment to 2 (since less than 10 seconds passed)
      time.sleep(0.1)  # Small delay to ensure different timestamps
      context_lock.access()
      count2 = context_lock.access_count()
      assert count2 == 2
      
      # Release - should decrement from 2 to 1
      context_lock.release()
      count3 = context_lock.access_count()
      assert count3 == 1
      
      # Release again - should decrement from 1 to 0
      context_lock.release()
      count4 = context_lock.access_count()
      assert count4 == 0
      
      # Release when at 0 - should stay at 0
      context_lock.release()
      count5 = context_lock.access_count()
      assert count5 == 0

  class TestLocking():
    def test_concurrent_access_calls(self, context_lock):
      """Test that concurrent access() calls are properly locked"""
      num_threads = 5
      num_calls_per_thread = 10
      
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

    def test_concurrent_access_and_release(self, context_lock):
      """Test that concurrent access() and release() calls are properly locked"""
      num_threads = 4
      
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
        # With num_threads accesses and num_threads releases, count should be back to initial_count
        # (initial_count + num_threads - num_threads = initial_count)
        assert count == initial_count

