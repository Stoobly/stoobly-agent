import json

from orator.orm import accessor, belongs_to

from .base import Base

DICT_TYPE = type({}).__name__
LIST_TYPE = type([]).__name__

class TraceAlias(Base):
  __fillable__ = ['assigned_to', 'assigned_to_inferred_type', 'name', 'trace_id', 'trace_request_id', 'value', 'value_inferred_type']

  @belongs_to
  def trace(self):
    from .trace import Trace # Get around circular import
    return Trace

  @belongs_to
  def trace_request(self):
    from .trace_request import TraceRequest
    return TraceRequest

  @accessor
  def assigned_to(self):
    _assigned_to = self.raw_assigned_to

    return self.__deserialize(_assigned_to, self.assigned_to_inferred_type)

  @accessor
  def value(self):
    _value = self.raw_value

    return self.__deserialize(_value, self.value_inferred_type)

  @property
  def raw_assigned_to(self):
    try:
      return self.get_raw_attribute('assigned_to')
    except KeyError as e:
      return None

  @property
  def raw_value(self):
    try:
      return self.get_raw_attribute('value')
    except KeyError as e:
      return None

  def serialize_assigned_to(self):
    _assigned_to = self.raw_assigned_to
    assigned_to_inferred_type = type(_assigned_to).__name__

    # If non primitive type, serialize
    if assigned_to_inferred_type == DICT_TYPE or assigned_to_inferred_type == LIST_TYPE:
      self.assigned_to = json.dumps(_assigned_to)

    self.assigned_to_inferred_type = assigned_to_inferred_type

  def serialize_value(self):
    _value = self.raw_value
    value_inferred_type = type(_value).__name__

    # If non primitive type, serialize
    if value_inferred_type == DICT_TYPE or value_inferred_type == LIST_TYPE:
      self.value = json.dumps(_value)

    self.value_inferred_type = value_inferred_type

  def __deserialize(self, value, inferred_type):
    if inferred_type == DICT_TYPE or inferred_type == LIST_TYPE:
      # If updating, _value can be non str or byte. _value will be what the user sets
      if isinstance(value, bytes) or isinstance(value, str):
        return json.loads(value)
      else:
        return value
    else:
      return value

# Handles creating and updating
def handle_saving(trace_alias):
  trace_alias.serialize_value()
  trace_alias.serialize_assigned_to()

TraceAlias.saving(handle_saving)
