import glob
import os
import shutil
from typing import Optional

from stoobly_agent.app.models.adapters.orm import JoinedRequestStringAdapter
from stoobly_agent.config.constants.custom_headers import BODY_REF
from stoobly_agent.config.data_dir import DataDir
from stoobly_agent.lib.logger import Logger
from stoobly_agent.lib.orm.request import Request

from .body_ref import externalize_joined_request, reconstitute_joined_request
from .request_slug import REQUEST_FILE_EXTENSION, build_request_slug, request_relative_path
from .snapshot import Snapshot
from .snapshot_format import FORMAT_V1, FORMAT_V2, resolve_write_format
from .snapshot_types import RequestSnapshotOptions

LOG_ID = 'RequestSnapshot'


def _parse_request_ref(uuid: str, slug: str = None):
  """Parse history-style refs: slug/<uuid> or slug/<uuid>.http."""
  parsed_slug = slug
  parsed_uuid = uuid
  if uuid and '/' in uuid:
    parsed_slug, rest = uuid.rsplit('/', 1)
    if rest.endswith(REQUEST_FILE_EXTENSION):
      rest = rest[:-len(REQUEST_FILE_EXTENSION)]
    parsed_uuid = rest
    parsed_slug = parsed_slug or slug
  return parsed_uuid, parsed_slug


def _detect_request_format(uuid: str, data_dir: DataDir, slug: str = None) -> int:
  requests_dir = data_dir.snapshots_requests_dir_path

  if slug:
    candidate = os.path.join(requests_dir, slug, f"{uuid}{REQUEST_FILE_EXTENSION}")
    if os.path.exists(candidate):
      return FORMAT_V2

  index_path = os.path.join(requests_dir, '.uuid-index', uuid)
  if os.path.isfile(index_path):
    return FORMAT_V2

  pattern = os.path.join(requests_dir, '*', f"{uuid}{REQUEST_FILE_EXTENSION}")
  if glob.glob(pattern):
    return FORMAT_V2

  v1_path = os.path.join(requests_dir, uuid[0:2], uuid)
  if os.path.exists(v1_path):
    return FORMAT_V1

  return resolve_write_format(data_dir)


class RequestSnapshot(Snapshot):
  """Base request snapshot. Prefer RequestSnapshot.create() or V1/V2 subclasses."""

  FORMAT = None

  def __init__(self, uuid: str, data_dir: DataDir = None, slug: str = None):
    parsed_uuid, parsed_slug = _parse_request_ref(uuid, slug)
    super().__init__(parsed_uuid, data_dir)

    self._requests_dir_path = self.data_dir.snapshots_requests_dir_path
    self._slug = parsed_slug
    self._backup = None
    self._resolved_path = None

  @classmethod
  def create(
    cls,
    uuid: str,
    data_dir: DataDir = None,
    slug: str = None,
    format: int = None,
  ) -> 'RequestSnapshot':
    data_dir = data_dir or DataDir.instance()
    parsed_uuid, parsed_slug = _parse_request_ref(uuid, slug)

    if format is None:
      if parsed_slug:
        format = FORMAT_V2
      else:
        format = _detect_request_format(parsed_uuid, data_dir, parsed_slug)

    if format == FORMAT_V2:
      return RequestSnapshotV2(parsed_uuid, data_dir, slug=parsed_slug)
    return RequestSnapshotV1(parsed_uuid, data_dir)

  @property
  def format(self) -> int:
    return self.FORMAT

  @property
  def backup(self):
    return self._backup

  @property
  def exists(self):
    path = self.path
    return bool(path) and os.path.exists(path)

  @property
  def slug(self) -> Optional[str]:
    return self._slug

  @property
  def relative_path(self) -> Optional[str]:
    return None

  @property
  def request(self):
    raise NotImplementedError

  @property
  def path(self):
    raise NotImplementedError

  @property
  def mitmproxy_request(self):
    from stoobly_agent.app.models.adapters.python.request.mitmproxy_adapter import MitmproxyRequestAdapter
    return MitmproxyRequestAdapter(self.python_request).adapt()

  @property
  def mitmproxy_response(self):
    from stoobly_agent.app.models.adapters.python.response.mitmproxy_adapter import MitmproxyResponseAdapter
    return MitmproxyResponseAdapter(self.python_response).adapt()

  @property
  def python_request(self):
    from stoobly_agent.app.models.adapters.raw_joined.request.python_adapter import PythonRequestAdapter
    return PythonRequestAdapter(self.request).adapt()

  @property
  def python_response(self):
    from stoobly_agent.app.models.adapters.raw_joined.response.python_adapter import PythonResponseAdapter
    return PythonResponseAdapter(self.request).adapt()

  def backup(self):
    path = self.path
    if path and os.path.exists(path):
      with open(path, 'rb') as fp:
        self._backup = fp.read()

  def copy(self, dest_dir: str):
    return self.copy_file(self.path, dest_dir)

  def find_resource(self):
    return Request.find_by(uuid=self.uuid)

  def remove(self):
    raise NotImplementedError

  def rollback(self):
    path = self.path
    if path is None:
      return
    with open(path, 'wb') as fp:
      fp.write(self._backup)

  def write(self, request: Request, **options: RequestSnapshotOptions):
    adapter = JoinedRequestStringAdapter(request)

    if options.get('decode'):
      try:
        adapter.decode_response()
      except Exception as e:
        Logger.instance(LOG_ID).warning(
          f"Failed to decode response for request {self.uuid}: {e}. Writing snapshot without decoding."
        )

    self.write_raw(adapter.adapt())

  def write_raw(self, text):
    raise NotImplementedError

  def _ensure_parent(self, path: str):
    parent = os.path.dirname(path)
    if parent and not os.path.exists(parent):
      os.makedirs(parent, exist_ok=True)


class RequestSnapshotV1(RequestSnapshot):
  FORMAT = FORMAT_V1

  def __init__(self, uuid: str, data_dir: DataDir = None, slug: str = None):
    super().__init__(uuid, data_dir, slug=None)

  @property
  def request(self):
    request_file_path = self.path
    if not request_file_path or not os.path.exists(request_file_path):
      return

    with open(request_file_path, 'rb') as fp:
      return fp.read()

  @property
  def path(self):
    if self._resolved_path and os.path.exists(self._resolved_path):
      return self._resolved_path

    self._resolved_path = self._v1_path(create_dir=True)
    return self._resolved_path

  def remove(self):
    request_file_path = self.path
    if request_file_path and os.path.exists(request_file_path):
      os.remove(request_file_path)

  def write_raw(self, text):
    path = self.path
    if path is None:
      raise ValueError(f"Cannot write request snapshot {self.uuid}: missing path")

    self._ensure_parent(path)
    with open(path, 'wb') as fp:
      fp.write(text)

  def _v1_path(self, create_dir: bool = True):
    dir_path = os.path.join(self._requests_dir_path, self.uuid[0:2])

    if create_dir and not os.path.exists(dir_path):
      os.mkdir(dir_path)

    return os.path.join(dir_path, self.uuid)


class RequestSnapshotV2(RequestSnapshot):
  FORMAT = FORMAT_V2

  def __init__(self, uuid: str, data_dir: DataDir = None, slug: str = None):
    super().__init__(uuid, data_dir, slug=slug)

  @property
  def slug(self) -> Optional[str]:
    if self._slug:
      return self._slug
    path = self._find_v2_path()
    if path:
      self._slug = os.path.basename(os.path.dirname(path))
    return self._slug

  @property
  def relative_path(self) -> Optional[str]:
    slug = self.slug
    if not slug:
      return None
    return request_relative_path(slug, self.uuid)

  @property
  def request(self):
    request_file_path = self.path
    if not request_file_path or not os.path.exists(request_file_path):
      return

    with open(request_file_path, 'rb') as fp:
      raw = fp.read()

    slug_dir = os.path.dirname(request_file_path)
    return reconstitute_joined_request(raw, slug_dir)

  @property
  def path(self):
    if self._resolved_path and os.path.exists(self._resolved_path):
      return self._resolved_path

    v2_path = self._find_v2_path()
    if v2_path:
      self._resolved_path = v2_path
      return v2_path

    slug = self._slug
    if not slug:
      return None

    # Do not mkdir here — path is also used for exists/remove checks
    self._resolved_path = os.path.join(
      self._requests_dir_path, slug, f"{self.uuid}{REQUEST_FILE_EXTENSION}"
    )
    return self._resolved_path

  def copy(self, dest_dir: str):
    request_file_path = self.path
    copied = self.copy_file(request_file_path, dest_dir)
    if request_file_path:
      self._copy_bodies(request_file_path, dest_dir)
    return copied

  def remove(self):
    request_file_path = self.path
    if request_file_path and os.path.exists(request_file_path):
      os.remove(request_file_path)
      self._remove_uuid_index()
      self._cleanup_empty_slug_dir(os.path.dirname(request_file_path))

  def write(self, request: Request, **options: RequestSnapshotOptions):
    self._slug = build_request_slug(request.method, request.path)
    self._resolved_path = None
    super().write(request, **options)

  def write_raw(self, text):
    path = self.path
    if path is None:
      raise ValueError(f"Cannot write request snapshot {self.uuid}: missing path/slug")

    self._ensure_parent(path)
    payload = externalize_joined_request(text, os.path.dirname(path))
    with open(path, 'wb') as fp:
      fp.write(payload)

  def _uuid_index_path(self) -> str:
    return os.path.join(self._requests_dir_path, '.uuid-index', self.uuid)

  def _remove_uuid_index(self):
    path = self._uuid_index_path()
    if os.path.exists(path):
      os.remove(path)

  def _find_v2_path(self) -> Optional[str]:
    if self._slug:
      candidate = os.path.join(
        self._requests_dir_path, self._slug, f"{self.uuid}{REQUEST_FILE_EXTENSION}"
      )
      if os.path.exists(candidate):
        return candidate

    index_path = self._uuid_index_path()
    if os.path.isfile(index_path):
      with open(index_path, 'r') as fp:
        relative = fp.read().strip().replace('\\', '/')
      if relative:
        candidate = os.path.join(self._requests_dir_path, *relative.split('/'))
        if os.path.isfile(candidate):
          self._slug = self._slug or relative.split('/', 1)[0]
          return candidate

    pattern = os.path.join(self._requests_dir_path, '*', f"{self.uuid}{REQUEST_FILE_EXTENSION}")
    matches = glob.glob(pattern)
    if matches:
      return matches[0]
    return None

  def _copy_bodies(self, request_file_path: str, dest_dir: str):
    slug_dir = os.path.dirname(request_file_path)
    bodies_dir = os.path.join(slug_dir, 'bodies')
    if not os.path.isdir(bodies_dir):
      return

    try:
      with open(request_file_path, 'rb') as fp:
        raw = fp.read()
    except OSError:
      return

    raw_text = raw.decode('utf-8', errors='ignore')
    for line in raw_text.splitlines():
      if line.lower().startswith(f'{BODY_REF.lower()}:'):
        ref = line.split(':', 1)[1].strip()
        src = os.path.join(slug_dir, ref.replace('/', os.sep))
        if os.path.exists(src):
          self.copy_file(src, dest_dir)

  def _cleanup_empty_slug_dir(self, slug_dir: str):
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
