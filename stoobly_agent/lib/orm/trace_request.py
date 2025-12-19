from stoobly_orator.orm import belongs_to, has_many

from .base import Base

class TraceRequest(Base):
  __fillable__ = ['trace_id']

  @belongs_to
  def trace(self):
    from .trace import Trace
    return Trace

  @has_many
  def trace_aliases(self):
    from .trace_alias import TraceAlias
    return TraceAlias

def handle_deleting(trace):
  trace_aliaces = trace.trace_aliases

  for trace_alias in trace_aliaces:
    trace_alias.delete()

TraceRequest.deleting(handle_deleting)