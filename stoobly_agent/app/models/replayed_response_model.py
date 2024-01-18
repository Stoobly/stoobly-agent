import pdb
import requests

from stoobly_agent.app.settings import Settings

from .factories.resource.replayed_response import ReplayedResponseResourceFactory
from .model import Model
from .types import ReplayeResponseCreateParams

class ReplayedResponseModel(Model):

  def __init__(self, settings: Settings, **options):
    super().__init__(settings, **options)

  def as_local(self):
    self.adapter = ReplayedResponseResourceFactory(self.settings.remote).local_db()
    self.is_local = True

  def as_remote(self):
    self.is_local = False

  def create(self, **body_params: ReplayeResponseCreateParams):
    try:
      return self.adapter.create(**body_params)
    except requests.exceptions.RequestException as e:
      return self.handle_request_error(e)

  def index(self, **query_params):
    try:
      return self.adapter.index(**query_params)
    except requests.exceptions.RequestException as e:
      return self.handle_request_error(e)

  def mock(self, replayed_response_id: str):
    try:
      return self.adapter.mock(replayed_response_id)
    except requests.exceptions.RequestException as e:
      return self.handle_request_error(e)

  def activate(self, replayed_response_id: str):
    try:
      return self.adapter.activate(replayed_response_id)
    except requests.exceptions.RequestException as e:
      return self.handle_request_error(e)

  def raw(self, replayed_response_id: str):
    try:
      return self.adapter.raw(replayed_response_id)
    except requests.exceptions.RequestException as e:
      return self.handle_request_error(e)

  def update(self, replayed_response_id: str, **params) -> requests.Response:
    try:
      return self.adapter.update(replayed_response_id, **params)
    except requests.exceptions.RequestException as e:
      return self.handle_request_error(e)