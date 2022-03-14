import requests

from typing import List, TypedDict, Union

from stoobly_agent.lib.models.schemas.request import Request
from stoobly_agent.lib.logger import Logger
from stoobly_agent.lib.settings import Settings

from .adapters.request_adapter_factory import RequestAdapterFactory
from .types.requests_model_index import RequestsModelIndex

class RequestModel():

  def __init__(self, settings: Settings):
    self.adapter = RequestAdapterFactory(settings).get()

  def create(self, project_id: str, raw_requests, params) -> Union[Request, None]:
    try:
      return Request(self.adapter.create(project_id, raw_requests, params))
    except requests.exceptions.RequestException as e:
      self.__handle_request_error(e)
      return None

  def show(self, project_id: str, request_id: str, query_params) -> Union[Request, None]:
    try:
      return Request(self.adapter.show(project_id, request_id, query_params))
    except requests.exceptions.RequestException as e:
      self.__handle_request_error(e)
      return None

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