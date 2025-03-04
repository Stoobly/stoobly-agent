import json
import os
import pdb
import shutil

from typing import Callable

from stoobly_agent.lib.orm.scenario import Scenario

from .snapshot import Snapshot
from .request_snapshot import RequestSnapshot, RequestSnapshotOptions

REQUEST_DELIMITTER = "\n"

class ScenarioSnapshot(Snapshot):
  def __init__(self, uuid: str):
    super().__init__(uuid)

    self.__scenarios_dir_path = self.data_dir.snapshots_scenarios_dir_path
    self.__requests_dir_path = self.data_dir.snapshots_scenario_requests_dir_path
    self.__metadata_backup = None
    self.__requests_backup = None

  @property
  def exists(self):
    return os.path.exists(self.requests_path) and os.path.exists(self.metadata_path)

  @property
  def metadata(self):
    if not os.path.exists(self.metadata_path):
      return {}

    with open(self.metadata_path, 'rb') as fp:
      try:
        return json.loads(fp.read())
      except Exception:
        return {
          'name': self.uuid
        }

  @property
  def metadata_backup(self):
    return self.__metadata_backup

  @property
  def metadata_path(self):
    return os.path.join(self.__scenarios_dir_path, self.uuid)

  @property
  def requests(self):
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
    return os.path.join(self.__requests_dir_path, self.uuid)

  def backup_metadata(self):
    if os.path.exists(self.metadata_path):
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

    requests_file_path = self.requests_path

    if os.path.exists(requests_file_path):
      # A request only ever belongs to one scenario
      self.iter_request_snapshots(lambda snapshot: self.__handle_copy_requests(snapshot, dest_dir))

      self.copy_file(requests_file_path, dest_dir)

  def iter_request_snapshots(self, handler: Callable[[RequestSnapshot], None]):
    requests_file_path = self.requests_path

    if os.path.exists(requests_file_path):
      with open(requests_file_path, 'r') as fp:
        self.__requests_backup = {}

        uuids = fp.read().split(REQUEST_DELIMITTER)
        uuids = list(filter(lambda uuid: len(uuid) == 36, uuids))

        for uuid in uuids:
          request_snapshot = RequestSnapshot(uuid)
          handler(request_snapshot)

  def remove(self):
    self.remove_metadata()
    self.remove_requests()

  def remove_metadata(self):
    metadata_file_path = self.metadata_path

    if os.path.exists(metadata_file_path):
      os.remove(metadata_file_path)

  def remove_requests(self):
    requests_file_path = self.requests_path

    if os.path.exists(requests_file_path):
      # A request only every belongs to one scenario
      self.iter_request_snapshots(self.__handle_remove_requests)

      os.remove(requests_file_path)

  def find_resource(self):
    return Scenario.find_by(uuid=self.uuid)

  def write_metadata(self, scenario: Scenario):
    with open(self.metadata_path, 'w') as fp:
      text = json.dumps({
        'description': scenario.description,
        'name': scenario.name,
      })
      fp.write(text)

  def write_requests(self, scenario: Scenario, **options: RequestSnapshotOptions):
    with open(self.requests_path, 'w') as fp:
      uuids = []
      requests = scenario.requests

      for request in requests:
        uuid = request.uuid

        request_snapshot = RequestSnapshot(uuid)
        request_snapshot.write(request, **options)

        uuids.append(uuid)
      
      fp.write(REQUEST_DELIMITTER.join(uuids))

  def __handle_backup_requests(self, request_snapshot: RequestSnapshot):
    self.__requests_backup[request_snapshot.uuid] = request_snapshot.request

  def __handle_copy_requests(self, request_snapshot: RequestSnapshot, dest_dir: str):
    request_snapshot.copy(dest_dir)

  def __handle_remove_requests(self, request_snapshot: RequestSnapshot):
    request_snapshot.remove()