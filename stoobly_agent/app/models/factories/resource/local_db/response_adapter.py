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
    return self.success(
      self.__transformer_with_sse_body(response).with_response_id().transform()
    )

  def update(self, response_id, **params):
    response = Response.find(response_id)

    if not response:
      return self.__request_not_found()

    is_streamed = self.__is_streamed(response)
    transformer = ORMToRequestsResponseTransformer(response)

    request_params = {}
    chunk_payload = None

    if params.get('status'):
      transformer.with_status(params['status'])

    headers = params.get('headers') or {}
    if params.get('headers'):
      transformer.with_headers(headers)
      request_params['response_headers_hash'] = RequestHasher.instance().hash_params(headers)

    # Prefer hydrated body for SSE so content-encoding changes re-encode stream text
    current_python_response = self.__transformer_with_sse_body(response).transform()
    # Only auto-fill text when headers are being updated; omitted headers is {} so
    # content-encoding would always look changed vs any existing encoding.
    if params.get('text') is None and params.get('headers'):
      if headers.get('content-encoding') != current_python_response.headers.get('content-encoding'):
        content = current_python_response.content
        params['text'] = decode(content) if isinstance(content, (bytes, bytearray)) else content

    if params.get('text') is not None:
      text = params['text']
      if isinstance(text, (bytes, bytearray)):
        text = decode(text)
      content_encoding = self.content_encoding_header(headers, current_python_response.headers)
      encoded_text = self.encode_body(text, content_encoding)
      if not isinstance(encoded_text, (bytes, bytearray)):
        encoded_text = encoded_text.encode()

      if is_streamed:
        # Body lives in response_chunks; keep Response.raw envelope-only.
        chunk_payload = bytes(encoded_text)
        request_params['response_hash'] = RequestHasher.instance().hash_text(b'')
      else:
        transformer.with_body(encoded_text)
        request_params['response_hash'] = RequestHasher.instance().hash_text(encoded_text)

    if params.get('latency') is not None:
      control = response.control
      control = ResponseStringControl(control)
      control.timestamp = control.timestamp - control.latency * 1000 + int(params['latency']) * 1000
      control.latency = params['latency']
      params['control'] = control.serialize()
      del params['latency']

    update_cols = {}
    if params.get('control') is not None:
      update_cols['control'] = params['control']

    if transformer.dirty:
      if is_streamed:
        # Envelope only — never fold stream body into raw
        transformer.with_body(b'')
      python_response = transformer.transform()
      update_cols['raw'] = PythonResponseAdapterFactory(python_response).raw_response()

    if not update_cols and chunk_payload is None and not request_params:
      return self.success(self.__to_show_response(response))

    # One transaction so chunk rewrite cannot commit without envelope/request hash
    from stoobly_agent.lib.orm import ORM
    try:
      with ORM.instance().db.transaction():
        if chunk_payload is not None:
          from stoobly_agent.app.proxy.record.sse_record_service import replace_response_chunks
          replace_response_chunks(response, chunk_payload)

        if update_cols:
          if not response.update(update_cols):
            raise RuntimeError('Could not update response')

        if request_params:
          request = self.__request_orm.find(response.request_id)
          if request and not request.update(request_params):
            raise RuntimeError('Could not update request')
    except Exception:
      return self.internal_error('Could not update response')

    # Reload so show sees fresh stream_status / chunks
    response = Response.find(response_id)
    return self.success(self.__to_show_response(response))

  def __is_streamed(self, response: Response) -> bool:
    from stoobly_agent.lib.orm.response_chunk import ResponseChunk
    if response.stream_status:
      return True
    return ResponseChunk.where('response_id', response.id).count() > 0

  def __transformer_with_sse_body(self, response: Response) -> ORMToRequestsResponseTransformer:
    """Envelope from Response.raw; SSE body joined from response_chunks when present."""
    transformer = ORMToRequestsResponseTransformer(response)

    from stoobly_agent.lib.orm.response_chunk import ResponseChunk
    chunk_count = ResponseChunk.where('response_id', response.id).count()
    if response.stream_status or chunk_count > 0:
      from stoobly_agent.app.proxy.record.sse_record_service import sse_body_from_chunks
      transformer = transformer.with_body(sse_body_from_chunks(response))

    return transformer

  def __to_show_response(self, response: Response):
    python_response = self.__transformer_with_sse_body(response).transform()
    headers = python_response.headers
    content = python_response.content

    return {
      'id': response.id,
      'mime_type': headers.get('content-type'),
      'text': decode(content),
    }

  def __request_not_found(self):
    return self.not_found('Request not found')
