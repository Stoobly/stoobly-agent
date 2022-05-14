from orator.orm import has_many

from . import ORM 
from .trace_alias import TraceAlias

class Trace(ORM.instance().base):
  __fillable__ = []

  @has_many
  def trace_aliases(self):
    return TraceAlias