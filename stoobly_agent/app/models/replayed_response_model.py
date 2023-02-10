import pdb
import requests

from stoobly_agent.app.models.adapters.replayed_response_adapter_factory import ReplayedResponseAdapterFactory
from stoobly_agent.app.settings import Settings
from stoobly_agent.lib.logger import Logger

from .model import Model

class ReplayedResponseModel(Model):

  def __init__(self, settings: Settings):
    super().__init__(settings)

  def as_local(self):
    self.adapter =  ReplayedResponseAdapterFactory(self.settings.remote).local_db()

  def as_remote(self):
    # raise('Not yet supported.')
    pass

  def index(self, **query_params):
    try:
      return self.adapter.index(**query_params)
    except requests.exceptions.RequestException as e:
      self.__handle_request_error(e)
      return None

  def mock(self, replayed_response_id: str) -> requests.Response:
    try:
      return self.adapter.mock(replayed_response_id)
    except requests.exceptions.RequestException as e:
      self.__handle_request_error(e)
      return None

  def raw(self, replayed_response_id: str) -> requests.Response:
    try:
      return self.adapter.raw(replayed_response_id)
    except requests.exceptions.RequestException as e:
      self.__handle_request_error(e)
      return None

  def update(self, replayed_response_id: str, **params) -> requests.Response:
    try:
      return self.adapter.update(replayed_response_id, **params)
    except requests.exceptions.RequestException as e:
      self.__handle_request_error(e)
      return None

  def __handle_request_error(self, e: requests.exceptions.RequestException):
      response: requests.Response = e.response
      if response:
        Logger.instance().error(f"{response.status_code} {response.content}")