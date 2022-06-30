from orator.orm import belongs_to, has_many

from . import ORM 
from .trace_alias import TraceAlias

class TraceRequest(ORM.instance().base):
  __fillable__ = []

  @belongs_to
  def trace(self):
    from .trace import Trace
    return Trace

  @has_many
  def trace_aliases(self):
    return TraceAlias