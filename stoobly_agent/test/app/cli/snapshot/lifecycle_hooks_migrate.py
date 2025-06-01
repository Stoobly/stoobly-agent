from stoobly_agent.app.cli.types.snapshot_migration import SnapshotMigration

def handle_before_migrate(snapshot_migration: SnapshotMigration):
  request = snapshot_migration.request
  response = snapshot_migration.response

  request.headers['X-Test'] = '1'
  response.content = b'Test'

  snapshot_migration.save()