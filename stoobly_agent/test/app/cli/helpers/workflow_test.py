import hashlib
import os
import shutil
import tempfile
from unittest.mock import patch

import pytest

from stoobly_agent.app.cli.helpers.workflow import workflow_running
from stoobly_agent.app.cli.scaffold.constants import APP_DIR_ENV, CONTEXT_DIR_MOUNT_ENV, WORKFLOW_NAME_ENV
from stoobly_agent.config.data_dir import DATA_DIR_NAME, TMP_DIR_NAME


@pytest.fixture
def temp_app_dir():
  """Create a temp dir mimicking the stoobly home inside Docker (/home/stoobly)."""
  tmpdir = tempfile.mkdtemp()
  os.makedirs(os.path.join(tmpdir, DATA_DIR_NAME, TMP_DIR_NAME), exist_ok=True)
  yield tmpdir
  shutil.rmtree(tmpdir, ignore_errors=True)


@pytest.fixture
def lock_file(temp_app_dir):
  """Create the lock file that ContextLock expects for temp_app_dir."""
  context_path = os.path.abspath(temp_app_dir)
  filename_hash = hashlib.md5(context_path.encode()).hexdigest()
  lock_path = os.path.join(temp_app_dir, DATA_DIR_NAME, TMP_DIR_NAME, f'.{filename_hash}.lock')
  open(lock_path, 'w').close()
  return lock_path


class TestWorkflowRunning:

  def test_returns_false_when_workflow_name_not_set(self):
    """Returns False when WORKFLOW_NAME env var is absent."""
    env = {k: v for k, v in os.environ.items() if k != WORKFLOW_NAME_ENV}
    with patch.dict(os.environ, env, clear=True):
      assert workflow_running() is False

  class TestOnHost:
    """APP_DIR points to a real, accessible path (host machine scenario)."""

    def test_returns_true_when_lock_file_exists(self, temp_app_dir, lock_file):
      with patch.dict(os.environ, {WORKFLOW_NAME_ENV: 'mock', APP_DIR_ENV: temp_app_dir}):
        assert workflow_running() is True

    def test_returns_false_when_lock_file_missing(self, temp_app_dir):
      with patch.dict(os.environ, {WORKFLOW_NAME_ENV: 'mock', APP_DIR_ENV: temp_app_dir}):
        assert workflow_running() is False

  class TestInDockerContainer:
    """
    APP_DIR contains the host path (inaccessible inside the container).
    CONTEXT_DIR_MOUNT provides the container-local equivalent (e.g. /home/stoobly).
    """

    def test_returns_true_when_lock_file_exists(self, temp_app_dir, lock_file):
      """CONTEXT_DIR_MOUNT points to the real app dir → lock found → True."""
      env = {
        WORKFLOW_NAME_ENV: 'mock',
        APP_DIR_ENV: '/host/path/not/in/container',
        CONTEXT_DIR_MOUNT_ENV: temp_app_dir,
      }
      with patch.dict(os.environ, env):
        assert workflow_running() is True

    def test_returns_false_when_lock_file_missing(self, temp_app_dir):
      """Lock file absent → False."""
      env = {
        WORKFLOW_NAME_ENV: 'mock',
        APP_DIR_ENV: '/host/path/not/in/container',
        CONTEXT_DIR_MOUNT_ENV: temp_app_dir,
      }
      with patch.dict(os.environ, env):
        assert workflow_running() is False

    def test_returns_false_when_context_dir_mount_not_set(self, tmp_path, monkeypatch):
      """Neither APP_DIR nor CONTEXT_DIR_MOUNT accessible → False."""
      monkeypatch.setenv(WORKFLOW_NAME_ENV, 'mock')
      monkeypatch.setenv(APP_DIR_ENV, '/host/path/not/in/container')
      monkeypatch.delenv(CONTEXT_DIR_MOUNT_ENV, raising=False)
      monkeypatch.chdir(tmp_path)  # CWD with no .stoobly
      assert workflow_running() is False
