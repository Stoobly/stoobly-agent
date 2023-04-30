import pdb
import requests

from stoobly_agent.app.models.types.request_components import Header
from stoobly_agent.app.settings import Settings

from .factories.resource.response_header import ResponseHeaderResourceFactory
from .model import Model

class ResponseHeaderModel(Model):

  def __init__(self, settings: Settings):
    super().__init__(settings)

  def as_local(self):
    self.adapter =  ResponseHeaderResourceFactory(self.settings.remote).local_db()

  def as_remote(self):
    # raise('Not yet supported.')
    pass

  def create(self, request_id: int, **params: Header):
    try:
      return self.adapter.create(request_id, **params)
    except requests.exceptions.RequestException as e:
      return self.handle_request_error(e)

  def index(self, request_id: str, **query_params):
    try:
      return self.adapter.index(request_id, **query_params)
    except requests.exceptions.RequestException as e:
      return self.handle_request_error(e)

  def update(self, request_id: int, **params: Header):
    try:
      return self.adapter.update(request_id, **params)
    except requests.exceptions.RequestException as e:
      return self.handle_request_error(e)

  def destroy(self, request_id: str, id: str):
    try:
      return self.adapter.destroy(request_id, id)
    except requests.exceptions.RequestException as e:
      return self.handle_request_error(e)