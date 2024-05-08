import pdb
import uuid
import time

from typing import Callable, TypedDict

from stoobly_agent.lib.orm.request import Request
from stoobly_agent.lib.orm.scenario import Scenario

from .request_snapshot import RequestSnapshot
from .scenario_snapshot import ScenarioSnapshot
from .snapshot_types import Action, DELETE_ACTION, PUT_ACTION, REQUEST_RESOURCE, Resource, SCENARIO_RESOURCE

COLUMN_DELIMITTER = ' '

class EventHandlers(TypedDict):
  handle_request_delete: Callable[[str], None]
  handle_request_put: Callable[[str], None]
  handle_scenario_delete: Callable[[str], None]
  handle_scenario_put: Callable[[str], None]

class LogEvent():
  def __init__(self, event: str):
    toks = event.strip().split(COLUMN_DELIMITTER)

    self.uuid = toks[0]
    self.resource = toks[1]
    self.resource_uuid = toks[2]
    self.action = toks[3]
    self.created_at = int(toks[4]) if len(toks) > 4 else None # milliseconds

  @classmethod
  def from_resource(cls, resource: Resource, action: Action):
    return cls(cls.serialize_resource(resource, action))

  @staticmethod
  def serialize(resource_name: Resource, resource_uuid: str, action: Action):
    return f"{str(uuid.uuid1())} {resource_name} {resource_uuid} {action} {int(time.time() * 1000)}"

  @classmethod
  def serialize_delete(cls, resource: Resource):
    return cls.serialize_resource(resource, DELETE_ACTION)

  @classmethod
  def serialize_put(cls, resource: Resource):
    return cls.serialize_resource(resource, PUT_ACTION)

  @classmethod
  def serialize_resource(cls, resource: Resource, action: Action):
    resource_name = ''

    if isinstance(resource, Request):
      resource_name = REQUEST_RESOURCE
    elif isinstance(resource, Scenario):
      resource_name = SCENARIO_RESOURCE
    else:
      resource_name = resource.__class__.__name__

    return cls.serialize(resource_name, resource.uuid, action)

  @property
  def key(self):
    return f"{self.resource_uuid}.{self.resource}"

  def __str__(self):
    return COLUMN_DELIMITTER.join([self.uuid, self.resource, self.resource_uuid, self.action, str(self.created_at)])

  def apply(self, **kwargs: EventHandlers):
    if self.is_request():
      if self.action == DELETE_ACTION:
        return kwargs['handle_request_delete'](self.resource_uuid)
      elif self.action == PUT_ACTION:
        return kwargs['handle_request_put'](self.resource_uuid)
    elif self.is_scenario():
      if self.action == DELETE_ACTION:
        return kwargs['handle_scenario_delete'](self.resource_uuid)
      elif self.action == PUT_ACTION:
        return kwargs['handle_scenario_put'](self.resource_uuid)

  def duplicate(self):
    event_str = str(self) 
    toks = event_str.split(COLUMN_DELIMITTER)
    toks[0] = str(uuid.uuid1())
    toks[4] = str(int(time.time() * 1000))
    return LogEvent(COLUMN_DELIMITTER.join(toks))

  def is_request(self):
    return self.resource == REQUEST_RESOURCE

  def is_scenario(self):
    return self.resource == SCENARIO_RESOURCE

  def snapshot(self):
    if self.is_request():
      return RequestSnapshot(self.resource_uuid)
    elif self.is_scenario():
      return ScenarioSnapshot(self.resource_uuid)

  def to_dict(self):
    return {
      'action': self.action,
      'created_at': self.created_at,
      'resource': self.resource,
      'resource_uuid': self.resource_uuid,
      'uuid': self.uuid,
    }