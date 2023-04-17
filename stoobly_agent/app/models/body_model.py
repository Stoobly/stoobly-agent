import pdb
import requests

from stoobly_agent.app.settings import Settings
from stoobly_agent.lib.logger import Logger

from .factories.resource.body import BodyResourceFactory
from .model import Model

class BodyModel(Model):

  def __init__(self, settings: Settings):
    super().__init__(settings)

  def as_local(self):
    self.adapter = BodyResourceFactory(self.settings.remote).local_db()

  def as_remote(self):
    # 'Not yet supported.'
    pass 

  def update(self, request_id: int, text: str):
    try:
      return self.adapter.update(request_id, text)
    except requests.exceptions.RequestException as e:
      self.__handle_request_error(e)
      return None

  def mock(self, request_id: str) -> requests.Request:
    try:
      return self.adapter.mock(request_id)
    except requests.exceptions.RequestException as e:
      self.__handle_request_error(e)
      return None

  def __handle_request_error(self, e: requests.exceptions.RequestException):
      response: requests.Response = e.response
      if response:
        Logger.instance().error(f"{response.status_code} {response.content}")