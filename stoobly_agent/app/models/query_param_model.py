import pdb
import requests

from typing import Union

from stoobly_agent.app.settings import Settings
from stoobly_agent.lib.api.interfaces import QueryParam

from .factories.resource.query_param import QueryParamResourceFactory
from .model import Model

class QueryParamModel(Model):

  def __init__(self, settings: Settings, **options):
    super().__init__(settings, **options)

  def as_local(self):
    self.adapter =  QueryParamResourceFactory(self.settings.remote).local_db()
    self.is_local = True

  def as_remote(self):
    self.is_local = False

  def create(self, request_id: int, **params: QueryParam):
    try:
      return self.adapter.create(request_id, **params)
    except requests.exceptions.RequestException as e:
      return self.handle_request_error(e)

  def index(self, request_id: int, **query_params):
    try:
      return self.adapter.index(request_id, **query_params)
    except requests.exceptions.RequestException as e:
      return self.handle_request_error(e)

  def update(self, request_id: int, query_param_id: str, **params: QueryParam):
    try:
      return self.adapter.update(request_id, query_param_id, **params)
    except requests.exceptions.RequestException as e:
      return self.handle_request_error(e)

  def destroy(self, request_id: str, id: str):
    try:
      return self.adapter.destroy(request_id, id)
    except requests.exceptions.RequestException as e:
      return self.handle_request_error(e)