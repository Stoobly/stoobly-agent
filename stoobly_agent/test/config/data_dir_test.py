import os
import shutil

from stoobly_agent.config.data_dir import DataDir
from stoobly_agent.test.test_helper import reset


class TestDataDir():
  original_cwd = os.getcwd()

  def test_in_home(self):
    # A previous test can put us in a test folder
    os.chdir(self.original_cwd)
    reset()

    home_dir = os.path.expanduser("~")
    data_dir_path = os.path.join(home_dir, DataDir.DATA_DIR_NAME, 'tmp', DataDir.DATA_DIR_NAME)

    try:
      result = DataDir.instance().path

      assert result == data_dir_path
    finally:
      reset()

  def test_in_cwd(self):
    temp_dir = DataDir.instance().tmp_dir_path
    nested_temp_dir = os.path.join(temp_dir, DataDir.DATA_DIR_NAME, 'tmp' )
    data_dir_path = os.path.join(nested_temp_dir, DataDir.DATA_DIR_NAME)
    os.makedirs(data_dir_path, exist_ok=True)

    # Go into nested folder
    os.chdir(nested_temp_dir)
    reset()
    DataDir.instance().create_test_path = False

    try:
      result = DataDir.instance().path

      assert result == data_dir_path
      assert result != temp_dir

    finally:
      shutil.rmtree(temp_dir)
      os.chdir(self.original_cwd)
      reset()

  def test_in_parent_nested(self):
    # Create a temporary directory structure for testing
    temp_dir = DataDir.instance().tmp_dir_path

    # Create nested folders
    nested_dir1 = os.path.join(temp_dir, "nested1")
    nested_dir2 = os.path.join(nested_dir1, "nested2")
    nested_dir3 = os.path.join(nested_dir2, "nested3")
    os.makedirs(nested_dir3)

    # Create .stoobly folder in the nested structure
    data_dir_path = os.path.join(nested_dir1, DataDir.DATA_DIR_NAME)
    os.makedirs(data_dir_path)

    # Go into dir3
    os.chdir(nested_dir3)
    reset()
    DataDir.instance().create_test_path = False

    try:
      # Test when .stoobly folder exists in the nested structure
      result = DataDir.instance().path

      assert result == data_dir_path
      assert result != temp_dir

    finally:
      shutil.rmtree(temp_dir)
      os.chdir(self.original_cwd)
      reset()

