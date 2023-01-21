from .base import Base

class Scenario(Base):
  __fillable__ = ['name','description', 'is_deleted', 'position', 'priority', 'starred']