import json

from orator.orm import accessor, belongs_to

from .base import Base

DICT_TYPE = type({}).__name__
LIST_TYPE = type([]).__name__

class TraceAlias(Base):
  __fillable__ = ['assigned_to', 'inferred_type', 'name', 'trace_id', 'value']

  @belongs_to
  def trace(self):
    from .trace import Trace # Get around circular import
    return Trace

  @belongs_to
  def trace_request(self):
    from .trace_request import TraceRequest
    return TraceRequest

  @accessor
  def value(self):
    _value = self.get_raw_attribute('value')

    if self.inferred_type == DICT_TYPE or self.inferred_type == LIST_TYPE:
      # If updating, _value can be non str or byte. _value will be what the user sets
      if isinstance(_value, bytes) or isinstance(_value, str):
        return json.loads(_value)
      else:
        return _value
    else:
      return _value

  @property
  def raw_value(self):
    return self.get_raw_attribute('value')

  def serialize_value(self):
    _value = self.raw_value
    inferred_type = type(_value).__name__

    # If non primitive type, serialize
    if inferred_type == DICT_TYPE or inferred_type == LIST_TYPE:
      self.value = json.dumps(_value)

    self.inferred_type = inferred_type

# Handles creating and updating
def handle_saving(trace_alias):
  trace_alias.serialize_value()

TraceAlias.saving(handle_saving)