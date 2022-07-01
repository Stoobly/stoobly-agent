from orator.orm import belongs_to, has_many

from .base import Base
from .trace_alias import TraceAlias

class TraceRequest(Base):
  __fillable__ = ['trace_id']

  @belongs_to
  def trace(self):
    from .trace import Trace
    return Trace

  @has_many
  def trace_aliases(self):
    return TraceAlias