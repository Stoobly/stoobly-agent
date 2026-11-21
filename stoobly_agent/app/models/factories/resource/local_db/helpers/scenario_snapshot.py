import json
import os
import re
from typing import Callable, List, Optional

import yaml

from stoobly_agent.config.data_dir import DataDir
from stoobly_agent.lib.orm.scenario import Scenario

from .request_snapshot import RequestSnapshot, RequestSnapshotV1, RequestSnapshotV2, RequestSnapshotOptions
from .snapshot import Snapshot
from .snapshot_format import FORMAT_V1, FORMAT_V2, UUID_RE, resolve_write_format

REQUEST_DELIMITTER = "\n"
SAFE_NAME_RE = re.compile(r'[^A-Za-z0-9._-]+')


class ScenarioSnapshot(Snapshot):
  """Base scenario snapshot. Prefer create(), from_path(), or V1/V2 subclasses."""

  FORMAT = None

  def __init__(self, uuid: str, data_dir: DataDir = None, name: str = None):
    parsed_uuid, parsed_name = self._parse_scenario_ref(uuid, name)
    # Snapshot requires a uuid string; hydrate from YAML in create() when name-only
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
    - name-only (v2)
    - name/<uuid> (legacy v2)
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

    if uuid and not name and not UUID_RE.match(uuid):
      # v2 name-only locator
      return None, uuid

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
  def _detect_scenario_format(uuid: str, data_dir: DataDir, name: str = None) -> int:
    scenarios_dir = data_dir.snapshots_scenarios_dir_path

    if name:
      candidate = os.path.join(
        scenarios_dir, f"{ScenarioSnapshotV2.sanitize_scenario_filename(name)}.yaml"
      )
      if os.path.isfile(candidate):
        return FORMAT_V2

    if uuid:
      index_path = os.path.join(scenarios_dir, '.uuid-index', uuid)
      if os.path.isfile(index_path):
        return FORMAT_V2

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
      snapshot = cls.create(name, data_dir=data_dir)
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
    name = SAFE_NAME_RE.sub('-', name).strip('-._')
    return name or 'scenario'

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

    name = self._name or self.uuid
    filename = f"{self.sanitize_scenario_filename(name)}.yaml"
    self._resolved_metadata_path = os.path.join(self._scenarios_dir_path, filename)
    return self._resolved_metadata_path

  def copy_requests(self, dest_dir: str):
    if not os.path.exists(dest_dir):
      os.makedirs(dest_dir, exist_ok=True)
    self.iter_request_snapshots(lambda snapshot: self._handle_copy_requests(snapshot, dest_dir))

  def iter_request_snapshots(self, handler: Callable[[RequestSnapshot], None]):
    meta = self._load_metadata_data()
    for relative in meta.get('requests') or []:
      parsed = RequestSnapshotV2.parse_request_relative_path(relative)
      if not parsed:
        continue
      slug, uuid = parsed
      handler(RequestSnapshotV2(uuid, self.data_dir, slug=slug))

  def remove_metadata(self):
    metadata_file_path = self.metadata_path
    if metadata_file_path and os.path.exists(metadata_file_path):
      os.remove(metadata_file_path)
    self._remove_uuid_index()

  def remove_requests(self, handle_remove_request_snapshot=None):
    self.iter_request_snapshots(handle_remove_request_snapshot or self._handle_remove_requests)

  def write_metadata(self, scenario: Scenario, **options):
    self._name = scenario.name
    self._resolved_metadata_path = None

    existing_requests = []
    if self.metadata_path and os.path.exists(self.metadata_path):
      existing_requests = (self._load_metadata_data() or {}).get('requests') or []

    os.makedirs(self._scenarios_dir_path, exist_ok=True)
    with open(self.metadata_path, 'w') as fp:
      yaml.safe_dump({
        'uuid': scenario.uuid,
        'description': scenario.description or '',
        'requests': existing_requests,
      }, fp, sort_keys=False, default_flow_style=False)

  def write_requests(self, scenario: Scenario, **options: RequestSnapshotOptions):
    relative_paths = []
    for request in scenario.requests:
      slug = RequestSnapshotV2.build_request_slug(request.method, request.path)
      request_snapshot = RequestSnapshotV2(request.uuid, self.data_dir, slug=slug)
      request_snapshot.write(request, **options)
      relative_paths.append(RequestSnapshotV2.request_relative_path(slug, request.uuid))

    self._name = scenario.name
    self._resolved_metadata_path = None
    os.makedirs(self._scenarios_dir_path, exist_ok=True)
    with open(self.metadata_path, 'w') as fp:
      yaml.safe_dump({
        'uuid': scenario.uuid,
        'description': scenario.description or '',
        'requests': relative_paths,
      }, fp, sort_keys=False, default_flow_style=False)

  def _uuid_index_path(self) -> str:
    return os.path.join(self._scenarios_dir_path, '.uuid-index', self.uuid)

  def _remove_uuid_index(self):
    path = self._uuid_index_path()
    if os.path.exists(path):
      os.remove(path)

  def _find_v2_metadata_path(self) -> Optional[str]:
    if not os.path.isdir(self._scenarios_dir_path):
      return None

    if self._name:
      candidate = os.path.join(
        self._scenarios_dir_path,
        f"{self.sanitize_scenario_filename(self._name)}.yaml",
      )
      if os.path.isfile(candidate):
        return candidate

    index_path = self._uuid_index_path()
    if os.path.isfile(index_path):
      with open(index_path, 'r') as fp:
        basename = fp.read().strip()
      if basename:
        candidate = os.path.join(self._scenarios_dir_path, basename)
        if os.path.isfile(candidate):
          return candidate

    for name in os.listdir(self._scenarios_dir_path):
      if not (name.endswith('.yaml') or name.endswith('.yml')):
        continue
      path = os.path.join(self._scenarios_dir_path, name)
      if not os.path.isfile(path):
        continue
      try:
        with open(path, 'r') as fp:
          data = yaml.safe_load(fp) or {}
        if isinstance(data, dict) and data.get('uuid') == self.uuid:
          return path
      except Exception:
        continue
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
      # Without a uuid in YAML, name-only history cannot recover identity
      if not found_uuid or not UUID_RE.match(str(found_uuid)):
        raise ValueError('missing uuid')
      return {
        'name': data.get('name') or self._name_from_path(self.metadata_path),
        'description': data.get('description') or '',
        'uuid': str(found_uuid),
        'requests': data.get('requests') or [],
      }
    except Exception:
      # Treat corrupt/invalid YAML as missing so apply can skip
      return {}
