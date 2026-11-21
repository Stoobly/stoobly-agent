import glob
import os
import shutil
from typing import Optional

from stoobly_agent.app.models.adapters.orm import JoinedRequestStringAdapter
from stoobly_agent.config.data_dir import DataDir
from stoobly_agent.lib.logger import Logger
from stoobly_agent.lib.orm.request import Request

from .body_ref import externalize_joined_request, reconstitute_joined_request
from .request_slug import REQUEST_FILE_EXTENSION, build_request_slug, request_relative_path
from .snapshot import Snapshot
from .snapshot_format import FORMAT_V1, FORMAT_V2, resolve_write_format
from .snapshot_types import RequestSnapshotOptions

LOG_ID = 'RequestSnapshot'

class RequestSnapshot(Snapshot):

  def __init__(
    self,
    uuid: str,
    data_dir: DataDir = None,
    slug: str = None,
    format: int = None,
  ):
    # Allow history-style refs: slug/<uuid> or slug/<uuid>.http
    parsed_slug = slug
    parsed_uuid = uuid
    if uuid and '/' in uuid:
      parsed_slug, rest = uuid.rsplit('/', 1)
      if rest.endswith(REQUEST_FILE_EXTENSION):
        rest = rest[:-len(REQUEST_FILE_EXTENSION)]
      parsed_uuid = rest
      parsed_slug = parsed_slug or slug

    super().__init__(parsed_uuid, data_dir)

    self.__requests_dir_path = self.data_dir.snapshots_requests_dir_path
    self.__slug = parsed_slug
    self.__format = format
    self.__backup = None
    self.__resolved_path = None

  @property
  def backup(self):
    return self.__backup

  @property
  def exists(self):
    path = self.path
    return bool(path) and os.path.exists(path)

  @property
  def format(self) -> int:
    if self.__format is not None:
      return self.__format

    # Prefer existing on-disk location for this uuid
    v2_path = self.__find_v2_path()
    if v2_path:
      self.__format = FORMAT_V2
      self.__resolved_path = v2_path
      self.__slug = self.__slug or os.path.basename(os.path.dirname(v2_path))
      return self.__format

    v1_path = self.__v1_path(create_dir=False)
    if os.path.exists(v1_path):
      self.__format = FORMAT_V1
      self.__resolved_path = v1_path
      return self.__format

    # Fall back to write-format policy for new files
    self.__format = resolve_write_format(self.data_dir)
    return self.__format

  @property
  def slug(self) -> Optional[str]:
    if self.__slug:
      return self.__slug
    if self.format == FORMAT_V2:
      path = self.__find_v2_path()
      if path:
        self.__slug = os.path.basename(os.path.dirname(path))
    return self.__slug

  @property
  def relative_path(self) -> Optional[str]:
    if self.format != FORMAT_V2:
      return None
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

    if self.format == FORMAT_V2:
      slug_dir = os.path.dirname(request_file_path)
      return reconstitute_joined_request(raw, slug_dir)

    return raw

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

  @property
  def path(self):
    if self.__resolved_path and os.path.exists(self.__resolved_path):
      return self.__resolved_path

    if self.format == FORMAT_V2:
      v2_path = self.__find_v2_path()
      if v2_path:
        self.__resolved_path = v2_path
        return v2_path

      slug = self.__slug
      if not slug:
        # Cannot build a new v2 path without a slug
        return None

      # Do not mkdir here — path is also used for exists/remove checks
      self.__resolved_path = os.path.join(self.__requests_dir_path, slug, f"{self.uuid}{REQUEST_FILE_EXTENSION}")
      return self.__resolved_path

    self.__resolved_path = self.__v1_path(create_dir=True)
    return self.__resolved_path

  def backup(self):
    path = self.path
    if path and os.path.exists(path):
      with open(path, 'rb') as fp:
        self.__backup = fp.read()

  def copy(self, dest_dir: str):
    request_file_path = self.path
    copied = self.copy_file(request_file_path, dest_dir)
    if self.format == FORMAT_V2 and request_file_path:
      self.__copy_bodies(request_file_path, dest_dir)
    return copied

  def find_resource(self):
    return Request.find_by(uuid=self.uuid)

  def remove(self):
    request_file_path = self.path

    if request_file_path and os.path.exists(request_file_path):
      os.remove(request_file_path)

      if self.format == FORMAT_V2:
        # Clean legacy uuid-index entries if present
        self.__remove_uuid_index()
        self.__cleanup_empty_slug_dir(os.path.dirname(request_file_path))

  def rollback(self):
    path = self.path
    if path is None:
      return
    with open(path, 'wb') as fp:
      fp.write(self.__backup)

  def write(self, request: Request, **options: RequestSnapshotOptions):
    adapter = JoinedRequestStringAdapter(request)

    if options.get('decode'):
      try:
        adapter.decode_response()
      except Exception as e:
        Logger.instance(LOG_ID).warning(
          f"Failed to decode response for request {self.uuid}: {e}. Writing snapshot without decoding."
        )

    text = adapter.adapt()

    write_format = options.get('format')
    if write_format is None:
      write_format = self.__format if self.__format is not None else resolve_write_format(self.data_dir)
    self.__format = write_format

    if write_format == FORMAT_V2:
      self.__slug = build_request_slug(request.method, request.path)
      self.__resolved_path = None

    self.write_raw(text)

  def write_raw(self, text):
    path = self.path
    if path is None:
      raise ValueError(f"Cannot write request snapshot {self.uuid}: missing path/slug")

    parent = os.path.dirname(path)
    if parent and not os.path.exists(parent):
      os.makedirs(parent, exist_ok=True)

    payload = text
    if self.format == FORMAT_V2:
      payload = externalize_joined_request(text, parent)

    with open(path, 'wb') as fp:
      fp.write(payload)

  def __v1_path(self, create_dir: bool = True):
    dir_path = os.path.join(self.__requests_dir_path, self.uuid[0:2])

    if create_dir and not os.path.exists(dir_path):
      os.mkdir(dir_path)

    return os.path.join(dir_path, self.uuid)

  def __uuid_index_path(self) -> str:
    # Legacy index kept for read/delete compatibility with older v2 trees
    return os.path.join(self.__requests_dir_path, '.uuid-index', self.uuid)

  def __remove_uuid_index(self):
    path = self.__uuid_index_path()
    if os.path.exists(path):
      os.remove(path)

  def __find_v2_path(self) -> Optional[str]:
    if self.__slug:
      candidate = os.path.join(self.__requests_dir_path, self.__slug, f"{self.uuid}{REQUEST_FILE_EXTENSION}")
      if os.path.exists(candidate):
        return candidate

    # Legacy O(1) lookup via uuid index (older v2 trees)
    index_path = self.__uuid_index_path()
    if os.path.isfile(index_path):
      with open(index_path, 'r') as fp:
        relative = fp.read().strip().replace('\\', '/')
      if relative:
        candidate = os.path.join(self.__requests_dir_path, *relative.split('/'))
        if os.path.isfile(candidate):
          self.__slug = self.__slug or relative.split('/', 1)[0]
          return candidate

    # Fallback glob for uuid-only history lines / missing index
    pattern = os.path.join(self.__requests_dir_path, '*', f"{self.uuid}{REQUEST_FILE_EXTENSION}")
    matches = glob.glob(pattern)
    if matches:
      return matches[0]
    return None

  def __copy_bodies(self, request_file_path: str, dest_dir: str):
    slug_dir = os.path.dirname(request_file_path)
    bodies_dir = os.path.join(slug_dir, 'bodies')
    if not os.path.isdir(bodies_dir):
      return

    # Copy referenced body files only
    try:
      with open(request_file_path, 'rb') as fp:
        raw = fp.read()
    except OSError:
      return

    raw_text = raw.decode('utf-8', errors='ignore')
    for line in raw_text.splitlines():
      if line.lower().startswith('x-stoobly-body-ref:'):
        ref = line.split(':', 1)[1].strip()
        src = os.path.join(slug_dir, ref.replace('/', os.sep))
        if os.path.exists(src):
          self.copy_file(src, dest_dir)

  def __cleanup_empty_slug_dir(self, slug_dir: str):
    if not os.path.isdir(slug_dir):
      return

    # When no .http files remain, drop bodies/ then the slug dir (same as migrate)
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
