import pdb
import requests

from typing import List, TypedDict, Union

from stoobly_agent.lib.models.schemas.request import Request
from stoobly_agent.lib.logger import Logger
from stoobly_agent.lib.settings import Settings

from .adapters.request_adapter_factory import RequestAdapterFactory
from .adapters.types.request_create_params import RequestCreateParams
from .types.requests_model_index import RequestsModelIndex

class RequestModel():

  def __init__(self, settings: Settings):
    if not settings.remote_enabled:
      self.adapter =  RequestAdapterFactory(settings).local_db()
    else:
      self.adapter =  RequestAdapterFactory(settings).stoobly()

  def create(self, **body_params: RequestCreateParams) -> Union[Request, None]:
    try:
      return Request(self.adapter.create(**body_params))
    except requests.exceptions.RequestException as e:
      self.__handle_request_error(e)
      return None

  def show(self, project_id: str, request_id: str, query_params) -> Union[Request, None]:
    try:
      return Request(self.adapter.show(project_id, request_id, query_params))
    except requests.exceptions.RequestException as e:
      self.__handle_request_error(e)
      return None

  def response(self, **query_params):
    return self.adapter.response(**query_params)

  def index(self, project_id: int, query_params) -> Union[RequestsModelIndex, None]:
    try:
      res = self.adapter.index(project_id, query_params)
    except requests.exceptions.RequestException as e:
      self.__handle_request_error(e)
      return None, None

    return {
      'list': list(map(lambda request_response: Request(request_response), res['list'])),
      'total': res['total'],
    }

  def __handle_request_error(self, e: requests.exceptions.RequestException):
      response: requests.Response = e.response
      Logger.instance().error(f"{response.status_code} {response.content}")