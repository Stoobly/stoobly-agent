import json
import os
import re
from typing import Any, Callable, Dict, List, Optional

import yaml

from stoobly_agent.app.models.adapters.snapshot.yaml_dump import dump_snapshot_yaml
from stoobly_agent.config.data_dir import DataDir
from stoobly_agent.lib.orm.scenario import Scenario

from .request_snapshot import RequestSnapshot, RequestSnapshotV1, RequestSnapshotV2, RequestSnapshotOptions
from .snapshot import Snapshot
from .snapshot_format import FORMAT_V1, FORMAT_V2, UUID_RE, resolve_write_format

REQUEST_DELIMITTER = "\n"
# Only path separators and controls (history is newline-delimited; resource id may have spaces).
SAFE_NAME_RE = re.compile(r'[/\\\x00-\x1f]+')


class ScenarioSnapshot(Snapshot):
  """Base scenario snapshot. Prefer create(), from_path(), or V1/V2 subclasses."""

  FORMAT = None

  @staticmethod
  def is_request_entry(value: Any) -> bool:
    """True if value looks like a structured request entry (not a path string)."""
    return (
      isinstance(value, dict)
      and 'headers' in value
      and 'response' in value
      and 'method' in value
    )

  @staticmethod
  def iter_request_entries(requests_field: Any):
    """
    Yield (uuid, entry) from scenario YAML `requests`.

    Current form is a uuid-keyed dict. Also accepts a legacy list of entries that
    still embedded `uuid` (entry returned without that field).
    """
    if isinstance(requests_field, dict):
      for request_uuid, entry in requests_field.items():
        if ScenarioSnapshot.is_request_entry(entry) and UUID_RE.match(str(request_uuid)):
          yield str(request_uuid), entry
      return

    if not isinstance(requests_field, list):
      return

    for item in requests_field:
      if not ScenarioSnapshot.is_request_entry(item):
        continue
      request_uuid = str(item.get('uuid') or '')
      if not UUID_RE.match(request_uuid):
        continue
      yield request_uuid, {k: v for k, v in item.items() if k != 'uuid'}

  def __init__(self, uuid: str, data_dir: DataDir = None, name: str = None):
    parsed_uuid, parsed_name = self._parse_scenario_ref(uuid, name)
    # Snapshot requires a uuid string; hydrate from YAML when opened by stem
    super().__init__(parsed_uuid or parsed_name or '', data_dir)

    self._scenarios_dir_path = self.data_dir.snapshots_scenarios_dir_path
    self._scenario_requests_dir_path = self.data_dir.snapshots_scenario_requests_dir_path
    self._name = parsed_name
    self._metadata_backup = None
    self._requests_backup = None
    self._resolved_metadata_path = None
    self._resolved_uuid = parsed_uuid if parsed_uuid and UUID_RE.match(str(parsed_uuid)) else None

  @staticmethod
  def _parse_scenario_ref(uuid: str, name: str = None):
    """
    Parse history-style refs into (uuid, name).

    Accepts:
    - name/<uuid> (v2)
    - bare uuid (v1)
    """
    parsed_name = name
    parsed_uuid = uuid

    if uuid and '/' in uuid:
      parsed_name, rest = uuid.rsplit('/', 1)
      if rest.endswith('.yaml') or rest.endswith('.yml'):
        rest = rest.rsplit('.', 1)[0]
      parsed_uuid = rest
      parsed_name = name or parsed_name
      return parsed_uuid, parsed_name

    return parsed_uuid, parsed_name

  @staticmethod
  def _uuid_from_v2_yaml(path: str) -> Optional[str]:
    try:
      with open(path, 'r') as fp:
        data = yaml.safe_load(fp) or {}
      if isinstance(data, dict):
        found = data.get('uuid')
        if found and UUID_RE.match(str(found)):
          return str(found)
    except Exception:
      pass
    return None

  @staticmethod
  def _safe_scenario_yaml_path(scenarios_dir: str, name: str) -> Optional[str]:
    """
    Join scenarios_dir/{sanitized_name}.yaml without allowing path escape.

    History-derived names may contain ../ or separators; sanitize to a single
    basename component before joining (same idea as request slug sanitization).

    Prefers an existing .yaml, then an existing .yml; otherwise returns the
    .yaml path for new writes.
    """
    if not name:
      return None
    safe = ScenarioSnapshotV2.sanitize_scenario_filename(name)
    abs_dir = os.path.abspath(scenarios_dir)
    chosen = None
    for ext in ('.yaml', '.yml'):
      path = os.path.join(scenarios_dir, f'{safe}{ext}')
      abs_path = os.path.abspath(path)
      if os.path.commonpath([abs_path, abs_dir]) != abs_dir:
        return None
      if os.path.isfile(path):
        return path
      if chosen is None:
        chosen = path
    return chosen

  @staticmethod
  def _detect_scenario_format(uuid: str, data_dir: DataDir, name: str = None) -> int:
    scenarios_dir = data_dir.snapshots_scenarios_dir_path

    if name:
      candidate = ScenarioSnapshot._safe_scenario_yaml_path(scenarios_dir, name)
      if candidate and os.path.isfile(candidate):
        return FORMAT_V2

    if uuid:
      if os.path.isdir(scenarios_dir):
        for entry in os.listdir(scenarios_dir):
          if not (entry.endswith('.yaml') or entry.endswith('.yml')):
            continue
          path = os.path.join(scenarios_dir, entry)
          if not os.path.isfile(path):
            continue
          try:
            with open(path, 'r') as fp:
              data = yaml.safe_load(fp) or {}
            if isinstance(data, dict) and data.get('uuid') == uuid:
              return FORMAT_V2
          except Exception:
            continue

      v1_meta = os.path.join(scenarios_dir, uuid)
      if os.path.exists(v1_meta):
        return FORMAT_V1

    return resolve_write_format(data_dir)

  @classmethod
  def create(
    cls,
    uuid: str,
    data_dir: DataDir = None,
    name: str = None,
    format: int = None,
  ) -> 'ScenarioSnapshot':
    data_dir = data_dir or DataDir.instance()
    # Open by on-disk yaml stem (filesystem helper, not a history locator)
    if (
      uuid
      and name is None
      and '/' not in str(uuid)
      and not UUID_RE.match(str(uuid))
    ):
      name = uuid
      uuid = ''

    parsed_uuid, parsed_name = cls._parse_scenario_ref(uuid, name)

    if format is None:
      if parsed_name:
        format = FORMAT_V2
      else:
        format = cls._detect_scenario_format(parsed_uuid, data_dir, parsed_name)

    if format == FORMAT_V2:
      snapshot = ScenarioSnapshotV2(parsed_uuid or '', data_dir, name=parsed_name)
      snapshot._hydrate_uuid_from_metadata()
      return snapshot
    return ScenarioSnapshotV1(parsed_uuid, data_dir)

  @classmethod
  def from_path(
    cls,
    path: str,
    data_dir: DataDir = None,
    uuid: str = None,
  ) -> Optional['ScenarioSnapshot']:
    """
    Build a scenario snapshot from a filesystem path.

    v1: .../scenarios/{uuid}
    v2: .../scenarios/{name}.yaml
    """
    data_dir = data_dir or DataDir.instance()
    abs_path = os.path.abspath(path)
    scenarios_dir = data_dir.snapshots_scenarios_dir_path
    rel_path = os.path.relpath(abs_path, scenarios_dir)
    if rel_path.startswith('..'):
      return None

    parts = [p for p in rel_path.split(os.sep) if p]
    if len(parts) < 1:
      return None

    basename = parts[0]
    if basename.endswith(('.yaml', '.yml')):
      name = basename.rsplit('.', 1)[0]
      snapshot = cls.create('', data_dir=data_dir, name=name)
      if uuid:
        snapshot._resolved_uuid = uuid
      elif not snapshot._resolved_uuid:
        return None
      return snapshot

    return cls.create(uuid or basename, data_dir=data_dir)

  @property
  def uuid(self):
    if self._resolved_uuid:
      return self._resolved_uuid
    return super().uuid

  def _hydrate_uuid_from_metadata(self):
    if self._resolved_uuid:
      return
    path = self.metadata_path
    if path and os.path.isfile(path):
      found = self._uuid_from_v2_yaml(path)
      if found:
        self._resolved_uuid = found

  @property
  def format(self) -> int:
    return self.FORMAT

  @property
  def exists(self):
    raise NotImplementedError

  @property
  def metadata(self):
    """Return apply-compatible metadata: name + description only."""
    data = self._load_metadata_data()
    if not data:
      return {}
    return {
      'name': data.get('name') or self.uuid,
      'description': data.get('description') or '',
    }

  @property
  def metadata_backup(self):
    return self._metadata_backup

  @property
  def metadata_path(self):
    raise NotImplementedError

  @property
  def request_snapshots(self) -> List[RequestSnapshot]:
    snapshots = []
    self.iter_request_snapshots(lambda snapshot: snapshots.append(snapshot))
    return snapshots

  @property
  def requests(self):
    if not self.exists:
      return

    raw_requests = []
    self.iter_request_snapshots(lambda snapshot: raw_requests.append(snapshot.request))
    return raw_requests

  @property
  def requests_backup(self):
    return self._requests_backup

  @property
  def requests_path(self):
    """v1 request-index path. Unused for v2 (requests live in YAML)."""
    return os.path.join(self._scenario_requests_dir_path, self.uuid)

  def backup_metadata(self):
    if self.metadata_path and os.path.exists(self.metadata_path):
      with open(self.metadata_path, 'r') as fp:
        self._metadata_backup = fp.read()

  def backup_requests(self):
    self._requests_backup = {}
    self.iter_request_snapshots(self._handle_backup_requests)

  def copy(self, destination):
    self.copy_metadata(destination)
    self.copy_requests(destination)

  def copy_metadata(self, dest_dir: str):
    return self.copy_file(self.metadata_path, dest_dir)

  def copy_requests(self, dest_dir: str):
    raise NotImplementedError

  def iter_request_snapshots(self, handler: Callable[[RequestSnapshot], None]):
    raise NotImplementedError

  def remove(self, handle_remove_request_snapshot=None):
    self.remove_requests(handle_remove_request_snapshot)
    self.remove_metadata()

  def remove_metadata(self):
    raise NotImplementedError

  def remove_requests(self, handle_remove_request_snapshot=None):
    raise NotImplementedError

  def find_resource(self):
    return Scenario.find_by(uuid=self.uuid)

  def write_metadata(self, scenario: Scenario, **options):
    raise NotImplementedError

  def write_requests(self, scenario: Scenario, **options: RequestSnapshotOptions):
    raise NotImplementedError

  def _handle_backup_requests(self, request_snapshot: RequestSnapshot):
    self._requests_backup[request_snapshot.uuid] = request_snapshot.request

  def _handle_copy_requests(self, request_snapshot: RequestSnapshot, dest_dir: str):
    request_snapshot.copy(dest_dir)

  def _handle_remove_requests(self, request_snapshot: RequestSnapshot):
    request_snapshot.remove()

  def _load_metadata_data(self) -> dict:
    raise NotImplementedError


class ScenarioSnapshotV1(ScenarioSnapshot):
  FORMAT = FORMAT_V1

  def __init__(self, uuid: str, data_dir: DataDir = None, name: str = None):
    super().__init__(uuid, data_dir, name=None)

  @property
  def exists(self):
    return os.path.exists(self.requests_path) and os.path.exists(self.metadata_path)

  @property
  def metadata_path(self):
    if self._resolved_metadata_path and os.path.exists(self._resolved_metadata_path):
      return self._resolved_metadata_path
    self._resolved_metadata_path = os.path.join(self._scenarios_dir_path, self.uuid)
    return self._resolved_metadata_path

  def copy_requests(self, dest_dir: str):
    if not os.path.exists(dest_dir):
      os.makedirs(dest_dir, exist_ok=True)

    requests_file_path = self.requests_path
    if os.path.exists(requests_file_path):
      self.iter_request_snapshots(lambda snapshot: self._handle_copy_requests(snapshot, dest_dir))
      self.copy_file(requests_file_path, dest_dir)

  def iter_request_snapshots(self, handler: Callable[[RequestSnapshot], None]):
    requests_file_path = self.requests_path
    if not os.path.exists(requests_file_path):
      return

    with open(requests_file_path, 'r') as fp:
      self._requests_backup = {}
      uuids = fp.read().split(REQUEST_DELIMITTER)
      uuids = list(filter(lambda uuid: len(uuid) == 36, uuids))

      for uuid in uuids:
        handler(RequestSnapshotV1(uuid, self.data_dir))

  def remove_metadata(self):
    metadata_file_path = self.metadata_path
    if metadata_file_path and os.path.exists(metadata_file_path):
      os.remove(metadata_file_path)

  def remove_requests(self, handle_remove_request_snapshot=None):
    requests_file_path = self.requests_path
    if os.path.exists(requests_file_path):
      self.iter_request_snapshots(handle_remove_request_snapshot or self._handle_remove_requests)
      os.remove(requests_file_path)

  def write_metadata(self, scenario: Scenario, **options):
    self._name = scenario.name
    self._resolved_metadata_path = None
    with open(self.metadata_path, 'w') as fp:
      fp.write(json.dumps({
        'description': scenario.description,
        'name': scenario.name,
      }))

  def write_requests(self, scenario: Scenario, **options: RequestSnapshotOptions):
    with open(self.requests_path, 'w') as fp:
      uuids = []
      for request in scenario.requests:
        request_snapshot = RequestSnapshotV1(request.uuid, self.data_dir)
        request_snapshot.write(request, **options)
        uuids.append(request.uuid)
      fp.write(REQUEST_DELIMITTER.join(uuids))

  def _load_metadata_data(self) -> dict:
    if not self.metadata_path or not os.path.exists(self.metadata_path):
      return {}

    with open(self.metadata_path, 'rb') as fp:
      raw = fp.read()

    try:
      return json.loads(raw)
    except Exception:
      return {'name': self.uuid}


class ScenarioSnapshotV2(ScenarioSnapshot):
  FORMAT = FORMAT_V2

  def __init__(self, uuid: str, data_dir: DataDir = None, name: str = None):
    super().__init__(uuid, data_dir, name=name)

  @staticmethod
  def sanitize_scenario_filename(name: str) -> str:
    """Filesystem-safe scenario YAML basename (without extension)."""
    name = (name or '').strip() or 'scenario'
    name = SAFE_NAME_RE.sub('-', name).strip(' .-_')
    return name or 'scenario'

  @staticmethod
  def unique_yaml_path(path: str) -> str:
    """Return path, or path with -2, -3, ... before the extension if it exists."""
    if not os.path.exists(path):
      return path
    base, ext = os.path.splitext(path)
    i = 2
    while True:
      candidate = f"{base}-{i}{ext}"
      if not os.path.exists(candidate):
        return candidate
      i += 1

  @classmethod
  def allocate_yaml_path(
    cls,
    scenarios_dir: str,
    name: str,
    uuid: str = None,
  ) -> str:
    """
    Choose a unique scenarios/*.yaml path for name.

    Reuses an existing file whose YAML uuid matches; otherwise sanitizes name and
    appends -2, -3, ... on collision (same as migrate).
    """
    if uuid and UUID_RE.match(str(uuid)) and os.path.isdir(scenarios_dir):
      for entry in os.listdir(scenarios_dir):
        if not (entry.endswith('.yaml') or entry.endswith('.yml')):
          continue
        path = os.path.join(scenarios_dir, entry)
        if not os.path.isfile(path):
          continue
        if cls._uuid_from_v2_yaml(path) == str(uuid):
          return path

    base = cls.sanitize_scenario_filename(name)
    path = os.path.join(scenarios_dir, f"{base}.yaml")
    if not os.path.exists(path):
      return path

    if uuid and UUID_RE.match(str(uuid)) and cls._uuid_from_v2_yaml(path) == str(uuid):
      return path

    return cls.unique_yaml_path(path)

  @classmethod
  def history_locator_for(
    cls,
    uuid: str,
    name: str,
    data_dir: DataDir = None,
  ) -> str:
    """
    v2 history locator: {stem}/{uuid}.

    Stem is the on-disk yaml basename when present, else the newly allocated
    stem for name. UUID is always appended so collapse/DELETE can key on
    resource_id == uuid (same pattern as request slug/uuid locators).
    """
    if not uuid or not UUID_RE.match(str(uuid)):
      raise ValueError(f"scenario history locator requires a uuid, got {uuid!r}")

    data_dir = data_dir or DataDir.instance()
    snap = cls(uuid or '', data_dir, name=name)
    found = snap._find_v2_metadata_path()
    if found:
      stem = snap._name_from_path(found)
    else:
      path = cls.allocate_yaml_path(
        data_dir.snapshots_scenarios_dir_path,
        name or uuid or 'scenario',
        uuid=uuid,
      )
      stem = snap._name_from_path(path)
    return f"{stem}/{uuid}"

  @property
  def exists(self):
    return bool(self.metadata_path) and os.path.exists(self.metadata_path)

  @property
  def metadata_path(self):
    if self._resolved_metadata_path and os.path.exists(self._resolved_metadata_path):
      return self._resolved_metadata_path

    found = self._find_v2_metadata_path()
    if found:
      self._resolved_metadata_path = found
      return found

    # New file: reuse uuid match when present, else {name}.yaml (unique on orphan collision)
    self._resolved_metadata_path = self.allocate_yaml_path(
      self._scenarios_dir_path,
      self._name or self.uuid,
      uuid=self._resolved_uuid,
    )
    return self._resolved_metadata_path

  def copy_requests(self, dest_dir: str):
    if not os.path.exists(dest_dir):
      os.makedirs(dest_dir, exist_ok=True)
    self.iter_request_snapshots(lambda snapshot: self._handle_copy_requests(snapshot, dest_dir))

  def iter_request_snapshots(self, handler: Callable[[RequestSnapshot], None]):
    meta = self._load_metadata_data()
    requests_field = meta.get('requests') or {}

    for request_uuid, entry in self.iter_request_entries(requests_field):
      try:
        embedded = RequestSnapshotV2.from_entry(
          entry, self.data_dir, uuid=request_uuid
        )
      except ValueError:
        continue
      # Prefer a standalone uuid.yaml when present (e.g. after snapshot visit)
      standalone = RequestSnapshotV2(embedded.uuid, self.data_dir, slug=embedded.slug)
      if standalone.path and os.path.exists(standalone.path):
        handler(standalone)
      else:
        handler(embedded)

    # Legacy v2: list of relative path strings slug/<uuid>.yaml
    if isinstance(requests_field, list):
      for item in requests_field:
        if not isinstance(item, str):
          continue
        parsed = RequestSnapshotV2.parse_request_relative_path(item)
        if not parsed:
          continue
        slug, uuid = parsed
        handler(RequestSnapshotV2(uuid, self.data_dir, slug=slug))

  def remove_metadata(self):
    metadata_file_path = self.metadata_path
    if metadata_file_path and os.path.exists(metadata_file_path):
      os.remove(metadata_file_path)
    # Embed-only request.remove() leaves bodies/headers alone while this YAML
    # still exists. After it is gone, drop slug dirs no other scenario uses.
    self._cleanup_pending_slug_dirs()

  def remove_requests(self, handle_remove_request_snapshot=None):
    handler = handle_remove_request_snapshot or self._handle_remove_requests
    pending = set()

    def wrap(request_snapshot: RequestSnapshot):
      slug_dir = getattr(request_snapshot, 'slug_dir', None)
      if slug_dir:
        pending.add(slug_dir)
      handler(request_snapshot)

    self.iter_request_snapshots(wrap)
    self._pending_slug_dirs = pending

  def _cleanup_pending_slug_dirs(self):
    pending = getattr(self, '_pending_slug_dirs', None) or set()
    self._pending_slug_dirs = set()
    if not pending:
      return
    cleaner = RequestSnapshotV2('', self.data_dir)
    for slug_dir in pending:
      cleaner._cleanup_empty_slug_dir(slug_dir)

  def write_metadata(self, scenario: Scenario, **options):
    self._name = scenario.name
    if scenario.uuid and UUID_RE.match(str(scenario.uuid)):
      self._resolved_uuid = str(scenario.uuid)
    self._resolved_metadata_path = None

    existing_path = self._find_uuid_metadata_path()
    existing_requests = {}
    if existing_path and os.path.exists(existing_path):
      self._resolved_metadata_path = existing_path
      existing_requests = (self._load_metadata_data() or {}).get('requests') or {}
      self._resolved_metadata_path = None

    dest_path = self._destination_metadata_path(scenario.name, existing_path)
    os.makedirs(self._scenarios_dir_path, exist_ok=True)
    with open(dest_path, 'w') as fp:
      dump_snapshot_yaml({
        'uuid': scenario.uuid,
        'description': scenario.description or '',
        'requests': existing_requests,
      }, fp)

    self._resolved_metadata_path = dest_path
    self._remove_uuid_orphans(dest_path)

  def write_requests(self, scenario: Scenario, **options: RequestSnapshotOptions):
    entries = {}
    for request in scenario.requests:
      slug = RequestSnapshotV2.build_request_slug(request.method, request.path)
      request_snapshot = RequestSnapshotV2(request.uuid, self.data_dir, slug=slug)
      entries[request.uuid] = request_snapshot.build_entry(request, **options)

    self._name = scenario.name
    if scenario.uuid and UUID_RE.match(str(scenario.uuid)):
      self._resolved_uuid = str(scenario.uuid)
    self._resolved_metadata_path = None

    existing_path = self._find_uuid_metadata_path()
    dest_path = self._destination_metadata_path(scenario.name, existing_path)
    os.makedirs(self._scenarios_dir_path, exist_ok=True)
    with open(dest_path, 'w') as fp:
      dump_snapshot_yaml({
        'uuid': scenario.uuid,
        'description': scenario.description or '',
        'requests': entries,
      }, fp)

    self._resolved_metadata_path = dest_path
    self._remove_uuid_orphans(dest_path)

  def update_request_entries(self, entries: Dict[str, dict]):
    """
    Merge updated request embeds into the scenario YAML and write.

    Only updates the current uuid-keyed `requests` map. No-op when the
    metadata file is missing or `requests` is not a dict.
    """
    path = self.metadata_path
    if not path or not os.path.exists(path) or not entries:
      return

    with open(path, 'r') as fp:
      data = yaml.safe_load(fp) or {}
    if not isinstance(data, dict):
      return

    requests_field = data.get('requests')
    if not isinstance(requests_field, dict):
      return

    for request_uuid, entry in entries.items():
      if not isinstance(entry, dict):
        continue
      requests_field[str(request_uuid)] = entry

    with open(path, 'w') as fp:
      dump_snapshot_yaml(data, fp)

  def _find_uuid_metadata_path(self) -> Optional[str]:
    """Locate scenarios/*.yaml whose embedded uuid matches, ignoring name/stem."""
    if not os.path.isdir(self._scenarios_dir_path):
      return None

    resolved_uuid = self._resolved_uuid
    if not resolved_uuid or not UUID_RE.match(str(resolved_uuid)):
      return None

    for name in os.listdir(self._scenarios_dir_path):
      if not (name.endswith('.yaml') or name.endswith('.yml')):
        continue
      path = os.path.join(self._scenarios_dir_path, name)
      if not os.path.isfile(path):
        continue
      if self._uuid_from_v2_yaml(path) == str(resolved_uuid):
        return path
    return None

  @staticmethod
  def _is_collision_stem(stem: str, base: str) -> bool:
    """True if stem is base-2, base-3, ... from unique_yaml_path."""
    prefix = f'{base}-'
    if not stem.startswith(prefix):
      return False
    suffix = stem[len(prefix):]
    return suffix.isdigit() and int(suffix) >= 2

  def _destination_metadata_path(self, name: str, existing_path: Optional[str] = None) -> str:
    """
    Path to write for the current scenario name.

    Keeps the existing file when its stem already matches the sanitized name
    or a collision suffix (name-2, name-3, ...) so write_metadata + write_requests
    do not re-allocate past an already-disambiguated path. Otherwise allocates a
    new {name}.yaml (with -2, -3, ... on collision) so a rename relocates instead
    of writing in place under the old stem.
    """
    desired_stem = self.sanitize_scenario_filename(name or self.uuid or 'scenario')
    if existing_path:
      existing_stem = self._name_from_path(existing_path)
      if existing_stem == desired_stem or self._is_collision_stem(existing_stem, desired_stem):
        return existing_path

    # Do not pass uuid: allocate_yaml_path would reuse the old-stem file.
    return self.allocate_yaml_path(
      self._scenarios_dir_path,
      name or self.uuid or 'scenario',
      uuid=None,
    )

  def _remove_uuid_orphans(self, keep_path: str):
    """Remove other scenarios/*.yaml copies left after a rename write."""
    if not self._resolved_uuid or not UUID_RE.match(str(self._resolved_uuid)):
      return
    if not os.path.isdir(self._scenarios_dir_path):
      return

    keep = os.path.abspath(keep_path)
    for name in os.listdir(self._scenarios_dir_path):
      if not (name.endswith('.yaml') or name.endswith('.yml')):
        continue
      path = os.path.join(self._scenarios_dir_path, name)
      if not os.path.isfile(path):
        continue
      if os.path.abspath(path) == keep:
        continue
      if self._uuid_from_v2_yaml(path) != str(self._resolved_uuid):
        continue
      try:
        os.remove(path)
      except OSError:
        continue

  def _find_v2_metadata_path(self) -> Optional[str]:
    if not os.path.isdir(self._scenarios_dir_path):
      return None

    # Prefer exact name/stem path when set (after rename, avoids pinning old stem
    # via uuid). Fall through to uuid scan for history name/uuid and bare uuid.
    resolved_uuid = self._resolved_uuid
    if self._name:
      candidate = self._safe_scenario_yaml_path(self._scenarios_dir_path, self._name)
      if candidate and os.path.isfile(candidate):
        if not resolved_uuid or not UUID_RE.match(str(resolved_uuid)):
          return candidate
        if self._uuid_from_v2_yaml(candidate) == str(resolved_uuid):
          return candidate

    found = self._find_uuid_metadata_path()
    if found:
      return found

    return None

  def _name_from_path(self, path: str) -> str:
    basename = os.path.basename(path)
    for ext in ('.yaml', '.yml'):
      if basename.endswith(ext):
        return basename[:-len(ext)]
    return basename

  def _load_metadata_data(self) -> dict:
    if not self.metadata_path or not os.path.exists(self.metadata_path):
      return {}

    with open(self.metadata_path, 'rb') as fp:
      raw = fp.read()

    try:
      data = yaml.safe_load(raw) or {}
      if not isinstance(data, dict):
        raise ValueError('invalid yaml')
      found_uuid = data.get('uuid')
      # v2 YAML must include uuid for history/apply identity
      if not found_uuid or not UUID_RE.match(str(found_uuid)):
        raise ValueError('missing uuid')
      return {
        'name': data.get('name') or self._name_from_path(self.metadata_path),
        'description': data.get('description') or '',
        'uuid': str(found_uuid),
        'requests': data.get('requests') or {},
      }
    except Exception:
      # Treat corrupt/invalid YAML as missing so apply can skip
      return {}
