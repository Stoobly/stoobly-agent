from . import ORM 

class Response(ORM.instance().base):
  __fillable__ = ['control','request_id', 'raw']