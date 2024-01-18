import pdb
import requests

from stoobly_agent.app.settings import Settings

from .factories.resource.body import BodyResourceFactory
from .model import Model

class BodyModel(Model):

  def __init__(self, settings: Settings, **options):
    super().__init__(settings, **options)

  def as_local(self):
    self.adapter = BodyResourceFactory(self.settings.remote).local_db()
    self.is_local = False

  def as_remote(self):
    self.is_local = False

  def update(self, request_id: int, text: str):
    try:
      return self.adapter.update(request_id, text)
    except requests.exceptions.RequestException as e:
      return self.handle_request_error(e)

  def mock(self, request_id: str):
    try:
      return self.adapter.mock(request_id)
    except requests.exceptions.RequestException as e:
      return self.handle_request_error(e)