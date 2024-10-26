import os
import shutil

import pytest

from stoobly_agent.config.constants.env_vars import ENV
from stoobly_agent.config.constants.mode import NONE
from stoobly_agent.config.data_dir import DataDir, DATA_DIR_NAME
from stoobly_agent.test.test_helper import reset


class TestDataDir():
  @pytest.fixture(autouse=True, scope='class')
  def settings(self):
    return reset()

  @pytest.fixture(scope='class')
  def original_cwd(self) -> str:
    return os.getcwd()

  @pytest.fixture(scope='class')
  def home_dir(self) -> str:
    return os.path.expanduser("~")

  def test_in_home(self, original_cwd: str, home_dir: str):
    # A previous test can put us in 'stoobly_agent/test/app/models/schemas/.stoobly'
    os.chdir(original_cwd)
    data_dir_path = os.path.join(home_dir, DATA_DIR_NAME)
    os.environ[ENV] = NONE

    result = DataDir.instance().path

    assert result == data_dir_path

  def test_in_cwd(self, original_cwd: str):
    os.environ[ENV] = NONE
    DataDir._instances = None

    temp_dir = os.path.join(original_cwd, 'tmp')
    nested_temp_dir = os.path.join(temp_dir, 'tmp-nested')
    data_dir_path = os.path.join(nested_temp_dir, DATA_DIR_NAME)
    os.makedirs(data_dir_path)

    # Go into nested folder
    os.chdir(nested_temp_dir)

    try:
      result = DataDir.instance().path

      assert result == data_dir_path
      assert result != temp_dir

    finally:
      shutil.rmtree(temp_dir)
      os.chdir(original_cwd)

  def test_in_parent_nested(self, original_cwd: str):
    os.environ[ENV] = NONE
    DataDir._instances = None

    # Create a temporary directory structure for testing
    temp_dir = os.path.join(original_cwd, 'tmp')

    # Create nested folders
    nested_dir1 = os.path.join(temp_dir, "nested1")
    nested_dir2 = os.path.join(nested_dir1, "nested2")
    nested_dir3 = os.path.join(nested_dir2, "nested3")
    os.makedirs(nested_dir3)

    # Create .stoobly folder in the nested structure
    data_dir_path = os.path.join(nested_dir1, DATA_DIR_NAME)
    os.makedirs(data_dir_path)

    # Go into dir3
    os.chdir(nested_dir3)

    try:
      # Test when .stoobly folder exists in the nested structure
      result = DataDir.instance().path

      assert result == data_dir_path
      assert result != temp_dir

    finally:
      shutil.rmtree(temp_dir)
      os.chdir(original_cwd)

