import time
import uuid
from typing import Callable, Optional, Tuple, TypedDict, Type

from stoobly_agent.config.data_dir import DataDir
from stoobly_agent.lib.orm.request import Request
from stoobly_agent.lib.orm.scenario import Scenario

from .request_slug import REQUEST_FILE_EXTENSION, build_request_slug, sanitize_scenario_filename
from .request_snapshot import RequestSnapshot
from .scenario_snapshot import ScenarioSnapshot
from .snapshot_format import FORMAT_V1, FORMAT_V2, UUID_RE, resolve_write_format
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


def _parse_scenario_resource_ref(ref: str) -> Tuple[Optional[str], str]:
  """
  Parse scenario history field into (name, identity).

  v2 uses name-only (unique). Legacy accepts `name/<uuid>`.
  v1 uses bare uuid. Identity for collapse is name when present, else uuid.
  """
  if not ref:
    return None, ref

  if '/' in ref:
    name, rest = ref.rsplit('/', 1)
    if rest.endswith('.yaml') or rest.endswith('.yml'):
      rest = rest.rsplit('.', 1)[0]
    # Name is the stable unique key; uuid kept only for legacy path resolve
    return name or None, name or rest

  if UUID_RE.match(ref):
    return None, ref

  return ref, ref


def _resolve_event_class(format: int = None, data_dir: DataDir = None) -> Type['LogEvent']:
  if format is None:
    format = resolve_write_format(data_dir or DataDir.instance())
  return LogEventV2 if format == FORMAT_V2 else LogEventV1


class LogEvent():
  """Base history event. Prefer LogEvent.create() or LogEventV1/V2 for writes."""

  FORMAT = None

  def __init__(self, event: str):
    toks = event.strip().split(COLUMN_DELIMITTER)

    self.uuid = toks[0]
    self.resource = toks[1]
    # Raw history field: bare uuid (v1), slug/<uuid> (v2 request), or name (v2 scenario)
    self.resource_uuid = toks[2]
    self.action = toks[3]
    self.created_at = int(toks[4]) if len(toks) > 4 else None # milliseconds

    if self.resource == SCENARIO_RESOURCE:
      self.__resource_slug, self.__resource_id = _parse_scenario_resource_ref(self.resource_uuid)
    else:
      self.__resource_slug, self.__resource_id = parse_resource_ref(self.resource_uuid)

  @classmethod
  def create(cls, event: str) -> 'LogEvent':
    """Parse a history line into LogEventV1 or LogEventV2 from locator shape."""
    toks = event.strip().split(COLUMN_DELIMITTER)
    resource = toks[1] if len(toks) > 1 else ''
    resource_uuid = toks[2] if len(toks) > 2 else ''
    if '/' in resource_uuid:
      return LogEventV2(event)
    # v2 scenarios use a unique name-only locator (not a UUID)
    if resource == SCENARIO_RESOURCE and resource_uuid and not UUID_RE.match(resource_uuid):
      return LogEventV2(event)
    return LogEventV1(event)

  @classmethod
  def from_resource(
    cls,
    resource: Resource,
    action: Action,
    data_dir: DataDir = None,
    format: int = None,
  ):
    if cls is LogEvent:
      return _resolve_event_class(format, data_dir).from_resource(
        resource, action, data_dir=data_dir
      )
    return cls(cls.serialize_resource(resource, action, data_dir=data_dir))

  @staticmethod
  def serialize(resource_name: Resource, resource_uuid: str, action: Action):
    return f"{str(uuid.uuid1())} {resource_name} {resource_uuid} {action} {int(time.time() * 1000)}"

  @classmethod
  def serialize_delete(
    cls,
    resource: Resource,
    data_dir: DataDir = None,
    format: int = None,
  ):
    if cls is LogEvent:
      return _resolve_event_class(format, data_dir).serialize_delete(
        resource, data_dir=data_dir
      )
    return cls.serialize_resource(resource, DELETE_ACTION, data_dir=data_dir)

  @classmethod
  def serialize_put(
    cls,
    resource: Resource,
    data_dir: DataDir = None,
    format: int = None,
  ):
    if cls is LogEvent:
      return _resolve_event_class(format, data_dir).serialize_put(
        resource, data_dir=data_dir
      )
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

  @classmethod
  def request_locator(cls, request: Request, data_dir: DataDir = None) -> str:
    raise NotImplementedError

  @classmethod
  def scenario_locator(cls, scenario: Scenario, data_dir: DataDir = None) -> str:
    raise NotImplementedError

  @property
  def format(self) -> Optional[int]:
    return self.FORMAT

  @property
  def resource_id(self) -> str:
    """Stable identity for collapse/apply (request UUID; scenario name or UUID)."""
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
        # Pass locator (name or uuid) so apply can resolve ORM identity
        return kwargs['handle_scenario_delete'](self.resource_uuid)
      elif self.action == PUT_ACTION:
        # Pass history locator (name) so snapshot resolve stays O(1)
        return kwargs['handle_scenario_put'](self.resource_uuid)

  def duplicate(self):
    event_str = str(self)
    toks = event_str.split(COLUMN_DELIMITTER)
    toks[0] = str(uuid.uuid1())
    toks[4] = str(int(time.time() * 1000))
    return self.__class__(COLUMN_DELIMITTER.join(toks))

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
      return RequestSnapshot.create(self.resource_id, data_dir, slug=self.resource_slug)
    elif self.is_scenario():
      # resource_uuid is name (v2), name/uuid (legacy v2), or bare uuid (v1)
      return ScenarioSnapshot.create(self.resource_uuid, data_dir)

  def to_dict(self):
    return {
      'action': self.action,
      'created_at': self.created_at,
      'resource': self.resource,
      'resource_uuid': self.resource_uuid,
      'uuid': self.uuid,
    }


class LogEventV1(LogEvent):
  """History events with bare-UUID resource locators."""

  FORMAT = FORMAT_V1

  @classmethod
  def request_locator(cls, request: Request, data_dir: DataDir = None) -> str:
    return request.uuid

  @classmethod
  def scenario_locator(cls, scenario: Scenario, data_dir: DataDir = None) -> str:
    return scenario.uuid


class LogEventV2(LogEvent):
  """History events with v2 locators (request: slug/<uuid>; scenario: unique name)."""

  FORMAT = FORMAT_V2

  @classmethod
  def request_locator(cls, request: Request, data_dir: DataDir = None) -> str:
    slug = build_request_slug(request.method, request.path)
    return f"{slug}/{request.uuid}"

  @classmethod
  def scenario_locator(cls, scenario: Scenario, data_dir: DataDir = None) -> str:
    return sanitize_scenario_filename(scenario.name)
