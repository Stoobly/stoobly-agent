import os
import pdb

from typing import TYPE_CHECKING
from filelock import FileLock

if TYPE_CHECKING:
  from stoobly_orator.migrations import Migrator

from stoobly_agent.config.data_dir import DataDir
from stoobly_agent.config.source_dir import SourceDir
from stoobly_agent.lib.orm import ORM

def migrate(version, pretend = False):
  # If current db version is same as version, return
  if os.path.exists(DataDir.instance().db_version_path):
    with open(DataDir.instance().db_version_path, 'r') as fp:
      _version = fp.read().strip()

      if _version == version:
        return

  # Use FileLock for migration locking
  data_dir: DataDir = DataDir.instance()
  lock_path = os.path.join(data_dir.tmp_dir_path, '.db-migrate.lock')
  file_lock = FileLock(lock_path, timeout=5)

  with file_lock:
    migrator = __build_migrator()
    migrations_path = __build_migrations_path()
    migrator.run(migrations_path, pretend)

    with open(DataDir.instance().db_version_path, 'w') as fp:
      fp.write(version)

def rollback(pretend = False):
  migrator = __build_migrator()
  migrations_path = __build_migrations_path()
  migrator.rollback(migrations_path, pretend)

  os.remove(DataDir.instance().db_version_path)

def __build_migrator() -> 'Migrator':
  from stoobly_orator.migrations import Migrator, DatabaseMigrationRepository

  db = ORM.instance().db

  # Table to store migrations history
  repository = DatabaseMigrationRepository(db, 'migrations')
  migrator = Migrator(repository, db)

  if not migrator.repository_exists():
      repository.create_repository()

  return migrator

def __build_migrations_path():
  return os.path.join(SourceDir.instance().db_migrations_dir_path)