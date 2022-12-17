from stoobly_agent.app.settings import RemoteSettings
from stoobly_agent.lib.orm.request import Request

from .local_db.response_header_adapter import LocalDBResponseHeaderAdapter

class ResponseHeaderAdapterFactory():

  def __init__(self, settings: RemoteSettings):
    self.__remote_settings = settings

  def local_db(self) -> LocalDBResponseHeaderAdapter:
    return LocalDBResponseHeaderAdapter(Request)  