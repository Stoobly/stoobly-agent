import pdb
import requests

from stoobly_agent.app.settings import Settings
from stoobly_agent.lib.logger import Logger

from .factories.resource.response import ResponseResourceFactory
from .model import Model
from .types import ResponseShowResponse

class ResponseModel(Model):

  def __init__(self, settings: Settings):
    super().__init__(settings)

  def as_local(self):
    self.adapter = ResponseResourceFactory(self.settings.remote).local_db()

  def as_remote(self):
    # raise('Not yet supported.')
    pass

  def show(self, request_id: str) -> ResponseShowResponse:
    try:
      return self.adapter.show(request_id)
    except requests.exceptions.RequestException as e:
      self.__handle_request_error(e)
      return None

  def mock(self, request_id: str) -> requests.Response:
    try:
      return self.adapter.mock(request_id)
    except requests.exceptions.RequestException as e:
      self.__handle_request_error(e)
      return None

  def update(self, request_id: str, **params) -> requests.Response:
    try:
      return self.adapter.update(request_id, **params)
    except requests.exceptions.RequestException as e:
      self.__handle_request_error(e)
      return None

  def __handle_request_error(self, e: requests.exceptions.RequestException):
      response: requests.Response = e.response
      if response:
        Logger.instance().error(f"{response.status_code} {response.content}")