import pdb

from stoobly_agent.app.settings import Settings

from .factories.resource.response import ResponseResourceFactory
from .model import Model

class ResponseModel(Model):

  def __init__(self, settings: Settings, **options):
    super().__init__(settings, **options)

  def as_local(self):
    self.adapter = ResponseResourceFactory(self.settings.remote).local_db()
    self.is_local = True

  def as_remote(self):
    self.is_local = False

  def show(self, request_id: str):
    try:
      return self.adapter.show(request_id)
    except Exception as e:
      import requests
      if isinstance(e, requests.exceptions.RequestException):
        return self.handle_request_error(e)
      raise

  def mock(self, request_id: str):
    try:
      return self.adapter.mock(request_id)
    except Exception as e:
      import requests
      if isinstance(e, requests.exceptions.RequestException):
        return self.handle_request_error(e)
      raise

  def update(self, response_id: str, **params):
    try:
      return self.adapter.update(response_id, **params)
    except Exception as e:
      import requests
      if isinstance(e, requests.exceptions.RequestException):
        return self.handle_request_error(e)
      raise