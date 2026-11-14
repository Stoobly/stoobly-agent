import os
import shutil

import pytest

from stoobly_agent.config.app_data_dir import AppDataDir, SERVICES_CONFIG_FILE_PATH
from stoobly_agent.config.constants.env_vars import ENV
from stoobly_agent.config.constants.mode import NONE
from stoobly_agent.config.data_dir import DATA_DIR_NAME, DataDir
from stoobly_agent.test.test_helper import reset


def _make_app_data_dir(app_root: str) -> str:
  """Create .stoobly/services/.config.yml under app_root; return the .stoobly path."""
  data_dir_path = os.path.join(app_root, DATA_DIR_NAME)
  services_config_path = os.path.join(data_dir_path, SERVICES_CONFIG_FILE_PATH)
  os.makedirs(os.path.dirname(services_config_path), exist_ok=True)
  with open(services_config_path, 'w') as fp:
    fp.write('')
  return data_dir_path


def _reset_singletons():
  AppDataDir._instance = None
  DataDir._instances = None


class TestAppDataDir:
  @pytest.fixture(autouse=True, scope='class')
  def settings(self):
    return reset()

  @pytest.fixture(scope='class')
  def original_cwd(self) -> str:
    return os.getcwd()

  def test_init_raises(self):
    with pytest.raises(RuntimeError, match='Call instance\\(\\) instead'):
      AppDataDir()

  def test_find_data_dir_in_start_path(self, original_cwd: str):
    os.environ[ENV] = NONE
    _reset_singletons()

    temp_dir = os.path.join(original_cwd, 'tmp-app-data-dir')
    app_root = os.path.join(temp_dir, 'app')
    os.makedirs(app_root, exist_ok=True)
    expected = _make_app_data_dir(app_root)

    try:
      result = AppDataDir.find_data_dir(app_root)
      assert result == expected
    finally:
      shutil.rmtree(temp_dir)
      os.chdir(original_cwd)

  def test_find_data_dir_in_parent(self, original_cwd: str):
    os.environ[ENV] = NONE
    _reset_singletons()

    temp_dir = os.path.join(original_cwd, 'tmp-app-data-dir')
    app_root = os.path.join(temp_dir, 'app')
    nested = os.path.join(app_root, 'nested1', 'nested2')
    os.makedirs(nested, exist_ok=True)
    expected = _make_app_data_dir(app_root)

    try:
      result = AppDataDir.find_data_dir(nested)
      assert result == expected
    finally:
      shutil.rmtree(temp_dir)
      os.chdir(original_cwd)

  def test_find_data_dir_requires_services_config(self, original_cwd: str):
    os.environ[ENV] = NONE
    _reset_singletons()

    temp_dir = os.path.join(original_cwd, 'tmp-app-data-dir')
    app_root = os.path.join(temp_dir, 'app')
    data_dir_path = os.path.join(app_root, DATA_DIR_NAME)
    os.makedirs(data_dir_path, exist_ok=True)

    try:
      result = AppDataDir.find_data_dir(app_root)
      assert result is None
    finally:
      shutil.rmtree(temp_dir)
      os.chdir(original_cwd)

  def test_find_data_dir_not_found(self, original_cwd: str):
    os.environ[ENV] = NONE
    _reset_singletons()

    # Isolate under /tmp so ancestors cannot contain services/.config.yml
    isolated = os.path.join('/tmp', 'stoobly-app-data-dir-isolated')
    os.makedirs(isolated, exist_ok=True)

    try:
      result = AppDataDir.find_data_dir(isolated)
      assert result is None
    finally:
      shutil.rmtree(isolated)
      os.chdir(original_cwd)

  def test_instance_uses_app_dir_when_found(self, original_cwd: str):
    os.environ[ENV] = NONE
    _reset_singletons()

    temp_dir = os.path.join(original_cwd, 'tmp-app-data-dir')
    app_root = os.path.join(temp_dir, 'app')
    nested = os.path.join(app_root, 'nested')
    os.makedirs(nested, exist_ok=True)
    expected_data_dir = _make_app_data_dir(app_root)

    os.chdir(nested)

    try:
      result = AppDataDir.instance()
      assert isinstance(result, DataDir)
      assert result.path == expected_data_dir
      assert result.context_dir_path == os.path.abspath(app_root)
    finally:
      _reset_singletons()
      shutil.rmtree(temp_dir)
      os.chdir(original_cwd)

  def test_instance_with_explicit_path(self, original_cwd: str):
    os.environ[ENV] = NONE
    _reset_singletons()

    temp_dir = os.path.join(original_cwd, 'tmp-app-data-dir')
    app_root = os.path.join(temp_dir, 'app')
    os.makedirs(app_root, exist_ok=True)
    expected_data_dir = _make_app_data_dir(app_root)

    os.chdir(original_cwd)

    try:
      result = AppDataDir.instance(app_root)
      assert result.path == expected_data_dir
      assert result.context_dir_path == os.path.abspath(app_root)
    finally:
      _reset_singletons()
      shutil.rmtree(temp_dir)
      os.chdir(original_cwd)

  def test_instance_falls_back_to_data_dir(self, original_cwd: str):
    os.environ[ENV] = NONE
    _reset_singletons()

    # No services/.config.yml under this tree; AppDataDir should match DataDir.instance()
    isolated = os.path.join('/tmp', 'stoobly-app-data-dir-fallback')
    os.makedirs(isolated, exist_ok=True)
    os.chdir(isolated)

    try:
      expected = DataDir.instance()
      _reset_singletons()
      os.chdir(isolated)

      result = AppDataDir.instance()
      assert isinstance(result, DataDir)
      assert result.path == DataDir.instance().path
      assert result is DataDir.instance()
      assert result.path == expected.path
    finally:
      _reset_singletons()
      shutil.rmtree(isolated)
      os.chdir(original_cwd)
