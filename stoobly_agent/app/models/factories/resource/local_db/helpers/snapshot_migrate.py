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
from .log_event import LogEvent
from .request_slug import (
  REQUEST_FILE_EXTENSION,
  build_request_slug,
  parse_request_relative_path,
  request_relative_path,
  sanitize_scenario_filename,
)
from .snapshot_format import FORMAT_NONE, FORMAT_V1, FORMAT_V2, UUID_RE, detect_snapshot_format


def migrate_snapshots(data_dir: DataDir = None, format: int = FORMAT_V2) -> dict:
  """
  Convert snapshots to the target format.

  Noops when there are no snapshots or they are already the target format.
  Rewrites history locators to match the target format. VERSION is left
  untouched. Returns counts of migrated resources and whether the call was a noop.
  """
  data_dir = data_dir or DataDir.instance()
  detected = detect_snapshot_format(data_dir)

  if detected == FORMAT_NONE or detected == format:
    return {
      'requests': 0,
      'scenarios': 0,
      'noop': True,
    }

  if format == FORMAT_V2:
    result = migrate_snapshots_to_v2(data_dir)
  elif format == FORMAT_V1:
    result = migrate_snapshots_to_v1(data_dir)
  else:
    raise ValueError(f"Unsupported snapshot format: {format}")

  result['noop'] = False
  return result


def migrate_snapshots_to_v2(data_dir: DataDir = None) -> dict:
  """
  Convert all v1 snapshot files under data_dir to v2 layout.

  Also rewrites history locators from bare uuids to slug/uuid and name/uuid
  so .uuid-index is unnecessary. VERSION is left untouched.
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

        slug = build_request_slug(method, path)
        slug_dir = os.path.join(requests_dir, slug)
        os.makedirs(slug_dir, exist_ok=True)

        externalized = externalize_joined_request(joined, slug_dir)
        dest = os.path.join(slug_dir, f"{name}{REQUEST_FILE_EXTENSION}")
        with open(dest, 'wb') as fp:
          fp.write(externalized)

        relative = request_relative_path(slug, name)
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

    # Drop legacy indexes; history locators replace them
    _remove_uuid_index_dir(os.path.join(requests_dir, '.uuid-index'))

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
            parsed = parse_request_relative_path(relative)
            if parsed and request_uuid not in request_uuid_to_locator:
              slug, _uuid = parsed
              request_uuid_to_locator[request_uuid] = f"{slug}/{request_uuid}"

      yaml_name = f"{sanitize_scenario_filename(scenario_name)}.yaml"
      yaml_path = os.path.join(scenarios_dir, yaml_name)
      # Avoid clobbering if name collision
      yaml_path = _unique_path(yaml_path)
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

    _remove_uuid_index_dir(os.path.join(scenarios_dir, '.uuid-index'))

  # Remove empty scenarios/requests dir if empty
  if os.path.isdir(scenario_requests_dir) and not os.listdir(scenario_requests_dir):
    try:
      os.rmdir(scenario_requests_dir)
    except OSError:
      pass

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

    _remove_uuid_index_dir(os.path.join(requests_dir, '.uuid-index'))

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

      request_uuids = []
      for relative in data.get('requests') or []:
        parsed = parse_request_relative_path(relative)
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

    _remove_uuid_index_dir(os.path.join(scenarios_dir, '.uuid-index'))

  _rewrite_history_locators(data_dir, to_v2=False)

  return {
    'requests': migrated_requests,
    'scenarios': migrated_scenarios,
  }


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

  log = Log(data_dir)
  paths = list(log.history_files)
  if os.path.isfile(log.log_file_path):
    paths.append(log.log_file_path)

  for path in paths:
    with open(path, 'r') as fp:
      contents = fp.read().strip()
    if not contents:
      continue

    raw_events = [e for e in contents.split(EVENT_DELIMITTER) if e]
    changed = False
    new_raw_events = []

    for raw in raw_events:
      try:
        event = LogEvent(raw)
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
          if '/' not in event.resource_uuid and event.resource_id in scenario_locators:
            new_resource_uuid = scenario_locators[event.resource_id]
        elif '/' in event.resource_uuid:
          new_resource_uuid = event.resource_id

      if new_resource_uuid != event.resource_uuid:
        changed = True
        event.resource_uuid = new_resource_uuid
        new_raw_events.append(str(event))
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

  # Legacy O(1) lookup for older migrated trees
  index_path = os.path.join(requests_dir, '.uuid-index', uuid)
  if os.path.isfile(index_path):
    with open(index_path, 'r') as fp:
      relative = fp.read().strip().replace('\\', '/')
    if relative:
      return relative

  for slug in os.listdir(requests_dir):
    if slug.startswith('.'):
      continue
    candidate = os.path.join(requests_dir, slug, f"{uuid}{REQUEST_FILE_EXTENSION}")
    if os.path.isfile(candidate):
      return request_relative_path(slug, uuid)
  return None


def _unique_path(path: str) -> str:
  if not os.path.exists(path):
    return path
  base, ext = os.path.splitext(path)
  i = 2
  while True:
    candidate = f"{base}-{i}{ext}"
    if not os.path.exists(candidate):
      return candidate
    i += 1


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


def _remove_uuid_index_dir(index_dir: str):
  if os.path.isdir(index_dir):
    shutil.rmtree(index_dir, ignore_errors=True)
