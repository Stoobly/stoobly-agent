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

  def test_in_home(self, original_cwd: str):
    os.chdir(original_cwd)
    data_dir_path = os.path.join(original_cwd, DATA_DIR_NAME)
    os.environ[ENV] = NONE

    result = DataDir.instance().path

    assert result == data_dir_path

  def test_in_cwd(self, original_cwd: str):
    os.environ[ENV] = NONE
    DataDir._instances = None

    temp_dir = os.path.join(original_cwd, 'tmp')
    nested_temp_dir = os.path.join(temp_dir, 'tmp-nested')
    data_dir_path = os.path.join(nested_temp_dir, DATA_DIR_NAME)
    os.makedirs(data_dir_path, exist_ok=True)

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
    os.makedirs(nested_dir3, exist_ok=True)

    # Create .stoobly folder in the nested structure
    data_dir_path = os.path.join(nested_dir1, DATA_DIR_NAME)
    os.makedirs(data_dir_path, exist_ok=True)

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

  def test_relative_path_arg_returns_absolute_path(self, original_cwd: str):
    """Regression: DataDir.instance() with a relative path must return an absolute .path"""
    os.environ[ENV] = NONE
    DataDir._instances = None

    # Create parent/child dirs; we'll cd into child and pass '../' as path
    temp_dir = os.path.join(original_cwd, 'tmp')
    child_dir = os.path.join(temp_dir, 'child')
    os.makedirs(child_dir, exist_ok=True)

    expected_data_dir_path = os.path.join(temp_dir, DATA_DIR_NAME)

    os.chdir(child_dir)

    try:
      result = DataDir.instance('..').path

      assert os.path.isabs(result), f"Expected absolute path, got: {result}"
      assert result == expected_data_dir_path

    finally:
      DataDir._instances = None
      shutil.rmtree(temp_dir)
      os.chdir(original_cwd)

  def test_path_with_stoobly_resolves_to_grandparent(self, original_cwd: str):
    os.environ[ENV] = NONE
    DataDir._instances = None

    temp_dir = os.path.join(original_cwd, 'tmp')
    data_dir_path = os.path.join(temp_dir, DATA_DIR_NAME)
    nested_path = os.path.join(data_dir_path, 'db')
    os.makedirs(nested_path, exist_ok=True)

    try:
      result = DataDir.instance(nested_path).path

      assert result == data_dir_path

    finally:
      DataDir._instances = None
      shutil.rmtree(temp_dir)

  def test_path_with_stoobly_in_tmp_keeps_nested_stoobly(self, original_cwd: str):
    os.environ[ENV] = NONE
    DataDir._instances = None

    temp_dir = os.path.join(original_cwd, 'tmp')
    parent_data_dir_path = os.path.join(temp_dir, DATA_DIR_NAME)
    nested_data_dir_path = os.path.join(parent_data_dir_path, 'tmp', DATA_DIR_NAME)
    os.makedirs(nested_data_dir_path, exist_ok=True)

    try:
      result = DataDir.instance(nested_data_dir_path).path

      assert result == nested_data_dir_path
      assert result != parent_data_dir_path

    finally:
      DataDir._instances = None
      shutil.rmtree(temp_dir)