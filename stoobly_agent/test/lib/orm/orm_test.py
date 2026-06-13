import os
import shutil
import tempfile

import pytest

from stoobly_agent.config.data_dir import DataDir
from stoobly_agent.lib.orm import ORM


@pytest.fixture
def temp_context_dirs():
  dir_a = tempfile.mkdtemp()
  dir_b = tempfile.mkdtemp()
  yield dir_a, dir_b
  shutil.rmtree(dir_a, ignore_errors=True)
  shutil.rmtree(dir_b, ignore_errors=True)


def test_configure_uses_custom_data_dir_path(temp_context_dirs):
  dir_a, dir_b = temp_context_dirs

  DataDir.instance(dir_a).create(dir_a)
  DataDir.instance(dir_b).create(dir_b)

  ORM.configure(dir_a)
  assert ORM.instance()._data_dir_path == dir_a
  assert ORM.instance().db._config['production']['database'] == DataDir.instance(dir_a).db_file_path

  ORM.configure(dir_b)
  assert ORM.instance()._data_dir_path == dir_b
  assert ORM.instance().db._config['production']['database'] == DataDir.instance(dir_b).db_file_path


def test_configure_is_idempotent_for_same_path(temp_context_dirs):
  dir_a, _ = temp_context_dirs

  DataDir.instance(dir_a).create(dir_a)

  ORM.configure(dir_a)
  db = ORM.instance().db

  ORM.configure(dir_a)

  assert ORM.instance().db is db
