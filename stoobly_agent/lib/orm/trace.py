from orator.orm import has_many

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

def handle_deleting(trace):
  trace_aliaces = trace.trace_aliases

  for trace_alias in trace_aliaces:
    trace_alias.delete()

  trace_requests = trace.trace_requests
  for trace_request in trace_requests:
    trace_request.delete()

Trace.deleting(handle_deleting)