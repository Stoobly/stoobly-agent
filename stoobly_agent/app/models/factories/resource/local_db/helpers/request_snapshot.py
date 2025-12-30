import os

from stoobly_agent.app.models.adapters.orm import JoinedRequestStringAdapter
from stoobly_agent.lib.logger import Logger
from stoobly_agent.lib.orm.request import Request

from .snapshot import Snapshot
from .snapshot_types import RequestSnapshotOptions

LOG_ID = 'RequestSnapshot'

class RequestSnapshot(Snapshot):

  def __init__(self, uuid: str):
    super().__init__(uuid)
    
    self.__requests_dir_path = self.data_dir.snapshots_requests_dir_path
  
    self.__backup = None

  @property
  def backup(self):
    return self.__backup

  @property
  def exists(self):
    return os.path.exists(self.path)

  @property
  def request(self):
    request_file_path = self.path

    if not os.path.exists(request_file_path):
      return

    with open(request_file_path, 'rb') as fp:
      return fp.read()

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
    dir_path = os.path.join(self.__requests_dir_path, self.uuid[0:2])

    if not os.path.exists(dir_path):
      os.mkdir(dir_path)

    return os.path.join(dir_path, self.uuid)

  def backup(self):
    if os.path.exists(self.path):
      with open(self.path, 'rb') as fp:
        self.__backup = fp.read()

  def copy(self, dest_dir: str):
    request_file_path = self.path
    return self.copy_file(request_file_path, dest_dir)

  def find_resource(self):
    return Request.find_by(uuid=self.uuid)

  def remove(self):
    request_file_path = self.path

    if os.path.exists(request_file_path):
      os.remove(request_file_path)

  def rollback(self):
    with open(self.path, 'wb') as fp:
      fp.write(self.__backup)

  def write(self, request: Request, **options: RequestSnapshotOptions):
    adapter = JoinedRequestStringAdapter(request)

    if options.get('decode'):
      try:
        adapter.decode_response()
      except Exception as e:
        Logger.instance(LOG_ID).warning(f"Failed to decode response for request {self.uuid}: {e}. Writing snapshot without decoding.")
        # Continue without decoding - graceful degradation

    text = adapter.adapt()
    self.write_raw(text)

  def write_raw(self, text):
    with open(self.path, 'wb') as fp:
      fp.write(text)
