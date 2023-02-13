import os
import pdb

from orator.migrations import Migrator, DatabaseMigrationRepository

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

def __build_migrator() -> Migrator:
  db = ORM.instance().db

  # Table to store migrations history
  repository = DatabaseMigrationRepository(db, 'migrations')
  migrator = Migrator(repository, db)

  if not migrator.repository_exists():
      repository.create_repository()

  return migrator

def __build_migrations_path():
  return os.path.join(SourceDir.instance().db_migrations_dir_path)