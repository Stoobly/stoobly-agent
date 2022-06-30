from orator.orm import has_many

from .base import Base
from .trace_alias import TraceAlias

class Trace(Base):
  __fillable__ = []

  @has_many
  def trace_aliases(self):
    return TraceAlias