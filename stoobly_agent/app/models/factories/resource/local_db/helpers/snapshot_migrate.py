import json
import os
import shutil
from typing import Dict, Optional

import yaml

from stoobly_agent.config.data_dir import DataDir

from .body_ref import (
  externalize_joined_request,
  extract_method_and_path_from_joined,
  reconstitute_joined_request,
)
from .log import EVENT_DELIMITTER, Log
from .log_event import LogEvent, LogEventV1, LogEventV2
from .request_snapshot import RequestSnapshotV2
from .scenario_snapshot import ScenarioSnapshotV2
from .snapshot_format import (
  FORMAT_V1,
  FORMAT_V2,
  REQUEST_FILE_EXTENSION,
  UUID_RE,
  has_v1_snapshots,
  has_v2_snapshots,
)


def migrate_snapshots(data_dir: DataDir = None, format: int = FORMAT_V2) -> dict:
  """
  Convert snapshots to the target format.

  Noops when there is nothing left to do. Keying off source presence (not
  detect_snapshot_format) so an interrupted migrate that left a mixed tree
  still finishes remaining files — detect prefers v2 as soon as any v2 file
  exists. Also treats unfinished history rewrite as work remaining: if files
  are already in the target format but history still has source-shaped
  locators (interrupt after the last source file was removed), remigrate runs
  backfill + rewrite instead of nooping.

  Rewrites history locators to match the target format. VERSION is left
  untouched. Returns counts of migrated resources and whether the call was a noop.
  """
  data_dir = data_dir or DataDir.instance()

  if format == FORMAT_V2:
    if not has_v1_snapshots(data_dir) and not (
      has_v2_snapshots(data_dir) and _history_needs_locator_rewrite(data_dir, to_v2=True)
    ):
      return {
        'requests': 0,
        'scenarios': 0,
        'noop': True,
      }
    result = migrate_snapshots_to_v2(data_dir)
  elif format == FORMAT_V1:
    if not has_v2_snapshots(data_dir) and not (
      has_v1_snapshots(data_dir) and _history_needs_locator_rewrite(data_dir, to_v2=False)
    ):
      return {
        'requests': 0,
        'scenarios': 0,
        'noop': True,
      }
    result = migrate_snapshots_to_v1(data_dir)
  else:
    raise ValueError(f"Unsupported snapshot format: {format}")

  result['noop'] = False
  return result


def migrate_snapshots_to_v2(data_dir: DataDir = None) -> dict:
  """
  Convert all v1 snapshot files under data_dir to v2 layout.

  Also rewrites history locators from bare uuids to slug/uuid (requests) and
  unique name (scenarios). VERSION is left untouched.
  """
  data_dir = data_dir or DataDir.instance()
  migrated_requests = 0
  migrated_scenarios = 0

  request_uuid_to_relative: Dict[str, str] = {}
  request_uuid_to_locator: Dict[str, str] = {}
  scenario_uuid_to_locator: Dict[str, str] = {}

  requests_dir = data_dir.snapshots_requests_dir_path
  if os.path.isdir(requests_dir):
    for entry in list(os.listdir(requests_dir)):
      shard_dir = os.path.join(requests_dir, entry)
      if not os.path.isdir(shard_dir) or len(entry) != 2:
        continue

      for name in list(os.listdir(shard_dir)):
        src = os.path.join(shard_dir, name)
        if not os.path.isfile(src) or name.endswith(REQUEST_FILE_EXTENSION) or not UUID_RE.match(name):
          continue

        with open(src, 'rb') as fp:
          joined = fp.read()

        try:
          method, path = extract_method_and_path_from_joined(joined)
        except Exception:
          # Skip corrupt files; leave them in place
          continue

        slug = RequestSnapshotV2.build_request_slug(method, path)
        slug_dir = os.path.join(requests_dir, slug)
        os.makedirs(slug_dir, exist_ok=True)

        externalized = externalize_joined_request(joined, slug_dir)
        dest = os.path.join(slug_dir, f"{name}{REQUEST_FILE_EXTENSION}")
        with open(dest, 'wb') as fp:
          fp.write(externalized)

        relative = RequestSnapshotV2.request_relative_path(slug, name)
        os.remove(src)
        request_uuid_to_relative[name] = relative
        request_uuid_to_locator[name] = f"{slug}/{name}"
        migrated_requests += 1

      # Remove empty shard dirs
      try:
        if os.path.isdir(shard_dir) and not os.listdir(shard_dir):
          os.rmdir(shard_dir)
      except OSError:
        pass

  scenarios_dir = data_dir.snapshots_scenarios_dir_path
  scenario_requests_dir = data_dir.snapshots_scenario_requests_dir_path

  if os.path.isdir(scenarios_dir):
    for name in list(os.listdir(scenarios_dir)):
      meta_path = os.path.join(scenarios_dir, name)
      if not os.path.isfile(meta_path):
        continue
      if name.endswith(('.yaml', '.yml')):
        continue
      if not UUID_RE.match(name):
        continue

      scenario_uuid = name
      try:
        with open(meta_path, 'r') as fp:
          meta = json.loads(fp.read())
      except Exception:
        meta = {'name': scenario_uuid, 'description': ''}

      scenario_name = meta.get('name') or scenario_uuid
      description = meta.get('description') or ''

      relative_requests = []
      index_path = os.path.join(scenario_requests_dir, scenario_uuid)
      if os.path.exists(index_path):
        with open(index_path, 'r') as fp:
          uuids = [u for u in fp.read().split('\n') if len(u) == 36]
        for request_uuid in uuids:
          relative = request_uuid_to_relative.get(request_uuid)
          if not relative:
            # Request may already be v2 or missing; try resolve from disk
            relative = _find_v2_relative(requests_dir, request_uuid)
          if relative:
            relative_requests.append(relative)
            parsed = RequestSnapshotV2.parse_request_relative_path(relative)
            if parsed and request_uuid not in request_uuid_to_locator:
              slug, _uuid = parsed
              request_uuid_to_locator[request_uuid] = f"{slug}/{request_uuid}"

      # Reuse existing uuid file when present; otherwise avoid clobbering orphans
      yaml_path = ScenarioSnapshotV2.allocate_yaml_path(
        scenarios_dir, scenario_name, uuid=scenario_uuid
      )
      yaml_stem = _name_from_yaml_filename(os.path.basename(yaml_path))

      with open(yaml_path, 'w') as fp:
        yaml.safe_dump({
          'uuid': scenario_uuid,
          'description': description,
          'requests': relative_requests,
        }, fp, sort_keys=False, default_flow_style=False)

      os.remove(meta_path)
      if os.path.exists(index_path):
        os.remove(index_path)

      scenario_uuid_to_locator[scenario_uuid] = f"{yaml_stem}/{scenario_uuid}"
      migrated_scenarios += 1

  # Remove empty scenarios/requests dir if empty
  if os.path.isdir(scenario_requests_dir) and not os.listdir(scenario_requests_dir):
    try:
      os.rmdir(scenario_requests_dir)
    except OSError:
      pass

  # Remigrate after interrupt: include already-v2 files so history rewrite
  # covers requests/scenarios converted in a prior partial run.
  _backfill_v2_request_locators(requests_dir, request_uuid_to_locator)
  _backfill_v2_scenario_locators(scenarios_dir, scenario_uuid_to_locator)

  _rewrite_history_locators(
    data_dir,
    to_v2=True,
    request_locators=request_uuid_to_locator,
    scenario_locators=scenario_uuid_to_locator,
  )

  return {
    'requests': migrated_requests,
    'scenarios': migrated_scenarios,
  }


def migrate_snapshots_to_v1(data_dir: DataDir = None) -> dict:
  """
  Convert all v2 snapshot files under data_dir to v1 layout.

  Also rewrites history locators back to bare uuids. VERSION is left untouched.
  """
  data_dir = data_dir or DataDir.instance()
  migrated_requests = 0
  migrated_scenarios = 0
  scenario_name_to_uuid: Dict[str, str] = {}

  requests_dir = data_dir.snapshots_requests_dir_path
  if os.path.isdir(requests_dir):
    for entry in list(os.listdir(requests_dir)):
      if entry.startswith('.'):
        continue

      slug_dir = os.path.join(requests_dir, entry)
      if not os.path.isdir(slug_dir):
        continue

      http_files = [
        name for name in os.listdir(slug_dir)
        if name.endswith(REQUEST_FILE_EXTENSION) and os.path.isfile(os.path.join(slug_dir, name))
      ]
      if not http_files:
        continue

      for name in http_files:
        src = os.path.join(slug_dir, name)
        request_uuid = name[:-len(REQUEST_FILE_EXTENSION)]
        if not UUID_RE.match(request_uuid):
          continue

        with open(src, 'rb') as fp:
          joined = fp.read()

        try:
          reconstituted = reconstitute_joined_request(joined, slug_dir)
        except Exception:
          # Skip corrupt files; leave them in place
          continue

        shard_dir = os.path.join(requests_dir, request_uuid[0:2])
        os.makedirs(shard_dir, exist_ok=True)
        dest = os.path.join(shard_dir, request_uuid)
        with open(dest, 'wb') as fp:
          fp.write(reconstituted)

        os.remove(src)
        migrated_requests += 1

      _cleanup_slug_dir(slug_dir)

  scenarios_dir = data_dir.snapshots_scenarios_dir_path
  scenario_requests_dir = data_dir.snapshots_scenario_requests_dir_path

  if os.path.isdir(scenarios_dir):
    for name in list(os.listdir(scenarios_dir)):
      if not (name.endswith('.yaml') or name.endswith('.yml')):
        continue

      yaml_path = os.path.join(scenarios_dir, name)
      if not os.path.isfile(yaml_path):
        continue

      try:
        with open(yaml_path, 'r') as fp:
          data = yaml.safe_load(fp) or {}
        if not isinstance(data, dict):
          raise ValueError('invalid yaml')
      except Exception:
        # Skip corrupt files; leave them in place
        continue

      scenario_uuid = data.get('uuid')
      if not scenario_uuid or not UUID_RE.match(str(scenario_uuid)):
        continue
      scenario_uuid = str(scenario_uuid)

      scenario_name = data.get('name') or _name_from_yaml_filename(name)
      description = data.get('description') or ''
      yaml_stem = _name_from_yaml_filename(name)
      scenario_name_to_uuid[yaml_stem] = scenario_uuid

      request_uuids = []
      for relative in data.get('requests') or []:
        parsed = RequestSnapshotV2.parse_request_relative_path(relative)
        if not parsed:
          continue
        _, request_uuid = parsed
        if UUID_RE.match(request_uuid):
          request_uuids.append(request_uuid)

      meta_path = os.path.join(scenarios_dir, scenario_uuid)
      with open(meta_path, 'w') as fp:
        fp.write(json.dumps({
          'description': description,
          'name': scenario_name,
        }))

      os.makedirs(scenario_requests_dir, exist_ok=True)
      index_path = os.path.join(scenario_requests_dir, scenario_uuid)
      with open(index_path, 'w') as fp:
        fp.write('\n'.join(request_uuids))

      os.remove(yaml_path)
      migrated_scenarios += 1

  # Remigrate after interrupt: include already-v1 scenario metas so name
  # locators from a prior partial run still resolve to bare uuids.
  _backfill_v1_scenario_locators(scenarios_dir, scenario_name_to_uuid)

  _rewrite_history_locators(
    data_dir,
    to_v2=False,
    scenario_locators=scenario_name_to_uuid,
  )

  return {
    'requests': migrated_requests,
    'scenarios': migrated_scenarios,
  }


def _backfill_v2_request_locators(requests_dir: str, locators: Dict[str, str]):
  if not os.path.isdir(requests_dir):
    return
  for slug in os.listdir(requests_dir):
    if slug.startswith('.'):
      continue
    slug_dir = os.path.join(requests_dir, slug)
    if not os.path.isdir(slug_dir):
      continue
    for name in os.listdir(slug_dir):
      if not name.endswith(REQUEST_FILE_EXTENSION):
        continue
      request_uuid = name[:-len(REQUEST_FILE_EXTENSION)]
      if UUID_RE.match(request_uuid) and request_uuid not in locators:
        locators[request_uuid] = f"{slug}/{request_uuid}"


def _backfill_v2_scenario_locators(scenarios_dir: str, locators: Dict[str, str]):
  if not os.path.isdir(scenarios_dir):
    return
  for name in os.listdir(scenarios_dir):
    if not (name.endswith('.yaml') or name.endswith('.yml')):
      continue
    yaml_path = os.path.join(scenarios_dir, name)
    if not os.path.isfile(yaml_path):
      continue
    try:
      with open(yaml_path, 'r') as fp:
        data = yaml.safe_load(fp) or {}
      if not isinstance(data, dict):
        continue
      scenario_uuid = data.get('uuid')
      if scenario_uuid and UUID_RE.match(str(scenario_uuid)):
        scenario_uuid = str(scenario_uuid)
        if scenario_uuid not in locators:
          stem = _name_from_yaml_filename(name)
          locators[scenario_uuid] = f"{stem}/{scenario_uuid}"
    except Exception:
      continue


def _backfill_v1_scenario_locators(scenarios_dir: str, locators: Dict[str, str]):
  if not os.path.isdir(scenarios_dir):
    return
  for name in os.listdir(scenarios_dir):
    if name.endswith(('.yaml', '.yml', '.json')) or not UUID_RE.match(name):
      continue
    meta_path = os.path.join(scenarios_dir, name)
    if not os.path.isfile(meta_path):
      continue
    try:
      with open(meta_path, 'r') as fp:
        meta = json.loads(fp.read())
      scenario_name = (meta or {}).get('name') or name
      if scenario_name not in locators:
        locators[scenario_name] = name
    except Exception:
      continue


def _history_file_paths(data_dir: DataDir) -> list:
  log = Log(data_dir)
  paths = list(log.history_files)
  if os.path.isfile(log.log_file_path):
    paths.append(log.log_file_path)
  return paths


def _history_needs_locator_rewrite(data_dir: DataDir, to_v2: bool) -> bool:
  """
  True when history/log still has locators that rewrite would change.

  Used so remigrate after an interrupt that removed the last source file still
  runs backfill + rewrite instead of nooping on a pure target-format tree.
  Only counts locators resolvable from on-disk target-format files so orphaned
  lines do not permanently block noop.
  """
  request_locators: Dict[str, str] = {}
  scenario_locators: Dict[str, str] = {}
  if to_v2:
    _backfill_v2_request_locators(data_dir.snapshots_requests_dir_path, request_locators)
    _backfill_v2_scenario_locators(data_dir.snapshots_scenarios_dir_path, scenario_locators)
  else:
    _backfill_v1_scenario_locators(data_dir.snapshots_scenarios_dir_path, scenario_locators)

  for path in _history_file_paths(data_dir):
    with open(path, 'r') as fp:
      contents = fp.read().strip()
    if not contents:
      continue

    for raw in contents.split(EVENT_DELIMITTER):
      if not raw:
        continue
      try:
        event = LogEvent.create(raw)
      except Exception:
        continue

      if event.is_request():
        if to_v2:
          if '/' not in event.resource_uuid and event.resource_id in request_locators:
            return True
        elif '/' in event.resource_uuid:
          return True
      elif event.is_scenario():
        if to_v2:
          # bare uuid → name/uuid; stale name/uuid → canonical
          if '/' in event.resource_uuid:
            _name, rest = event.resource_uuid.rsplit('/', 1)
            if UUID_RE.match(rest):
              canonical = scenario_locators.get(rest)
              if canonical and canonical != event.resource_uuid:
                return True
          elif UUID_RE.match(event.resource_uuid):
            if event.resource_uuid in scenario_locators:
              return True
        else:
          if '/' in event.resource_uuid:
            _name, rest = event.resource_uuid.rsplit('/', 1)
            if UUID_RE.match(rest):
              return True

  return False


def _rewrite_history_locators(
  data_dir: DataDir,
  to_v2: bool,
  request_locators: Dict[str, str] = None,
  scenario_locators: Dict[str, str] = None,
):
  """
  Rewrite history/log resource fields between bare uuid and v2 locators.
  """
  request_locators = request_locators or {}
  scenario_locators = scenario_locators or {}

  for path in _history_file_paths(data_dir):
    with open(path, 'r') as fp:
      contents = fp.read().strip()
    if not contents:
      continue

    raw_events = [e for e in contents.split(EVENT_DELIMITTER) if e]
    changed = False
    new_raw_events = []

    for raw in raw_events:
      try:
        event = LogEvent.create(raw)
      except Exception:
        new_raw_events.append(raw)
        continue

      new_resource_uuid = event.resource_uuid

      if event.is_request():
        if to_v2:
          if '/' not in event.resource_uuid and event.resource_id in request_locators:
            new_resource_uuid = request_locators[event.resource_id]
        elif '/' in event.resource_uuid:
          new_resource_uuid = event.resource_id
      elif event.is_scenario():
        if to_v2:
          # bare uuid / stale name/uuid → canonical {stem}/{uuid}
          # (uuid map required after sanitize collisions, e.g. dup-name-2)
          if '/' in event.resource_uuid:
            _name, rest = event.resource_uuid.rsplit('/', 1)
            if UUID_RE.match(rest) and rest in scenario_locators:
              new_resource_uuid = scenario_locators[rest]
          elif UUID_RE.match(event.resource_uuid) and event.resource_uuid in scenario_locators:
            new_resource_uuid = scenario_locators[event.resource_uuid]
        else:
          # name/uuid → bare uuid
          if '/' in event.resource_uuid:
            _name, rest = event.resource_uuid.rsplit('/', 1)
            if UUID_RE.match(rest):
              new_resource_uuid = rest

      event.resource_uuid = new_resource_uuid
      if to_v2:
        # uuid timestamp action resource resource_id
        new_line = LogEventV2.format_line(
          event.uuid, event.created_at, event.action, event.resource, new_resource_uuid,
        )
      else:
        # uuid resource locator action [timestamp]
        new_line = LogEventV1.format_line(
          event.uuid, event.created_at, event.action, event.resource, new_resource_uuid,
        )

      if new_line != raw:
        changed = True
        new_raw_events.append(new_line)
      else:
        new_raw_events.append(raw)

    if changed:
      with open(path, 'w') as fp:
        fp.write(EVENT_DELIMITTER.join(new_raw_events))
        if new_raw_events:
          fp.write(EVENT_DELIMITTER)


def _find_v2_relative(requests_dir: str, uuid: str) -> Optional[str]:
  if not os.path.isdir(requests_dir):
    return None

  for slug in os.listdir(requests_dir):
    if slug.startswith('.'):
      continue
    candidate = os.path.join(requests_dir, slug, f"{uuid}{REQUEST_FILE_EXTENSION}")
    if os.path.isfile(candidate):
      return RequestSnapshotV2.request_relative_path(slug, uuid)
  return None


def _name_from_yaml_filename(filename: str) -> str:
  for ext in ('.yaml', '.yml'):
    if filename.endswith(ext):
      return filename[:-len(ext)]
  return filename


def _cleanup_slug_dir(slug_dir: str):
  if not os.path.isdir(slug_dir):
    return

  remaining_http = [n for n in os.listdir(slug_dir) if n.endswith(REQUEST_FILE_EXTENSION)]
  if remaining_http:
    return

  bodies_dir = os.path.join(slug_dir, 'bodies')
  if os.path.isdir(bodies_dir):
    shutil.rmtree(bodies_dir, ignore_errors=True)

  try:
    if not os.listdir(slug_dir):
      os.rmdir(slug_dir)
  except OSError:
    pass
