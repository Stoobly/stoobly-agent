import click
import sys

from stoobly_agent.app.models.factories.resource.local_db.helpers.snapshot_format import (
  FORMAT_V1,
  FORMAT_V2,
  detect_snapshot_format,
  resolve_write_format,
)
from stoobly_agent.app.models.factories.resource.local_db.helpers.snapshot_migrate import (
  migrate_snapshots_to_v2,
)
from stoobly_agent.config.data_dir import DataDir


def prepare_snapshot_write_format(data_dir: DataDir = None, yes: bool = False) -> int:
  """
  Resolve write format for snapshot create.

  When v1 snapshots are detected, prompt to migrate to v2 (unless non-interactive).
  Returns FORMAT_V1 or FORMAT_V2.
  """
  data_dir = data_dir or DataDir.instance()
  detected = detect_snapshot_format(data_dir)

  if detected != FORMAT_V1:
    return resolve_write_format(data_dir)

  # Non-interactive: keep v1 (no silent migrate)
  if yes or not sys.stdin.isatty():
    return FORMAT_V1

  should_migrate = click.confirm(
    "Existing v1 snapshots detected. Migrate snapshots to v2 format?",
    default=False,
  )
  if not should_migrate:
    return FORMAT_V1

  result = migrate_snapshots_to_v2(data_dir)
  click.echo(
    f"Migrated {result['requests']} request(s) and {result['scenarios']} scenario(s) to v2."
  )
  return FORMAT_V2
