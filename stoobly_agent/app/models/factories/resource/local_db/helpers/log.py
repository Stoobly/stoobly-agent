import os
import pdb
import time

from typing import List

from stoobly_agent.config.data_dir import DataDir
from stoobly_agent.lib.logger import bcolors, Logger

from .log_event import LogEvent
from .snapshot_types import DELETE_ACTION, PUT_ACTION, Resource

EVENT_DELIMITTER = "\n"
LOG_ID = 'Log'

class Log():

  def __init__(self, data_dir: DataDir = None):
    data_dir = data_dir or DataDir.instance()
    
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

    return list(map(lambda raw_event: LogEvent(raw_event), events))

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
    return self.collapse(events)

  @property
  def raw_events(self):
    contents = self.read()
    return self.build_raw_events(contents) 

  @property
  def unprocessed_events(self) -> List[LogEvent]:
    events = self.events

    events_count = len(events)
    if events_count == 0:
      return []

    version = self.version.strip()
    version_uuids = []
    if version:
      version_uuids = version.split(EVENT_DELIMITTER)

    return self.remove_processed_events(events, version_uuids)

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

  def build_log_events(self, raw_events) -> List[LogEvent]:
    return list(map(lambda raw_event: LogEvent(raw_event), raw_events))

  def next_version(self, last_processed_uuid: str = None):
    uuids = self.uuids()

    if not last_processed_uuid:
      return self.generate_version(uuids)

    for i, uuid in enumerate(uuids):
      if uuid == last_processed_uuid:
        return self.generate_version(uuids[0:i + 1])

    return self.generate_version(uuids)

  def collapse(self, events: List[LogEvent]) -> List[LogEvent]:
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

  def prune(self, dry_run = False):
    # event uuid => history path
    events: List[LogEvent] = []
    path_index = {}

    history_files = self.history_files
    for file_path in history_files:
      with open(file_path, 'r') as fp:
        contents = fp.read().strip()
        raw_events = self.build_raw_events(contents)
        history_events = self.build_log_events(raw_events)

        for event in history_events:
          path_index[event.uuid] = file_path

        events += history_events
    
    # resource_uuid => event
    resource_index = {}
    for event in events:
      if event.resource_uuid not in resource_index:
        resource_index[event.resource_uuid] = []

      resource_index[event.resource_uuid].append(event)

    pruned_events = self.collapse(events)
    for event in pruned_events:
      snapshot = event.snapshot()
      snapshot_exists = snapshot.exists

      if event.action == DELETE_ACTION or not snapshot_exists:
        Logger.instance(LOG_ID).info(f"{bcolors.OKBLUE}Removing{bcolors.ENDC} {event.resource} {event.resource_uuid}")

        resource_events: List[LogEvent] = resource_index[event.resource_uuid]
        removed_events = {}

        for event in resource_events:
          history_path = path_index[event.uuid]
          if event.uuid in removed_events:
            continue

          Logger.instance(LOG_ID).info(f"Removing event {event.uuid}")
          self.remove_event_history(event, history_path, dry_run)
          removed_events[event.uuid] = True

        if event.action == DELETE_ACTION and snapshot_exists: 
          if not dry_run:
            snapshot.remove()
          Logger.instance(LOG_ID).info(f"Removing {event.resource} snapshot")

  def build_raw_events(self, contents: str) -> List[str]:
    if not contents:
      return []
    events = contents.strip().split(EVENT_DELIMITTER)
    return list(filter(lambda e: not not e, events))
      
  def read(self):
    history_files = self.history_files 

    log = []
    for file_path in history_files:
      with open(file_path, 'r') as fp:
        log.append(fp.read().strip())

    return EVENT_DELIMITTER.join(log)
  
  def remove_dangling_events(self, processed_events: List[LogEvent], unprocessed_events: List[LogEvent]):
    '''
    Remove DELETE events where the last processed event was a PUT
    '''
    index = {}
    for event in processed_events:
      if event.action == PUT_ACTION:
        index[event.resource_uuid] = event
      elif event.action == DELETE_ACTION:
        if event.resource_uuid in index:
          del index[event.resource_uuid]
    
    return list(
      filter(
        lambda e: e.action != DELETE_ACTION or (e.action == DELETE_ACTION and e.resource_uuid in index), 
        unprocessed_events
      )
    )

  def remove_event_history(self, event: LogEvent, history_path: str, dry_run = False):
    events = []
    raw_events = []

    with open(history_path, 'r') as fp:
      contents = fp.read().strip()
      raw_events = self.build_raw_events(contents)
      events = self.build_log_events(raw_events)
      events = list(filter(lambda log_event: log_event.uuid != event.uuid, events))

    if len(events) == 0:
      Logger.instance(LOG_ID).info(f"Removing {history_path}")

      if not dry_run:
        os.remove(history_path)
    else:
      new_raw_events = list(map(lambda event: str(event), events))
      Logger.instance(LOG_ID).info(f"Updating {history_path}, Events: {len(raw_events)} -> {len(new_raw_events)}")

      if not dry_run:
        with open(history_path, 'w') as fp:
          fp.write(EVENT_DELIMITTER.join(new_raw_events))

  def remove_processed_events(self, events, version_uuids):
    i = self.__diverge_point(events, version_uuids)
    processed_events = self.collapse(events[0:i])
    unprocessed_events = self.collapse(events[i:])
    remaining_version_uuids = version_uuids[i:]

    remaining_events = self.remove_dangling_events(processed_events, unprocessed_events)
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

  def __diverge_point(self, events: List[LogEvent], version_uuids: List[str]):
    iterations = min(len(events), len(version_uuids))
    for i in range(0, iterations):
      event = events[i] 

      if event.uuid != version_uuids[i]:
        return i
    return iterations

  def __history_file_path(self, bucket_interval: int):
    file_name = f"{int(time.time() / bucket_interval) * bucket_interval}"
    return os.path.join(self.history_dir_path, file_name)