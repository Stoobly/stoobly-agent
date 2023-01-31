import pdb
import requests

from typing import Union

from stoobly_agent.app.models.schemas.request import Request
from stoobly_agent.app.settings import Settings
from stoobly_agent.lib.api.interfaces import RequestShowResponse
from stoobly_agent.lib.logger import Logger

from .adapters.request_adapter_factory import RequestAdapterFactory
from .adapters.types import RequestCreateParams, RequestShowParams
from .model import Model
from .types.requests_model_index import RequestsModelIndex

class RequestModel(Model):

  def __init__(self, settings: Settings):
    super().__init__(settings)

  def as_local(self):
      self.adapter = RequestAdapterFactory(self.settings.remote).local_db()

  def as_remote(self):
      self.adapter = RequestAdapterFactory(self.settings.remote).stoobly()

  def create(self, **body_params: RequestCreateParams) -> Union[RequestsModelIndex, None]:
    try:
      return self.adapter.create(**body_params)
    except requests.exceptions.RequestException as e:
      self.__handle_request_error(e)
      return None

  def show(self, request_id: str, **params: RequestShowParams) -> Union[RequestShowResponse, None]:
    try:
      return self.adapter.show(request_id, **params)
    except requests.exceptions.RequestException as e:
      self.__handle_request_error(e)
      return None

  def response(self, **query_params):
    return self.adapter.response(**query_params)

  def index(self, **query_params) -> Union[RequestsModelIndex, None]:
    try:
      return self.adapter.index(**query_params)
    except requests.exceptions.RequestException as e:
      self.__handle_request_error(e)
      return None

  def update(self, request_id: str, **params: Request) -> Union[Request, None]:
    try:
      return self.adapter.update(request_id, **params)
    except requests.exceptions.RequestException as e:
      self.__handle_request_error(e)
      return None

  def destroy(self, request_id) -> Union[Request, None]:
    try:
      return self.adapter.destroy(request_id)
    except requests.exceptions.RequestException as e:
      self.__handle_request_error(e)
      return None 

  def __handle_request_error(self, e: requests.exceptions.RequestException):
      response: requests.Response = e.response
      if response:
        Logger.instance().error(f"{response.status_code} {response.content}")