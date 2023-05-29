import pdb

import requests

from stoobly_agent.app.models.schemas.request import Request
from stoobly_agent.app.settings import Settings

from .factories.resource.request import RequestResourceFactory
from .model import Model
from .types import RequestCreateParams, RequestDestroyParams, RequestDestroyAllParams, RequestFindParams, RequestShowParams

class RequestModel(Model):

  def __init__(self, settings: Settings):
    super().__init__(settings)

  def as_local(self):
      self.adapter = RequestResourceFactory(self.settings.remote).local_db()

  def as_remote(self):
      self.adapter = RequestResourceFactory(self.settings.remote).stoobly()

  def create(self, **body_params: RequestCreateParams):
    try:
      return self.adapter.create(**body_params)
    except requests.exceptions.RequestException as e:
      return self.handle_request_error(e)

  def show(self, request_id: str, **params: RequestShowParams):
    try:
      return self.adapter.show(request_id, **params)
    except requests.exceptions.RequestException as e:
      return self.handle_request_error(e)

  def find_similar(self, params: RequestFindParams):
    try:
      # TODO: fix adapter
      local_adapter = RequestResourceFactory(self.settings.remote).local_db()
      return local_adapter.find_similar_requests(params)

      # return self.adapter.find_similar(params)
    except requests.exceptions.RequestException as e:
      return self.handle_request_error(e)

  def response(self, **query_params):
    return self.adapter.response(**query_params)

  def index(self, **query_params):
    try:
      return self.adapter.index(**query_params)
    except requests.exceptions.RequestException as e:
      return self.handle_request_error(e)

  def update(self, request_id: str, **params: Request):
    try:
      return self.adapter.update(request_id, **params)
    except requests.exceptions.RequestException as e:
      return self.handle_request_error(e)

  def destroy(self, request_id: str, **params: RequestDestroyParams):
    try:
      return self.adapter.destroy(request_id, **params)
    except requests.exceptions.RequestException as e:
      return self.handle_request_error(e)

  def destroy_all(self, **params: RequestDestroyAllParams):
    try:
      return self.adapter.destroy_all(**params)
    except requests.exceptions.RequestException as e:
      return self.handle_request_error(e)

  def snapshot(self, request_id: str, **params):
    try:
      return self.adapter.snapshot(request_id, **params)
    except requests.exceptions.RequestException as e:
      return self.handle_request_error(e)
