import pdb

from typing import TYPE_CHECKING, Tuple

if TYPE_CHECKING:
    from requests import Response

from stoobly_agent.app.models.adapters.python import PythonResponseAdapterFactory
from stoobly_agent.app.proxy.mock.request_hasher import RequestHasher
from stoobly_agent.app.proxy.record.response_string_control import ResponseStringControl
from stoobly_agent.lib.orm.request import Request
from stoobly_agent.lib.orm.response import Response
from stoobly_agent.lib.orm.transformers import ORMToRequestsResponseTransformer
from stoobly_agent.lib.utils.decode import decode

from .local_db_adapter import LocalDBAdapter

class LocalDBResponseAdapter(LocalDBAdapter):
  __request_orm = None

  def __init__(self, request_orm: Request.__class__ = Request):
    self.__request_orm = request_orm

  def show(self, request_id):
    request = self.__request_orm.find(request_id)

    if not request:
      return self.__request_not_found()

    response = request.response
    return self.success([self.__to_show_response(response)])

  def mock(self, request_id) -> Tuple['Response', int]:
    request = self.__request_orm.find(request_id)

    if not request:
      return self.__request_not_found()

    response = request.response
    return self.success(ORMToRequestsResponseTransformer(response).with_response_id().transform())

  def update(self, response_id, **params):
    response = Response.find(response_id)

    if not response:
      return self.__request_not_found()
    
    transformer = ORMToRequestsResponseTransformer(response)

    request_params = {}

    if params.get('status'):
      transformer.with_status(params['status'])

    headers = params.get('headers') or {}
    if params.get('headers'):
      transformer.with_headers(headers)
      request_params['response_headers_hash'] = RequestHasher.instance().hash_params(headers)
 
    # If text not set and content-encoding changed 
    current_python_response = ORMToRequestsResponseTransformer(response).transform()
    if not params.get('text'):
      if headers.get('content-encoding') != current_python_response.headers.get('content-encoding'):
        params['text'] = current_python_response.content

    if params.get('text'):
      text: str = params['text'] # This will be given in decoded format
      content_encoding = self.content_encoding_header(headers, current_python_response.headers)
      encoded_text = self.encode_body(text, content_encoding)

      transformer.with_body(encoded_text)
      request_params['response_hash'] = RequestHasher.instance().hash_text(encoded_text)
      
    if params.get('latency'):
      control = response.control
      control = ResponseStringControl(control)
      control.timestamp = control.timestamp - control.latency * 1000 + int(params['latency']) * 1000
      control.latency = params['latency']
      params['control'] = control.serialize()
      del params['latency']

    if transformer.dirty:
      python_response = transformer.transform()
      params = {
        **params,
        'raw': PythonResponseAdapterFactory(python_response).raw_response()
      }

    if response.update(params):
      if len(request_params.keys()) != 0:
        request = self.__request_orm.find(response.request_id)

        if request:
          request.update(request_params)

      return self.success(self.__to_show_response(response))

    return self.internal_error('Could not update response')

  def __to_show_response(self, response: Response):
    python_response = ORMToRequestsResponseTransformer(response).transform()
    headers = python_response.headers
    content = python_response.content

    return {
      'id': response.id,
      'mime_type': headers.get('content-type'),
      'text': decode(content),
    }

  def __request_not_found(self):
    return self.not_found('Request not found')