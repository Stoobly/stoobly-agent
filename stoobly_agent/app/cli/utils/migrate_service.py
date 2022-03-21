import os

from orator.migrations import Migrator, DatabaseMigrationRepository

from stoobly_agent.config.source_dir import SourceDir
from stoobly_agent.lib.orm import ORM

def migrate(pretend = False):
  db = ORM.instance().db

  # Table to store migrations history
  repository = DatabaseMigrationRepository(db, 'migrations')
  migrator = Migrator(repository, db)

  if not migrator.repository_exists():
      repository.create_repository()

  migrations_path = os.path.join(SourceDir.instance().db_migrations_dir_path)
  migrator.run(migrations_path, pretend)  