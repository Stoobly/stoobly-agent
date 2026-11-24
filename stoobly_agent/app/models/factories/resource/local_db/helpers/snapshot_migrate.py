import json
import os
import shutil
from typing import Dict, List, Optional

import yaml

from stoobly_agent.config.data_dir import DataDir

from .joined_request_ref import extract_method_and_path_from_joined
from .log import EVENT_DELIMITTER, Log
from .log_event import LogEvent, LogEventV1, LogEventV2
from .request_snapshot import RequestSnapshot, RequestSnapshotV2
from .scenario_snapshot import ScenarioSnapshotV2
from .snapshot_format import (
  FORMAT_V1,
  FORMAT_V2,
  REQUEST_FILE_EXTENSION,
  UUID_RE,
  has_v1_snapshots,
  has_v2_snapshots,
)
from .yaml_adapter import (
  entry_to_joined,
  is_request_entry,
  iter_scenario_request_entries,
  joined_to_entry,
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
    if (
      not has_v1_snapshots(data_dir)
      and not _needs_v2_yaml_upgrade(data_dir)
      and not (
        has_v2_snapshots(data_dir) and _history_needs_locator_rewrite(data_dir, to_v2=True)
      )
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
  Convert all v1 snapshot files under data_dir to v2 YAML layout.

  Request shards that only exist because a scenario was snapshotted are
  embedded into the scenario YAML (bodies/headers under the slug dir) and do
  **not** get a standalone `requests/<slug>/<uuid>.yaml`. Standalone
  `<uuid>.yaml` files are written only for requests that have a corresponding
  request snapshot in history (REQUEST resource events).

  Also upgrades legacy scenario path-string indexes into structured YAML
  entries. Rewrites history locators from bare uuids to slug/uuid (requests)
  and name/uuid (scenarios). VERSION is left untouched.
  """
  data_dir = data_dir or DataDir.instance()
  migrated_requests = 0
  migrated_scenarios = 0

  request_uuid_to_entry: Dict[str, dict] = {}
  request_uuid_to_locator: Dict[str, str] = {}
  scenario_uuid_to_locator: Dict[str, str] = {}

  standalone_request_uuids = _standalone_request_uuids_from_history(data_dir)
  scenario_request_uuids = _scenario_referenced_request_uuids(data_dir)

  requests_dir = data_dir.snapshots_requests_dir_path
  if os.path.isdir(requests_dir):
    for entry in list(os.listdir(requests_dir)):
      shard_dir = os.path.join(requests_dir, entry)
      if not os.path.isdir(shard_dir) or len(entry) != 2:
        continue

      for name in list(os.listdir(shard_dir)):
        src = os.path.join(shard_dir, name)
        if (
          not os.path.isfile(src)
          or name.endswith(REQUEST_FILE_EXTENSION)
          or not UUID_RE.match(name)
        ):
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

        try:
          entry_data = joined_to_entry(joined, slug_dir, uuid=name)
        except Exception:
          continue

        request_uuid_to_entry[name] = entry_data
        # Keep a standalone yaml only for request-snapshotted UUIDs (or orphans
        # not referenced by any scenario). Scenario-only shards become embeds.
        write_standalone = (
          name in standalone_request_uuids
          or name not in scenario_request_uuids
        )
        if write_standalone:
          dest = os.path.join(slug_dir, f"{name}{REQUEST_FILE_EXTENSION}")
          with open(dest, 'w') as fp:
            yaml.safe_dump(entry_data, fp, sort_keys=False, default_flow_style=False)
          request_uuid_to_locator[name] = f"{slug}/{name}"

        os.remove(src)
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

      request_entries: Dict[str, dict] = {}
      index_path = os.path.join(scenario_requests_dir, scenario_uuid)
      if os.path.exists(index_path):
        with open(index_path, 'r') as fp:
          uuids = [u for u in fp.read().split('\n') if len(u) == 36]
        for request_uuid in uuids:
          entry_data = request_uuid_to_entry.get(request_uuid)
          if not entry_data:
            entry_data = _load_v2_request_entry(requests_dir, request_uuid)
          if entry_data:
            request_entries[request_uuid] = entry_data

      # Reuse existing uuid file when present; otherwise avoid clobbering orphans
      yaml_path = ScenarioSnapshotV2.allocate_yaml_path(
        scenarios_dir, scenario_name, uuid=scenario_uuid
      )
      yaml_stem = _name_from_yaml_filename(os.path.basename(yaml_path))

      with open(yaml_path, 'w') as fp:
        yaml.safe_dump({
          'uuid': scenario_uuid,
          'description': description,
          'requests': request_entries,
        }, fp, sort_keys=False, default_flow_style=False)

      os.remove(meta_path)
      if os.path.exists(index_path):
        os.remove(index_path)

      scenario_uuid_to_locator[scenario_uuid] = f"{yaml_stem}/{scenario_uuid}"
      migrated_scenarios += 1

    migrated_scenarios += _upgrade_scenario_request_entries(
      scenarios_dir, requests_dir, request_uuid_to_entry
    )

  # Drop standalone yaml left over for scenario-only requests
  _remove_scenario_only_request_files(
    requests_dir,
    standalone_request_uuids=standalone_request_uuids,
    scenario_request_uuids=_scenario_referenced_request_uuids(data_dir),
  )

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
  written_request_uuids = set()

  requests_dir = data_dir.snapshots_requests_dir_path
  if os.path.isdir(requests_dir):
    for entry in list(os.listdir(requests_dir)):
      if entry.startswith('.'):
        continue

      slug_dir = os.path.join(requests_dir, entry)
      if not os.path.isdir(slug_dir):
        continue

      request_files = [
        name for name in os.listdir(slug_dir)
        if (
          name.endswith(REQUEST_FILE_EXTENSION)
          and os.path.isfile(os.path.join(slug_dir, name))
        )
      ]
      if not request_files:
        continue

      for name in request_files:
        src = os.path.join(slug_dir, name)
        request_uuid = RequestSnapshot._strip_request_filename_ext(name)
        if not UUID_RE.match(request_uuid):
          continue

        try:
          reconstituted = _reconstitute_v2_request_file(src, slug_dir)
        except Exception:
          # Skip corrupt files; leave them in place
          continue

        shard_dir = os.path.join(requests_dir, request_uuid[0:2])
        os.makedirs(shard_dir, exist_ok=True)
        dest = os.path.join(shard_dir, request_uuid)
        with open(dest, 'wb') as fp:
          fp.write(reconstituted)

        os.remove(src)
        written_request_uuids.add(request_uuid)
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
      requests_field = data.get('requests') or {}
      for request_uuid, entry in iter_scenario_request_entries(requests_field):
        request_uuids.append(request_uuid)
        if request_uuid not in written_request_uuids:
          try:
            slug = RequestSnapshotV2.build_request_slug(
              entry.get('method'),
              _path_from_entry_url(entry.get('url')),
            )
            slug_dir = os.path.join(requests_dir, slug)
            reconstituted = entry_to_joined(entry, slug_dir, uuid=request_uuid)
            shard_dir = os.path.join(requests_dir, request_uuid[0:2])
            os.makedirs(shard_dir, exist_ok=True)
            with open(os.path.join(shard_dir, request_uuid), 'wb') as fp:
              fp.write(reconstituted)
            written_request_uuids.add(request_uuid)
            migrated_requests += 1
          except Exception:
            pass

      # Legacy v2: list of relative path strings
      if isinstance(requests_field, list):
        for item in requests_field:
          if not isinstance(item, str):
            continue
          parsed = RequestSnapshotV2.parse_request_relative_path(item)
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
      request_uuid = RequestSnapshot._strip_request_filename_ext(name)
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


def _name_from_yaml_filename(filename: str) -> str:
  for ext in ('.yaml', '.yml'):
    if filename.endswith(ext):
      return filename[:-len(ext)]
  return filename


def _path_from_entry_url(url: Optional[str]) -> str:
  if not url:
    return '/'
  if '://' in url:
    from urllib.parse import urlparse
    return urlparse(url).path or '/'
  return url.split('?', 1)[0] or '/'


def _needs_v2_yaml_upgrade(data_dir: DataDir) -> bool:
  """True when path-string scenario indexes remain."""
  scenarios_dir = data_dir.snapshots_scenarios_dir_path
  if os.path.isdir(scenarios_dir):
    for name in os.listdir(scenarios_dir):
      if not (name.endswith('.yaml') or name.endswith('.yml')):
        continue
      path = os.path.join(scenarios_dir, name)
      if not os.path.isfile(path):
        continue
      try:
        with open(path, 'r') as fp:
          data = yaml.safe_load(fp) or {}
        if not isinstance(data, dict):
          continue
        for item in data.get('requests') or []:
          if isinstance(item, str):
            return True
      except Exception:
        continue
  return False


def _standalone_request_uuids_from_history(data_dir: DataDir) -> set:
  """UUIDs that have a request-resource history event (standalone request snapshot)."""
  uuids = set()
  for path in _history_file_paths(data_dir):
    try:
      with open(path, 'r') as fp:
        contents = fp.read()
    except OSError:
      continue
    for raw in contents.split(EVENT_DELIMITTER):
      if not raw or not raw.strip():
        continue
      try:
        event = LogEvent.create(raw)
      except Exception:
        continue
      if event.is_request() and event.resource_id and UUID_RE.match(str(event.resource_id)):
        uuids.add(str(event.resource_id))
  return uuids


def _scenario_referenced_request_uuids(data_dir: DataDir) -> set:
  """
  Request UUIDs listed by scenario snapshots (v1 index and v2 YAML embeds/paths).
  """
  uuids = set()
  scenario_requests_dir = data_dir.snapshots_scenario_requests_dir_path
  if os.path.isdir(scenario_requests_dir):
    for name in os.listdir(scenario_requests_dir):
      index_path = os.path.join(scenario_requests_dir, name)
      if not os.path.isfile(index_path):
        continue
      try:
        with open(index_path, 'r') as fp:
          for request_uuid in fp.read().split('\n'):
            if len(request_uuid) == 36 and UUID_RE.match(request_uuid):
              uuids.add(request_uuid)
      except OSError:
        continue

  scenarios_dir = data_dir.snapshots_scenarios_dir_path
  if os.path.isdir(scenarios_dir):
    for name in os.listdir(scenarios_dir):
      if not (name.endswith('.yaml') or name.endswith('.yml')):
        continue
      path = os.path.join(scenarios_dir, name)
      if not os.path.isfile(path):
        continue
      try:
        with open(path, 'r') as fp:
          data = yaml.safe_load(fp) or {}
      except Exception:
        continue
      if not isinstance(data, dict):
        continue
      requests_field = data.get('requests') or {}
      for request_uuid, _entry in iter_scenario_request_entries(requests_field):
        uuids.add(request_uuid)
      if isinstance(requests_field, list):
        for item in requests_field:
          if not isinstance(item, str):
            continue
          parsed = RequestSnapshotV2.parse_request_relative_path(item)
          if parsed:
            _slug, request_uuid = parsed
            if UUID_RE.match(request_uuid):
              uuids.add(request_uuid)

  return uuids


def _should_write_standalone_request(
  request_uuid: str,
  standalone_request_uuids: set = None,
  scenario_request_uuids: set = None,
) -> bool:
  standalone_request_uuids = standalone_request_uuids or set()
  scenario_request_uuids = scenario_request_uuids or set()
  return (
    request_uuid in standalone_request_uuids
    or request_uuid not in scenario_request_uuids
  )


def _remove_scenario_only_request_files(
  requests_dir: str,
  standalone_request_uuids: set = None,
  scenario_request_uuids: set = None,
):
  """
  Delete standalone request yaml files that are only scenario-referenced.

  Do not wipe bodies/headers: scenario embeds still reference those files under
  the slug dir even when no standalone <uuid>.yaml remains.
  """
  if not os.path.isdir(requests_dir):
    return

  standalone_request_uuids = standalone_request_uuids or set()
  scenario_request_uuids = scenario_request_uuids or set()

  for slug in list(os.listdir(requests_dir)):
    if slug.startswith('.'):
      continue
    slug_dir = os.path.join(requests_dir, slug)
    if not os.path.isdir(slug_dir):
      continue

    for name in list(os.listdir(slug_dir)):
      if not name.endswith(REQUEST_FILE_EXTENSION):
        continue
      request_uuid = RequestSnapshot._strip_request_filename_ext(name)
      if not UUID_RE.match(request_uuid):
        continue
      if _should_write_standalone_request(
        request_uuid, standalone_request_uuids, scenario_request_uuids
      ):
        continue
      path = os.path.join(slug_dir, name)
      try:
        os.remove(path)
      except OSError:
        continue


def _upgrade_scenario_request_entries(
  scenarios_dir: str,
  requests_dir: str,
  request_uuid_to_entry: Dict[str, dict],
) -> int:
  migrated = 0
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
        continue
    except Exception:
      continue

    requests = data.get('requests') or {}
    # Upgrade legacy list indexes (path strings or entries with inlined uuid)
    # into a uuid-keyed dict. Already-keyed dicts are left alone.
    if isinstance(requests, dict):
      continue
    if not isinstance(requests, list):
      continue

    entries: Dict[str, dict] = {}
    changed = False
    for item in requests:
      if is_request_entry(item):
        request_uuid = str(item.get('uuid') or '')
        if UUID_RE.match(request_uuid):
          entries[request_uuid] = {k: v for k, v in item.items() if k != 'uuid'}
          changed = True
        continue
      if not isinstance(item, str):
        continue
      parsed = RequestSnapshotV2.parse_request_relative_path(item)
      if not parsed:
        continue
      _slug, request_uuid = parsed
      entry_data = request_uuid_to_entry.get(request_uuid) or _load_v2_request_entry(
        requests_dir, request_uuid
      )
      if entry_data:
        entries[request_uuid] = {k: v for k, v in entry_data.items() if k != 'uuid'}
        changed = True

    if not changed:
      continue

    data['requests'] = entries
    with open(yaml_path, 'w') as fp:
      yaml.safe_dump(data, fp, sort_keys=False, default_flow_style=False)
    migrated += 1

  return migrated


def _load_v2_request_entry(requests_dir: str, uuid: str) -> Optional[dict]:
  if not os.path.isdir(requests_dir) or not UUID_RE.match(uuid):
    return None

  for slug in os.listdir(requests_dir):
    if slug.startswith('.'):
      continue
    slug_dir = os.path.join(requests_dir, slug)
    if not os.path.isdir(slug_dir):
      continue

    yaml_path = os.path.join(slug_dir, f"{uuid}{REQUEST_FILE_EXTENSION}")
    if os.path.isfile(yaml_path):
      try:
        with open(yaml_path, 'r') as fp:
          data = yaml.safe_load(fp) or {}
        if isinstance(data, dict):
          data.pop('uuid', None)
          return data
      except Exception:
        return None

  return None


def _reconstitute_v2_request_file(path: str, slug_dir: str) -> bytes:
  with open(path, 'r') as fp:
    data = yaml.safe_load(fp) or {}
  if not isinstance(data, dict):
    raise ValueError('invalid yaml')
  request_uuid = RequestSnapshot._strip_request_filename_ext(os.path.basename(path))
  return entry_to_joined(data, slug_dir, uuid=request_uuid)


def _cleanup_slug_dir(slug_dir: str):
  if not os.path.isdir(slug_dir):
    return

  remaining = [
    n for n in os.listdir(slug_dir)
    if n.endswith(REQUEST_FILE_EXTENSION)
  ]
  if remaining:
    return

  bodies_dir = os.path.join(slug_dir, 'bodies')
  if os.path.isdir(bodies_dir):
    shutil.rmtree(bodies_dir, ignore_errors=True)

  headers_dir = os.path.join(slug_dir, 'headers')
  if os.path.isdir(headers_dir):
    shutil.rmtree(headers_dir, ignore_errors=True)

  try:
    if not os.listdir(slug_dir):
      os.rmdir(slug_dir)
  except OSError:
    pass
