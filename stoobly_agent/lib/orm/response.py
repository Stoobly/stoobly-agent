from .base import Base

class Response(Base):
  __fillable__ = ['control','request_id', 'raw']