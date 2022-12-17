from stoobly_agent.app.settings import RemoteSettings
from stoobly_agent.lib.orm.request import Request

from .local_db.body_adapter import LocalDBBodyAdapter

class BodyAdapterFactory():

  def __init__(self, settings: RemoteSettings):
    self.__remote_settings = settings

  def local_db(self) -> LocalDBBodyAdapter:
    return LocalDBBodyAdapter(Request)  