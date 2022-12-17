from stoobly_agent.app.settings import RemoteSettings
from stoobly_agent.lib.orm.request import Request

from .local_db.header_adapter import LocalDBHeaderAdapter

class HeaderAdapterFactory():

  def __init__(self, settings: RemoteSettings):
    self.__remote_settings = settings

  def local_db(self) -> LocalDBHeaderAdapter:
    return LocalDBHeaderAdapter(Request)  