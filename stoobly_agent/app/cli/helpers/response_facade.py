from stoobly_agent.app.models.response_model import ResponseModel
from stoobly_agent.app.settings import Settings
from stoobly_agent.lib.api.keys import RequestKey
from stoobly_agent.lib.orm.request import Request

from .request_facade import RequestNotFoundError

class ResponseNotFoundError(Exception):
  pass

class ResponseFacade:

  def __init__(self, settings: Settings):
    self.__model = ResponseModel(settings)

  def update(self, request_key: str, params: dict):
    key = RequestKey(request_key)
    request = Request.find_by(uuid=key.id)

    if not request:
      raise RequestNotFoundError('Request not found')

    response = request.response

    if not response:
      raise ResponseNotFoundError('Response not found')

    return self.__model.update(response.id, **params)
