import pdb
import requests

from typing import Union
from stoobly_agent.app.models.adapters.header_adapter_factory import HeaderAdapterFactory

from stoobly_agent.app.models.types.request_components import HeaderIndexResponse
from stoobly_agent.app.settings import Settings
from stoobly_agent.lib.logger import Logger

class HeaderModel():

  def __init__(self, settings: Settings):
    self.settings = settings

    if not settings.cli.features.remote:
      self.as_local()
    else:
      self.as_remote()

  def as_local(self):
    self.adapter =  HeaderAdapterFactory(self.settings.remote).local_db()

  def as_remote(self):
    # raise('Not yet supported.')
    pass

  def index(self, request_id: str, **query_params) -> Union[HeaderIndexResponse, None]:
    try:
      return self.adapter.index(request_id, **query_params)
    except requests.exceptions.RequestException as e:
      self.__handle_request_error(e)
      return None

  def __handle_request_error(self, e: requests.exceptions.RequestException):
      response: requests.Response = e.response
      if response:
        Logger.instance().error(f"{response.status_code} {response.content}")