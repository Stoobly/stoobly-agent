import os

from orator.migrations import Migrator, DatabaseMigrationRepository

from stoobly_agent.config.source_dir import SourceDir
from stoobly_agent.lib.orm import ORM

def build_migrator() -> Migrator:
  db = ORM.instance().db

  # Table to store migrations history
  repository = DatabaseMigrationRepository(db, 'migrations')
  migrator = Migrator(repository, db)

  if not migrator.repository_exists():
      repository.create_repository()

  return migrator

def build_migrations_path():
  return os.path.join(SourceDir.instance().db_migrations_dir_path)

def migrate(pretend = False):
  migrator = build_migrator()
  migrations_path = build_migrations_path()
  migrator.run(migrations_path, pretend)

def rollback(pretend = False):
  migrator = build_migrator()
  migrations_path = build_migrations_path()
  migrator.rollback(migrations_path, pretend)