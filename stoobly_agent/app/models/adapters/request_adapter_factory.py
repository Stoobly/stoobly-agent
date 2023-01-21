from stoobly_agent.lib.orm.request import Request
from stoobly_agent.lib.api.requests_resource import RequestsResource
from stoobly_agent.app.settings import RemoteSettings

from .local_db.request_adapter import LocalDBRequestAdapter
from .stoobly_request_adapter import StooblyRequestAdapter

class RequestAdapterFactory():

  def __init__(self, settings: RemoteSettings):
    self.__remote_settings = settings

  def local_db(self) -> LocalDBRequestAdapter:
    return LocalDBRequestAdapter(Request)  

  def stoobly(self) -> StooblyRequestAdapter:
    api = RequestsResource(self.__remote_settings.api_url, self.__remote_settings.api_key)
    return StooblyRequestAdapter(api)