import time
import uuid
from typing import Callable, Optional, Tuple, TypedDict, Type

from stoobly_agent.config.data_dir import DataDir
from stoobly_agent.lib.orm.request import Request
from stoobly_agent.lib.orm.scenario import Scenario

from .request_snapshot import RequestSnapshot, RequestSnapshotV2
from .scenario_snapshot import ScenarioSnapshot, ScenarioSnapshotV2
from .snapshot_format import FORMAT_V1, FORMAT_V2, UUID_RE, resolve_write_format
from .snapshot_types import Action, DELETE_ACTION, PUT_ACTION, REQUEST_RESOURCE, Resource, SCENARIO_RESOURCE

COLUMN_DELIMITTER = ' '
_ACTIONS = {DELETE_ACTION, PUT_ACTION}
_RESOURCES = {REQUEST_RESOURCE, SCENARIO_RESOURCE}

# uuid, resource, resource_uuid, action, created_at
_ParsedFields = Tuple[str, str, str, Action, Optional[int]]

class MalformedLogEventError(ValueError):
  """Raised when a snapshot history line cannot be parsed."""

  def __init__(self, line: str, reason: str):
    self.line = line
    self.reason = reason
    display = line if len(line) <= 200 else f"{line[:200]}..."
    super().__init__(f"Malformed snapshot history line ({reason}): {display}")


class EventHandlers(TypedDict):
  handle_request_delete: Callable[[str], None]
  handle_request_put: Callable[[str], None]
  handle_scenario_delete: Callable[[str], None]
  handle_scenario_put: Callable[[str], None]


class LogEvent():
  """Base history event. Prefer LogEvent.create() or LogEventV1/V2 for writes."""

  FORMAT = None

  def __init__(self, event: str):
    line = event.strip()
    toks = line.split(COLUMN_DELIMITTER)

    if len(toks) < 4:
      raise MalformedLogEventError(
        line,
        f"expected at least 4 space-separated fields, got {len(toks)}",
      )

    (
      self.uuid,
      self.resource,
      self.resource_uuid,
      self.action,
      self.created_at,
    ) = type(self)._parse_fields(toks, line)

    if self.resource == SCENARIO_RESOURCE:
      # Collapse identity prefers UUID (name/uuid or bare uuid); name-only
      # legacy locators fall back to the stem.
      parsed_uuid, parsed_name = ScenarioSnapshot._parse_scenario_ref(self.resource_uuid)
      self.__resource_slug = parsed_name
      if parsed_uuid and UUID_RE.match(str(parsed_uuid)):
        self.__resource_id = str(parsed_uuid)
      else:
        self.__resource_id = parsed_name or parsed_uuid
    else:
      parsed_uuid, parsed_slug = RequestSnapshot._parse_request_ref(self.resource_uuid)
      self.__resource_slug = parsed_slug
      self.__resource_id = parsed_uuid

  @classmethod
  def _parse_fields(cls, toks, line: str) -> _ParsedFields:
    """Default / legacy: `uuid resource locator action [timestamp]`."""
    event_uuid = toks[0]
    resource = toks[1]
    resource_uuid = toks[2]
    action = toks[3]

    if len(toks) > 4:
      try:
        created_at = int(toks[4])
      except ValueError as e:
        raise MalformedLogEventError(
          line,
          f"created_at must be an integer timestamp, got {toks[4]!r}",
        ) from e
    else:
      created_at = None

    return event_uuid, resource, resource_uuid, action, created_at

  @staticmethod
  def _is_v2_field_order(toks) -> bool:
    """True for `uuid timestamp action resource resource_id`."""
    return (
      len(toks) >= 5
      and toks[2] in _ACTIONS
      and toks[3] in _RESOURCES
    )

  @classmethod
  def _resolve_event_class(cls, format: int = None, data_dir: DataDir = None) -> Type['LogEvent']:
    if format is None:
      format = resolve_write_format(data_dir or DataDir.instance())
    return LogEventV2 if format == FORMAT_V2 else LogEventV1

  @classmethod
  def create(cls, event: str) -> 'LogEvent':
    """Parse a history line into LogEventV1 or LogEventV2 from line/locator shape."""
    toks = event.strip().split(COLUMN_DELIMITTER)
    if cls._is_v2_field_order(toks):
      return LogEventV2(event)

    resource = toks[1] if len(toks) > 1 else ''
    resource_uuid = toks[2] if len(toks) > 2 else ''
    if '/' in resource_uuid:
      return LogEventV2(event)
    # Legacy v2 scenarios use a unique name-only locator (not a UUID)
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
      return cls._resolve_event_class(format, data_dir).from_resource(
        resource, action, data_dir=data_dir
      )
    return cls(cls.serialize_resource(resource, action, data_dir=data_dir))

  @classmethod
  def format_line(
    cls,
    event_uuid: str,
    created_at: Optional[int],
    action: Action,
    resource_name: str,
    resource_uuid: str,
  ) -> str:
    """Build a history line in this class's field order (legacy by default)."""
    parts = [event_uuid, resource_name, resource_uuid, action]
    if created_at is not None:
      parts.append(str(created_at))
    return COLUMN_DELIMITTER.join(parts)

  @classmethod
  def serialize(cls, resource_name: Resource, resource_uuid: str, action: Action):
    return cls.format_line(
      str(uuid.uuid1()),
      int(time.time() * 1000),
      action,
      resource_name,
      resource_uuid,
    )

  @classmethod
  def serialize_delete(
    cls,
    resource: Resource,
    data_dir: DataDir = None,
    format: int = None,
  ):
    if cls is LogEvent:
      return cls._resolve_event_class(format, data_dir).serialize_delete(
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
      return cls._resolve_event_class(format, data_dir).serialize_put(
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
    """Stable identity for collapse/apply (request UUID; scenario UUID or legacy name)."""
    return self.__resource_id

  @property
  def resource_slug(self) -> Optional[str]:
    return self.__resource_slug

  @property
  def key(self):
    return f"{self.resource_id}.{self.resource}"

  def __str__(self):
    event_cls = type(self)
    if event_cls.FORMAT is None:
      # Bare LogEvent: preserve legacy order
      event_cls = LogEventV1
    return event_cls.format_line(
      self.uuid,
      self.created_at,
      self.action,
      self.resource,
      self.resource_uuid,
    )

  def apply(self, **kwargs: EventHandlers):
    if self.is_request():
      if self.action == DELETE_ACTION:
        return kwargs['handle_request_delete'](self.resource_id)
      elif self.action == PUT_ACTION:
        # Pass full history locator (slug/<uuid>) so snapshot resolve stays O(1)
        return kwargs['handle_request_put'](self.resource_uuid)
    elif self.is_scenario():
      if self.action == DELETE_ACTION:
        # Pass UUID identity when present (name/uuid); name-only legacy still works
        return kwargs['handle_scenario_delete'](self.resource_id)
      elif self.action == PUT_ACTION:
        # Pass full history locator (name/uuid) so snapshot resolve stays O(1)
        return kwargs['handle_scenario_put'](self.resource_uuid)

  def duplicate(self):
    event_cls = type(self)
    if event_cls.FORMAT is None:
      event_cls = LogEventV1
    line = event_cls.format_line(
      str(uuid.uuid1()),
      int(time.time() * 1000),
      self.action,
      self.resource,
      self.resource_uuid,
    )
    return event_cls(line)

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
      # resource_uuid is name/uuid (v2), name-only (legacy v2), or bare uuid (v1)
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
  """History events with bare-UUID resource locators.

  Line: `uuid resource locator action [timestamp]`
  """

  FORMAT = FORMAT_V1

  @classmethod
  def request_locator(cls, request: Request, data_dir: DataDir = None) -> str:
    return request.uuid

  @classmethod
  def scenario_locator(cls, scenario: Scenario, data_dir: DataDir = None) -> str:
    return scenario.uuid


class LogEventV2(LogEvent):
  """History events with v2 locators (request: slug/<uuid>; scenario: unique name).

  Line: `uuid timestamp action resource resource_id`
  (resource_id last so names may contain spaces).
  Also accepts legacy `uuid resource locator action [timestamp]` lines.
  """

  FORMAT = FORMAT_V2

  @classmethod
  def _parse_fields(cls, toks, line: str) -> _ParsedFields:
    if cls._is_v2_field_order(toks):
      event_uuid = toks[0]
      try:
        created_at = int(toks[1])
      except ValueError as e:
        raise MalformedLogEventError(
          line,
          f"created_at must be an integer timestamp, got {toks[1]!r}",
        ) from e
      action = toks[2]
      resource = toks[3]
      resource_uuid = COLUMN_DELIMITTER.join(toks[4:])
      if not resource_uuid:
        raise MalformedLogEventError(line, "missing resource id")
      return event_uuid, resource, resource_uuid, action, created_at

    # Legacy v2 lines still routed here by create()
    return super()._parse_fields(toks, line)

  @classmethod
  def format_line(
    cls,
    event_uuid: str,
    created_at: Optional[int],
    action: Action,
    resource_name: str,
    resource_uuid: str,
  ) -> str:
    ts = str(created_at if created_at is not None else int(time.time() * 1000))
    return COLUMN_DELIMITTER.join([
      event_uuid, ts, action, resource_name, resource_uuid,
    ])

  @classmethod
  def request_locator(cls, request: Request, data_dir: DataDir = None) -> str:
    slug = RequestSnapshotV2.build_request_slug(request.method, request.path)
    return f"{slug}/{request.uuid}"

  @classmethod
  def scenario_locator(cls, scenario: Scenario, data_dir: DataDir = None) -> str:
    # {stem}/{uuid}; stem prefers on-disk yaml (e.g. orphan -2 allocation)
    return ScenarioSnapshotV2.history_locator_for(
      scenario.uuid, scenario.name, data_dir=data_dir
    )
