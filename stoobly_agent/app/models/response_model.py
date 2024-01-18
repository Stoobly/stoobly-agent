import pdb
import requests

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
    except requests.exceptions.RequestException as e:
      return self.handle_request_error(e)

  def mock(self, request_id: str):
    try:
      return self.adapter.mock(request_id)
    except requests.exceptions.RequestException as e:
      return self.handle_request_error(e)

  def update(self, request_id: str, **params):
    try:
      return self.adapter.update(request_id, **params)
    except requests.exceptions.RequestException as e:
      return self.handle_request_error(e)