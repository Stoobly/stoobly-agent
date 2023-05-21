import uuid

from typing import Callable, Literal, TypedDict

from stoobly_agent.lib.orm.request import Request
from stoobly_agent.lib.orm.scenario import Scenario

REQUEST_RESOURCE = 'request'
SCENARIO_RESOURCE = 'scenario'

DELETE_ACTION = 'DELETE'
PUT_ACTION = 'PUT'

Action = Literal[f"{DELETE_ACTION}", f"{PUT_ACTION}"]
Resource = Literal[f"{REQUEST_RESOURCE}", f"{SCENARIO_RESOURCE}"]

class EventHandlers(TypedDict):
  handle_request_delete: Callable[[str], None]
  handle_request_put: Callable[[str], None]
  handle_scenario_delete: Callable[[str], None]
  handle_scenario_put: Callable[[str], None]

class LogEvent():
  DELIMITTER = ' '

  def __init__(self, event: str):
    toks = event.strip().split(self.DELIMITTER)

    self.uuid = toks[0]
    self.resource = toks[1]
    self.resource_uuid = toks[2]
    self.action = toks[3]

  @classmethod
  def from_resource(cls, resource: Resource, action: Action):
    return cls(cls.serialize(resource, action))

  @classmethod
  def serialize_delete(cls, resource: Resource):
    return cls.serialize(resource, DELETE_ACTION)

  @classmethod
  def serialize_put(cls, resource: Resource):
    return cls.serialize(resource, PUT_ACTION)

  @staticmethod
  def serialize(resource: Resource, action: Action):
    resource_name = ''

    if isinstance(resource, Request):
      resource_name = REQUEST_RESOURCE
    elif isinstance(resource, Scenario):
      resource_name = SCENARIO_RESOURCE
    else:
      resource_name = resource.__class__.__name__

    return f"{str(uuid.uuid1())} {resource_name} {resource.uuid} {action}"

  @property
  def key(self):
    return f"{self.resource_uuid}.{self.resource}"

  def apply(self, **kwargs: EventHandlers):
    if self.resource == REQUEST_RESOURCE:
      if self.action == DELETE_ACTION:
        kwargs['handle_request_delete'](self.resource_uuid)
      elif self.action == PUT_ACTION:
        kwargs['handle_request_put'](self.resource_uuid)
    elif self.resource == SCENARIO_RESOURCE:
      if self.action == DELETE_ACTION:
        kwargs['handle_scenario_delete'](self.resource_uuid)
      elif self.action == PUT_ACTION:
        kwargs['handle_scenario_put'](self.resource_uuid)