import time
import uuid
from typing import Callable, Optional, Tuple, TypedDict

from stoobly_agent.config.data_dir import DataDir
from stoobly_agent.lib.orm.request import Request
from stoobly_agent.lib.orm.scenario import Scenario

from .request_slug import REQUEST_FILE_EXTENSION, build_request_slug, sanitize_scenario_filename
from .request_snapshot import RequestSnapshot
from .scenario_snapshot import ScenarioSnapshot
from .snapshot_format import FORMAT_V2, resolve_write_format
from .snapshot_types import Action, DELETE_ACTION, PUT_ACTION, REQUEST_RESOURCE, Resource, SCENARIO_RESOURCE

COLUMN_DELIMITTER = ' '

class EventHandlers(TypedDict):
  handle_request_delete: Callable[[str], None]
  handle_request_put: Callable[[str], None]
  handle_scenario_delete: Callable[[str], None]
  handle_scenario_put: Callable[[str], None]

def parse_resource_ref(ref: str) -> Tuple[Optional[str], str]:
  """
  Parse history resource field into (slug, uuid).

  Accepts bare uuid or `slug/<uuid>` / `slug/<uuid>.http`.
  """
  if not ref:
    return None, ref

  if '/' not in ref:
    return None, ref

  slug, rest = ref.rsplit('/', 1)
  if rest.endswith(REQUEST_FILE_EXTENSION):
    rest = rest[:-len(REQUEST_FILE_EXTENSION)]
  return slug or None, rest

class LogEvent():
  def __init__(self, event: str):
    toks = event.strip().split(COLUMN_DELIMITTER)

    self.uuid = toks[0]
    self.resource = toks[1]
    # Raw history field: bare uuid (v1/legacy) or slug/<uuid> (v2 requests)
    self.resource_uuid = toks[2]
    self.action = toks[3]
    self.created_at = int(toks[4]) if len(toks) > 4 else None # milliseconds

    self.__resource_slug, self.__resource_id = parse_resource_ref(self.resource_uuid)

  @classmethod
  def from_resource(cls, resource: Resource, action: Action, data_dir: DataDir = None):
    return cls(cls.serialize_resource(resource, action, data_dir=data_dir))

  @staticmethod
  def serialize(resource_name: Resource, resource_uuid: str, action: Action):
    return f"{str(uuid.uuid1())} {resource_name} {resource_uuid} {action} {int(time.time() * 1000)}"

  @classmethod
  def serialize_delete(cls, resource: Resource, data_dir: DataDir = None):
    return cls.serialize_resource(resource, DELETE_ACTION, data_dir=data_dir)

  @classmethod
  def serialize_put(cls, resource: Resource, data_dir: DataDir = None):
    return cls.serialize_resource(resource, PUT_ACTION, data_dir=data_dir)

  @classmethod
  def serialize_resource(cls, resource: Resource, action: Action, data_dir: DataDir = None):
    resource_name = ''
    locator = getattr(resource, 'uuid', None)

    if isinstance(resource, Request):
      resource_name = REQUEST_RESOURCE
      locator = cls.request_locator(resource, data_dir=data_dir)
    elif isinstance(resource, Scenario):
      resource_name = SCENARIO_RESOURCE
      locator = cls.scenario_locator(resource, data_dir=data_dir)
    else:
      resource_name = resource.__class__.__name__

    return cls.serialize(resource_name, locator, action)

  @staticmethod
  def request_locator(request: Request, data_dir: DataDir = None) -> str:
    """History locator for a request: slug/<uuid> in v2, bare uuid in v1."""
    data_dir = data_dir or DataDir.instance()
    if resolve_write_format(data_dir) != FORMAT_V2:
      return request.uuid

    slug = build_request_slug(request.method, request.path)
    return f"{slug}/{request.uuid}"

  @staticmethod
  def scenario_locator(scenario: Scenario, data_dir: DataDir = None) -> str:
    """History locator for a scenario: <name>/<uuid> in v2, bare uuid in v1."""
    data_dir = data_dir or DataDir.instance()
    if resolve_write_format(data_dir) != FORMAT_V2:
      return scenario.uuid

    name = sanitize_scenario_filename(scenario.name)
    return f"{name}/{scenario.uuid}"

  @property
  def resource_id(self) -> str:
    """Stable UUID identity for collapse/apply/ORM (ignores slug locator)."""
    return self.__resource_id

  @property
  def resource_slug(self) -> Optional[str]:
    return self.__resource_slug

  @property
  def key(self):
    return f"{self.resource_id}.{self.resource}"

  def __str__(self):
    return COLUMN_DELIMITTER.join([self.uuid, self.resource, self.resource_uuid, self.action, str(self.created_at)])

  def apply(self, **kwargs: EventHandlers):
    if self.is_request():
      if self.action == DELETE_ACTION:
        return kwargs['handle_request_delete'](self.resource_id)
      elif self.action == PUT_ACTION:
        # Pass full history locator (slug/<uuid>) so snapshot resolve stays O(1)
        return kwargs['handle_request_put'](self.resource_uuid)
    elif self.is_scenario():
      if self.action == DELETE_ACTION:
        return kwargs['handle_scenario_delete'](self.resource_id)
      elif self.action == PUT_ACTION:
        # Pass full history locator (name/<uuid>) so snapshot resolve stays O(1)
        return kwargs['handle_scenario_put'](self.resource_uuid)

  def duplicate(self):
    event_str = str(self)
    toks = event_str.split(COLUMN_DELIMITTER)
    toks[0] = str(uuid.uuid1())
    toks[4] = str(int(time.time() * 1000))
    return LogEvent(COLUMN_DELIMITTER.join(toks))

  def duplicate_as_delete(self):
    event = self.duplicate()
    event.action = DELETE_ACTION
    return event

  def duplicate_as_put(self):
    event = self.duplicate()
    event.action = PUT_ACTION
    return event

  def is_request(self):
    return self.resource == REQUEST_RESOURCE

  def is_scenario(self):
    return self.resource == SCENARIO_RESOURCE

  def snapshot(self, data_dir: DataDir = None):
    if self.is_request():
      return RequestSnapshot(self.resource_id, data_dir, slug=self.resource_slug)
    elif self.is_scenario():
      return ScenarioSnapshot(self.resource_id, data_dir, name=self.resource_slug)

  def to_dict(self):
    return {
      'action': self.action,
      'created_at': self.created_at,
      'resource': self.resource,
      'resource_uuid': self.resource_uuid,
      'uuid': self.uuid,
    }
