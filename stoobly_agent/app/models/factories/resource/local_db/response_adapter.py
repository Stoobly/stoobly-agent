import pdb
import requests

from stoobly_agent.app.models.adapters.python import PythonResponseAdapterFactory
from stoobly_agent.lib.orm.request import Request
from stoobly_agent.lib.orm.response import Response
from stoobly_agent.lib.orm.transformers import ORMToRequestsResponseTransformer

class LocalDBResponseAdapter():
  __request_orm = None

  def __init__(self, request_orm: Request.__class__ = Request):
    self.__request_orm = request_orm

  def show(self, request_id):
    request = self.__request_orm.find(request_id)

    if not request:
      return None

    response = request.response
    return [self.__to_show_response(response)]

  def mock(self, request_id) -> requests.Response:
    request = self.__request_orm.find(request_id)

    if not request:
      return None

    response = request.response
    return ORMToRequestsResponseTransformer(response).with_response_id().transform()

  def update(self, response_id, **params):
    response = Response.find(response_id)

    if not response:
      return
    
    transformer = ORMToRequestsResponseTransformer(response)

    if params.get('headers'):
      transformer.with_headers(params['headers'])

    if params.get('status'):
      transformer.with_status(params['status'])

    if params.get('text'):
      encoded_text = params['text'].encode()
      transformer.with_body(encoded_text)

    if transformer.dirty:
      python_response = transformer.transform()
      params = {
        **params,
        'raw': PythonResponseAdapterFactory(python_response).raw_response()
      }

    if response.update(params):
      return self.__to_show_response(response)

  def __to_show_response(self, response: Response):
    python_response = ORMToRequestsResponseTransformer(response).transform()

    return {
      'id': response.id,
      'mime_type': python_response.headers.get('content-type'),
      'text': python_response.content.decode(),
    }

