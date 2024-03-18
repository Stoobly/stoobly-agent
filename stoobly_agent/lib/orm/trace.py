from stoobly_orator.orm import has_many

from .base import Base
from .trace_alias import TraceAlias
from .trace_request import TraceRequest

class Trace(Base):
  __fillable__ = []

  @has_many
  def trace_aliases(self):
    return TraceAlias

  @has_many
  def trace_requests(self):
    return TraceRequest

  def clone(self):
    trace = self.create()
    if not trace:
      return

    for alias in self.trace_aliases:
      TraceAlias.create(
        name=alias.name,
        trace_id=trace.id,
        value=alias.value,
        value_inferred_type=alias.value_inferred_type,
      )

    return trace

def handle_deleting(trace):
  trace_aliaces = trace.trace_aliases

  for trace_alias in trace_aliaces:
    trace_alias.delete()

  trace_requests = trace.trace_requests
  for trace_request in trace_requests:
    trace_request.delete()

Trace.deleting(handle_deleting)