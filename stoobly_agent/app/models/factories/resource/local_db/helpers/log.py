import os
import pdb
import time

from typing import List

from stoobly_agent.config.data_dir import DataDir

from .log_event import LogEvent, Resource

EVENT_DELIMITTER = "\n"

class Log():

  def __init__(self):
    data_dir = DataDir.instance()
    self.__log_file_path = data_dir.snapshots_log_file_path
    self.__history_dir_path = data_dir.snapshots_history_dir_path

    if not os.listdir(self.history_dir_path):
      self.rotate()

  @property
  def events(self):
    events = self.raw_events
    events_count = len(events)

    if events_count == 0:
      return [] 

    return list(map(lambda raw_event: LogEvent(raw_event), self.raw_events))

  @property
  def history_dir_path(self):
    return self.__history_dir_path

  @property
  def history_files(self):
    files = []

    if not os.path.exists(self.history_dir_path):
      return files

    for file_name in os.listdir(self.history_dir_path):
      full_path = os.path.join(self.history_dir_path, file_name)
      if os.path.isfile(full_path):
        files.append(full_path)

    files.sort()
    return files
    
  @property
  def log_file_path(self):
    return self.__log_file_path

  @property
  def target_events(self):
    events = self.events
    return self.prune(events)

  @property
  def raw_events(self):
    contents = self.read()
    if not contents:
      return []
    events = contents.strip().split(EVENT_DELIMITTER)
    return list(filter(lambda e: not not e, events))

  @property
  def unprocessed_events(self) -> List[LogEvent]:
    events = self.events

    events_count = len(events)
    if events_count == 0:
      return []

    version = self.version.strip()
    if not version:
      return self.prune(events)

    # Find diverge point
    version_uuids = version.split(EVENT_DELIMITTER)
    unprocessed_events: List[LogEvent] = self.remove_processed_events(events, version_uuids)

    return self.prune(unprocessed_events)

  @property
  def version(self):
    version_file_path = DataDir.instance().snapshosts_version_path
    version = ''

    if not os.path.exists(version_file_path):
      return version

    with open(version_file_path, 'r') as fp:
      version = fp.read()

    return version

  @version.setter
  def version(self, v: str):
    version_file_path = DataDir.instance().snapshosts_version_path

    with open(version_file_path, 'w') as fp:
      fp.write(v)

  def append(self, event: str, bucket_interval: int = 300):
    file_path = self.__history_file_path(bucket_interval)

    with open(file_path, 'a') as fp:
      fp.write(event + EVENT_DELIMITTER)

  def delete(self, resource: Resource):
    serialized_event = LogEvent.serialize_delete(resource)
    self.append(serialized_event)

  def generate_version(self, uuids: List[str]):
    return EVENT_DELIMITTER.join(uuids)

  def lock(self, events = ''):
    _events = events or self.read()

    if not _events:
      return

    with open(self.log_file_path, 'w') as fp:
      fp.write(_events + EVENT_DELIMITTER)

  def next_version(self, last_processed_uuid: str = None):
    uuids = self.uuids()

    if not last_processed_uuid:
      return self.generate_version(uuids)

    for i, uuid in enumerate(uuids):
      if uuid == last_processed_uuid:
        return self.generate_version(uuids[0:i + 1])

    return self.generate_version(uuids)

  def prune(self, events: List[LogEvent]) -> List[LogEvent]:
    events_count = {}

    # More recent events take precedence over earlier ones, keep only the most recent event 
    for event in events:
      event_key = event.key

      if event_key not in events_count:
        events_count[event_key] = 0

      events_count[event_key] += 1

    target_events = []
    for event in events: 
      event_key = event.key
      events_count[event_key] -= 1

      if events_count[event_key] == 0:
        target_events.append(event)

    return target_events

  def put(self, resource: Resource):
    serialized_event = LogEvent.serialize_put(resource)
    self.append(serialized_event)

  def read(self):
    history_files = self.history_files 

    log = []
    for file_path in history_files:
      with open(file_path, 'r') as fp:
        log.append(fp.read().strip())

    return EVENT_DELIMITTER.join(log)

  def remove_processed_events(self, events: List[LogEvent], version_uuids: List[str]):
    iterations = min(len(events), len(version_uuids))
    for i in range(0, iterations):
      event = events[i] 

      if event.uuid != version_uuids[i]:
        i -= 1
        break

    remaining_version_uuids = version_uuids[i + 1:]
    remaining_events = events[i + 1:]
    return list(filter(lambda e: e.uuid not in remaining_version_uuids, remaining_events))

  # Rotate log to history
  def rotate(self):
    if not os.path.exists(self.__log_file_path):
      return

    with open(self.__log_file_path, 'r') as fp:
      events = fp.read()
      if events:
        self.append(events.strip())

  def uuids(self, events: List[LogEvent] = None):
    _events = events or self.events
    return list(map(lambda e: e.uuid, _events))

  def __history_file_path(self, bucket_interval: int):
    file_name = f"{int(time.time() / bucket_interval) * bucket_interval}"
    return os.path.join(self.history_dir_path, file_name)