from stoobly_agent.app.cli.types.snapshot_migration import SnapshotMigration

def handle_before_migrate(snapshot_migration: SnapshotMigration):
  request = snapshot_migration.request
  response = snapshot_migration.response

  # Modify the request/response objects
  request.headers['X-Test'] = '1'
  response.content = b'Test'

  # Use setters to mark as dirty so the service will automatically commit
  snapshot_migration.request = request
  snapshot_migration.response = response