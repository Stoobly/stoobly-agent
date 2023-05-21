import os

from typing import List

from stoobly_agent.config.data_dir import DataDir

from .log_event import LogEvent, Resource

class Log():

  DELIMITTER = "\n"

  def __init__(self, log_file_path = None):
    if not log_file_path:
      base_path = DataDir.instance().snapshots_dir_path

      log_file_path = os.path.join(base_path, 'log')
   
    self.__log_file_path = log_file_path

  def append(self, event: str):
    with open(self.__log_file_path, 'a') as fp:
      fp.write(event + self.DELIMITTER)

  def delete(self, resource: Resource):
    serialized_event = LogEvent.serialize_delete(resource)
    self.append(serialized_event)

  def put(self, resource: Resource):
    serialized_event = LogEvent.serialize_put(resource)
    self.append(serialized_event)

  def read(self):
    if not os.path.exists(self.__log_file_path):
      return ''

    with open(self.__log_file_path, 'r') as fp:
      return fp.read()

  @property
  def events(self):
    events = self.raw_events
    events_count = len(events)

    if events_count == 0:
      return [] 

    return list(map(lambda raw_event: LogEvent(raw_event), self.raw_events))

  @property
  def raw_events(self):
    contents = self.read()
    if not contents:
      return []
    return contents.strip().split(self.DELIMITTER)

  @property
  def unprocessed_events(self):
    version = self.version

    events = self.raw_events
    events_count = len(events)

    if events_count == 0:
      return []

    # Find last processed event
    unprocessed_events: List[LogEvent] = []

    j = events_count - 1
    while j >= 0:
      try:
        event = LogEvent(events[j])
      except Exception:
        continue

      if event.uuid == version:
        break
      
      unprocessed_events.append(event)
      j -= 1

    events_set = {}

    # More recent events take precedence over earlier ones, keep only the most recent event 
    for event in unprocessed_events:
      event_key = event.key

      if event_key in events_set:
        continue
      
      events_set[event_key] = event

    unprocessed_events = list(events_set.values())
    unprocessed_events.reverse()

    return unprocessed_events

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