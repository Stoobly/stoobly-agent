import json
import os
import pdb

from stoobly_agent.app.models.adapters.orm import JoinedRequestStringAdapter
from stoobly_agent.lib.orm.scenario import Scenario

from .snapshot import Snapshot

SCENARIO_DELIMITTER = '🐵🐵🐵'.encode()

class ScenarioSnapshot(Snapshot):
  def __init__(self, uuid: str):
    super().__init__(uuid)

    self.__scenarios_dir_path = self.data_dir.snapshots_scenarios_dir_path
    self.__requests_dir_path = self.data_dir.snapshots_scenario_requests_dir_path
    self.__metadata_backup = None
    self.__requests_backup = None

  @property
  def metadata(self):
    if not os.path.exists(self.metadata_path):
      return

    with open(self.metadata_path, 'rb') as fp:
      try:
        return json.loads(fp.read())
      except Exception:
        return {}

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

    with open(requests_file_path, 'rb') as fp:
      return fp.read().split(SCENARIO_DELIMITTER)

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
    requests_file_path = self.requests_path

    if os.path.exists(requests_file_path):
      with open(requests_file_path, 'rb') as fp:
        self.__requests_backup = fp.read()

  def remove_metadata(self):
    metadata_file_path = self.metadata_path

    if os.path.exists(metadata_file_path):
      os.remove(metadata_file_path)

  def remove_requests(self):
    requests_file_path = self.requests_path

    if os.path.exists(requests_file_path):
      os.remove(requests_file_path)

  def write_metadata(self, scenario: Scenario):
    with open(self.metadata_path, 'w') as fp:
      text = json.dumps({
        'description': scenario.description,
        'name': scenario.name,
      })
      fp.write(text)

  def write_requests(self, scenario: Scenario):
    with open(self.requests_path, 'wb') as fp:
      raw_requests = []
      requests = scenario.requests

      for request in requests:
        text = JoinedRequestStringAdapter(request).adapt()
        raw_requests.append(text)
      
      fp.write(SCENARIO_DELIMITTER.join(raw_requests))

