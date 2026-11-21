import os
import re
from typing import Optional

from stoobly_agent.config.data_dir import DataDir

from .request_slug import REQUEST_FILE_EXTENSION

FORMAT_NONE = None
FORMAT_V1 = 1
FORMAT_V2 = 2

UUID_RE = re.compile(
  r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$',
  re.IGNORECASE,
)

def detect_snapshot_format(data_dir: DataDir = None) -> Optional[int]:
  """
  Detect on-disk snapshot format.

  Returns FORMAT_V2, FORMAT_V1, or FORMAT_NONE.
  Prefers v2 when any v2-shaped files exist.
  """
  data_dir = data_dir or DataDir.instance()

  if _has_v2_snapshots(data_dir):
    return FORMAT_V2

  if _has_v1_snapshots(data_dir):
    return FORMAT_V1

  return FORMAT_NONE

def resolve_write_format(data_dir: DataDir = None, migrate_to_v2: bool = False) -> int:
  """
  Format to use for new writes.

  none/v2 -> v2; v1 -> v1 unless migrate_to_v2.
  """
  detected = detect_snapshot_format(data_dir)
  if detected == FORMAT_NONE or detected == FORMAT_V2 or migrate_to_v2:
    return FORMAT_V2
  return FORMAT_V1

def _has_v2_snapshots(data_dir: DataDir) -> bool:
  requests_dir = data_dir.snapshots_requests_dir_path
  if os.path.isdir(requests_dir):
    for entry in os.listdir(requests_dir):
      if entry.startswith('.'):
        continue
      slug_dir = os.path.join(requests_dir, entry)
      if not os.path.isdir(slug_dir):
        continue
      for name in os.listdir(slug_dir):
        if name.endswith(REQUEST_FILE_EXTENSION):
          return True

  scenarios_dir = data_dir.snapshots_scenarios_dir_path
  if os.path.isdir(scenarios_dir):
    for name in os.listdir(scenarios_dir):
      if name.endswith('.yaml') or name.endswith('.yml'):
        return True

  return False

def _has_v1_snapshots(data_dir: DataDir) -> bool:
  requests_dir = data_dir.snapshots_requests_dir_path
  if os.path.isdir(requests_dir):
    for entry in os.listdir(requests_dir):
      shard_dir = os.path.join(requests_dir, entry)
      if not os.path.isdir(shard_dir):
        continue
      # v1 shards are 2-char hex prefixes
      if len(entry) != 2:
        continue
      for name in os.listdir(shard_dir):
        path = os.path.join(shard_dir, name)
        if os.path.isfile(path) and not name.endswith(REQUEST_FILE_EXTENSION) and UUID_RE.match(name):
          return True

  scenarios_dir = data_dir.snapshots_scenarios_dir_path
  if os.path.isdir(scenarios_dir):
    for name in os.listdir(scenarios_dir):
      path = os.path.join(scenarios_dir, name)
      if os.path.isfile(path) and not name.endswith(('.yaml', '.yml', '.json')) and UUID_RE.match(name):
        return True

  return False
