import json
import os
from typing import Callable, List, Optional

import yaml

from stoobly_agent.config.data_dir import DataDir
from stoobly_agent.lib.orm.scenario import Scenario

from .request_slug import (
  build_request_slug,
  parse_request_relative_path,
  request_relative_path,
  sanitize_scenario_filename,
)
from .request_snapshot import RequestSnapshot, RequestSnapshotOptions
from .snapshot import Snapshot
from .snapshot_format import FORMAT_V1, FORMAT_V2, resolve_write_format

REQUEST_DELIMITTER = "\n"

class ScenarioSnapshot(Snapshot):
  def __init__(
    self,
    uuid: str,
    data_dir: DataDir = None,
    name: str = None,
    format: int = None,
  ):
    # Allow history-style refs: <name>/<uuid>
    parsed_name = name
    parsed_uuid = uuid
    if uuid and '/' in uuid:
      parsed_name, rest = uuid.rsplit('/', 1)
      if rest.endswith('.yaml') or rest.endswith('.yml'):
        rest = rest.rsplit('.', 1)[0]
      parsed_uuid = rest
      parsed_name = name or parsed_name

    super().__init__(parsed_uuid, data_dir)

    self.__scenarios_dir_path = self.data_dir.snapshots_scenarios_dir_path
    self.__requests_dir_path = self.data_dir.snapshots_scenario_requests_dir_path
    self.__name = parsed_name
    self.__format = format
    self.__metadata_backup = None
    self.__requests_backup = None
    self.__resolved_metadata_path = None

  @property
  def exists(self):
    if self.format == FORMAT_V2:
      return bool(self.metadata_path) and os.path.exists(self.metadata_path)
    return os.path.exists(self.requests_path) and os.path.exists(self.metadata_path)

  @property
  def format(self) -> int:
    if self.__format is not None:
      return self.__format

    v2_path = self.__find_v2_metadata_path()
    if v2_path:
      self.__format = FORMAT_V2
      self.__resolved_metadata_path = v2_path
      return self.__format

    v1_meta = os.path.join(self.__scenarios_dir_path, self.uuid)
    if os.path.exists(v1_meta):
      self.__format = FORMAT_V1
      self.__resolved_metadata_path = v1_meta
      return self.__format

    self.__format = resolve_write_format(self.data_dir)
    return self.__format

  @property
  def metadata(self):
    """Return apply-compatible metadata: name + description only."""
    data = self.__load_metadata_data()
    if not data:
      return {}
    return {
      'name': data.get('name') or self.uuid,
      'description': data.get('description') or '',
    }

  @property
  def metadata_backup(self):
    return self.__metadata_backup

  @property
  def metadata_path(self):
    if self.__resolved_metadata_path and os.path.exists(self.__resolved_metadata_path):
      return self.__resolved_metadata_path

    if self.format == FORMAT_V2:
      found = self.__find_v2_metadata_path()
      if found:
        self.__resolved_metadata_path = found
        return found

      name = self.__name or self.uuid
      filename = f"{sanitize_scenario_filename(name)}.yaml"
      self.__resolved_metadata_path = os.path.join(self.__scenarios_dir_path, filename)
      return self.__resolved_metadata_path

    self.__resolved_metadata_path = os.path.join(self.__scenarios_dir_path, self.uuid)
    return self.__resolved_metadata_path

  @property
  def request_snapshots(self) -> List[RequestSnapshot]:
    snapshots = []
    handler = lambda request_snapshot: snapshots.append(request_snapshot)
    self.iter_request_snapshots(handler)
    return snapshots

  @property
  def requests(self):
    if self.format == FORMAT_V2:
      if not self.metadata_path or not os.path.exists(self.metadata_path):
        return

      raw_requests = []
      handler = lambda request_snapshot: raw_requests.append(request_snapshot.request)
      self.iter_request_snapshots(handler)
      return raw_requests

    requests_file_path = self.requests_path

    if not os.path.exists(requests_file_path):
      return

    raw_requests = []
    handler = lambda request_snapshot: raw_requests.append(request_snapshot.request)
    self.iter_request_snapshots(handler)

    return raw_requests

  @property
  def requests_backup(self):
    return self.__requests_backup

  @property
  def requests_path(self):
    """v1 request-index path. Unused for v2 (requests live in YAML)."""
    return os.path.join(self.__requests_dir_path, self.uuid)

  def backup_metadata(self):
    if self.metadata_path and os.path.exists(self.metadata_path):
      with open(self.metadata_path, 'r') as fp:
        self.__metadata_backup = fp.read()

  def backup_requests(self):
    self.__requests_backup = {}

    self.iter_request_snapshots(self.__handle_backup_requests)

  def copy(self, destination):
    self.copy_metadata(destination)
    self.copy_requests(destination)

  def copy_metadata(self, dest_dir: str):
    metadata_file_path = self.metadata_path
    return self.copy_file(metadata_file_path, dest_dir)

  def copy_requests(self, dest_dir: str):
    if not os.path.exists(dest_dir):
      os.makedirs(dest_dir, exist_ok=True)

    if self.format == FORMAT_V2:
      self.iter_request_snapshots(lambda snapshot: self.__handle_copy_requests(snapshot, dest_dir))
      return

    requests_file_path = self.requests_path

    if os.path.exists(requests_file_path):
      # A request only ever belongs to one scenario
      self.iter_request_snapshots(lambda snapshot: self.__handle_copy_requests(snapshot, dest_dir))

      self.copy_file(requests_file_path, dest_dir)

  def iter_request_snapshots(self, handler: Callable[[RequestSnapshot], None]):
    if self.format == FORMAT_V2:
      meta = self.__load_metadata_data()
      for relative in meta.get('requests') or []:
        parsed = parse_request_relative_path(relative)
        if not parsed:
          continue
        slug, uuid = parsed
        request_snapshot = RequestSnapshot(uuid, self.data_dir, slug=slug, format=FORMAT_V2)
        handler(request_snapshot)
      return

    requests_file_path = self.requests_path

    if os.path.exists(requests_file_path):
      with open(requests_file_path, 'r') as fp:
        self.__requests_backup = {}

        uuids = fp.read().split(REQUEST_DELIMITTER)
        uuids = list(filter(lambda uuid: len(uuid) == 36, uuids))

        for uuid in uuids:
          request_snapshot = RequestSnapshot(uuid, self.data_dir, format=FORMAT_V1)
          handler(request_snapshot)

  def remove(self, handle_remove_request_snapshot=None):
    # Requests must be removed before metadata in v2 (request list lives in YAML)
    self.remove_requests(handle_remove_request_snapshot)
    self.remove_metadata()

  def remove_metadata(self):
    metadata_file_path = self.metadata_path

    if metadata_file_path and os.path.exists(metadata_file_path):
      os.remove(metadata_file_path)

    if self.format == FORMAT_V2:
      self.__remove_uuid_index()

  def remove_requests(self, handle_remove_request_snapshot=None):
    if self.format == FORMAT_V2:
      self.iter_request_snapshots(handle_remove_request_snapshot or self.__handle_remove_requests)
      return

    requests_file_path = self.requests_path

    if os.path.exists(requests_file_path):
      # A request only every belongs to one scenario
      self.iter_request_snapshots(handle_remove_request_snapshot or self.__handle_remove_requests)

      os.remove(requests_file_path)

  def find_resource(self):
    return Scenario.find_by(uuid=self.uuid)

  def write_metadata(self, scenario: Scenario, **options):
    write_format = options.get('format')
    if write_format is None:
      write_format = self.__format if self.__format is not None else resolve_write_format(self.data_dir)
    self.__format = write_format
    self.__name = scenario.name
    self.__resolved_metadata_path = None

    if write_format == FORMAT_V2:
      # requests list is written in write_requests; keep existing if file present
      existing_requests = []
      if self.metadata_path and os.path.exists(self.metadata_path):
        existing_requests = (self.__load_metadata_data() or {}).get('requests') or []

      os.makedirs(self.__scenarios_dir_path, exist_ok=True)
      with open(self.metadata_path, 'w') as fp:
        yaml.safe_dump({
          'uuid': scenario.uuid,
          'description': scenario.description or '',
          'requests': existing_requests,
        }, fp, sort_keys=False, default_flow_style=False)
      return

    with open(self.metadata_path, 'w') as fp:
      text = json.dumps({
        'description': scenario.description,
        'name': scenario.name,
      })
      fp.write(text)

  def write_requests(self, scenario: Scenario, **options: RequestSnapshotOptions):
    write_format = options.get('format')
    if write_format is None:
      write_format = self.__format if self.__format is not None else resolve_write_format(self.data_dir)
    self.__format = write_format

    if write_format == FORMAT_V2:
      relative_paths = []
      requests = scenario.requests

      for request in requests:
        slug = build_request_slug(request.method, request.path)
        request_snapshot = RequestSnapshot(
          request.uuid,
          self.data_dir,
          slug=slug,
          format=FORMAT_V2,
        )
        request_snapshot.write(request, **{**options, 'format': FORMAT_V2})
        relative_paths.append(request_relative_path(slug, request.uuid))

      # Rewrite YAML with ordered request paths
      self.__name = scenario.name
      self.__resolved_metadata_path = None
      os.makedirs(self.__scenarios_dir_path, exist_ok=True)
      with open(self.metadata_path, 'w') as fp:
        yaml.safe_dump({
          'uuid': scenario.uuid,
          'description': scenario.description or '',
          'requests': relative_paths,
        }, fp, sort_keys=False, default_flow_style=False)
      return

    with open(self.requests_path, 'w') as fp:
      uuids = []
      requests = scenario.requests

      for request in requests:
        uuid = request.uuid

        request_snapshot = RequestSnapshot(uuid, self.data_dir, format=FORMAT_V1)
        request_snapshot.write(request, **{**options, 'format': FORMAT_V1})

        uuids.append(uuid)

      fp.write(REQUEST_DELIMITTER.join(uuids))

  def __handle_backup_requests(self, request_snapshot: RequestSnapshot):
    self.__requests_backup[request_snapshot.uuid] = request_snapshot.request

  def __handle_copy_requests(self, request_snapshot: RequestSnapshot, dest_dir: str):
    request_snapshot.copy(dest_dir)

  def __handle_remove_requests(self, request_snapshot: RequestSnapshot):
    request_snapshot.remove()

  def __uuid_index_dir(self) -> str:
    return os.path.join(self.__scenarios_dir_path, '.uuid-index')

  def __uuid_index_path(self) -> str:
    return os.path.join(self.__uuid_index_dir(), self.uuid)

  def __remove_uuid_index(self):
    # Clean legacy uuid-index entries if present
    path = self.__uuid_index_path()
    if os.path.exists(path):
      os.remove(path)

  def __find_v2_metadata_path(self) -> Optional[str]:
    if not os.path.isdir(self.__scenarios_dir_path):
      return None

    # Prefer name from history locator / constructor
    if self.__name:
      candidate = os.path.join(
        self.__scenarios_dir_path,
        f"{sanitize_scenario_filename(self.__name)}.yaml",
      )
      if os.path.isfile(candidate):
        return candidate

    # Legacy O(1) lookup via uuid index (older v2 trees)
    index_path = self.__uuid_index_path()
    if os.path.isfile(index_path):
      with open(index_path, 'r') as fp:
        basename = fp.read().strip()
      if basename:
        candidate = os.path.join(self.__scenarios_dir_path, basename)
        if os.path.isfile(candidate):
          return candidate

    for name in os.listdir(self.__scenarios_dir_path):
      if not (name.endswith('.yaml') or name.endswith('.yml')):
        continue
      path = os.path.join(self.__scenarios_dir_path, name)
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

  def __name_from_path(self, path: str) -> str:
    basename = os.path.basename(path)
    for ext in ('.yaml', '.yml'):
      if basename.endswith(ext):
        return basename[:-len(ext)]
    return basename

  def __load_metadata_data(self) -> dict:
    if not self.metadata_path or not os.path.exists(self.metadata_path):
      return {}

    with open(self.metadata_path, 'rb') as fp:
      raw = fp.read()

    if self.format == FORMAT_V2:
      try:
        data = yaml.safe_load(raw) or {}
        if not isinstance(data, dict):
          raise ValueError('invalid yaml')
        return {
          'name': data.get('name') or self.__name_from_path(self.metadata_path),
          'description': data.get('description') or '',
          'uuid': data.get('uuid') or self.uuid,
          'requests': data.get('requests') or [],
        }
      except Exception:
        # Match v1 corrupt-metadata fallback: use uuid as name
        return {
          'name': self.uuid,
          'description': '',
          'uuid': self.uuid,
          'requests': [],
        }

    try:
      return json.loads(raw)
    except Exception:
      return {
        'name': self.uuid
      }
