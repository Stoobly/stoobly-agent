from typing import TYPE_CHECKING, Callable, List, Optional

if TYPE_CHECKING:
  from mitmproxy.http import HTTPFlow as MitmproxyHTTPFlow

from stoobly_agent.app.models.request_model import RequestModel
from stoobly_agent.app.proxy.intercept_settings import InterceptSettings
from stoobly_agent.app.proxy.mock.request_hasher import RequestHasher
from stoobly_agent.app.proxy.record.join_request_service import join_request_from_flow
from stoobly_agent.config.constants import stream_status
from stoobly_agent.lib.api.param_builder import ParamBuilder
from stoobly_agent.lib.logger import Logger
from stoobly_agent.lib.orm.request import Request
from stoobly_agent.lib.orm.response import Response
from stoobly_agent.lib.orm.response_chunk import ResponseChunk

LOG_ID = 'SseRecord'

# Flow metadata: Response.id created for this SSE stream
SSE_RESPONSE_ID_KEY = 'stoobly_sse_response_id'
SSE_FINALIZED_KEY = 'stoobly_sse_finalized'

# Caps for never-ending streams (still forward after cap; stop persisting)
MAX_SSE_CHUNKS = 10_000
MAX_SSE_BYTES = 10 * 1024 * 1024


def is_sse_flow(flow: 'MitmproxyHTTPFlow') -> bool:
  response = getattr(flow, 'response', None)
  if not response:
    return False
  from stoobly_agent.app.proxy.replay.body_parser_service import is_event_stream
  content_type = response.headers.get('content-type')
  return is_event_stream(content_type)


def start_sse_record(
  flow: 'MitmproxyHTTPFlow',
  request_model: RequestModel,
  intercept_settings: InterceptSettings,
) -> Optional[Response]:
  """
  Create Request + envelope-only Response, then tee streamed body into response_chunks.
  Never appends chunk payloads into Response.raw.
  """
  if flow.metadata.get(SSE_RESPONSE_ID_KEY):
    return Response.find(flow.metadata[SSE_RESPONSE_ID_KEY])

  joined_request = join_request_from_flow(flow, intercept_settings=intercept_settings)

  body_params = ParamBuilder({ 'flow': flow, 'joined_request': joined_request })
  body_params.with_resource_scoping(
    intercept_settings.project_key,
    intercept_settings.scenario_key,
  )
  sequence_id = intercept_settings.request_sequence_id
  if sequence_id is not None:
    body_params.with_param('sequence_id', sequence_id)

  created, status = request_model.create(**body_params.build())
  if not created or status >= 400:
    Logger.instance(LOG_ID).error(f"Failed to create SSE request status={status}")
    enable_sse_passthrough(flow)
    return None

  request_uuid = created['list'][0]['uuid']
  request_record = Request.find_by(uuid=request_uuid)
  if not request_record:
    enable_sse_passthrough(flow)
    return None

  response_record = request_record.response
  if not response_record:
    enable_sse_passthrough(flow)
    return None

  response_record.update(stream_status=stream_status.STREAMING)

  flow.metadata[SSE_RESPONSE_ID_KEY] = response_record.id
  flow.metadata[SSE_FINALIZED_KEY] = False

  flow.response.stream = _build_tee(flow, response_record.id)
  Logger.instance(LOG_ID).debug(f"Started SSE record response_id={response_record.id}")
  return response_record


def enable_sse_passthrough(flow: 'MitmproxyHTTPFlow') -> None:
  """Stream SSE to the client without recording chunks."""
  flow.response.stream = True


def finalize_sse_record(flow: 'MitmproxyHTTPFlow', capped: bool = False) -> None:
  response_id = flow.metadata.get(SSE_RESPONSE_ID_KEY)
  if not response_id or flow.metadata.get(SSE_FINALIZED_KEY):
    return

  response = Response.find(response_id)
  if not response:
    return

  status = stream_status.CAPPED if capped or response.stream_status == stream_status.CAPPED else stream_status.COMPLETE
  response.update(stream_status=status)

  # Update request response_hash from chunk payloads (in memory only; raw stays envelope)
  request = response.request
  if request:
    body = sse_body_from_chunks(response)
    request.update(response_hash=RequestHasher.instance().hash_text(body))

  flow.metadata[SSE_FINALIZED_KEY] = True
  Logger.instance(LOG_ID).debug(f"Finalized SSE record response_id={response_id} status={status}")


def sse_body_from_chunks(response: Response) -> bytes:
  chunks = ResponseChunk.where('response_id', response.id).order_by('sequence', 'asc').get()
  return b''.join(chunk.payload or b'' for chunk in chunks)


def _build_tee(flow: 'MitmproxyHTTPFlow', response_id: int) -> Callable[[bytes], List[bytes]]:
  state = {
    'sequence': 0,
    'total_bytes': 0,
    'capped': False,
  }

  def tee(data: bytes) -> List[bytes]:
    if data == b'':
      finalize_sse_record(flow, capped=state['capped'])
      return []

    if not state['capped']:
      next_total = state['total_bytes'] + len(data)
      if state['sequence'] >= MAX_SSE_CHUNKS or next_total > MAX_SSE_BYTES:
        state['capped'] = True
        response = Response.find(response_id)
        if response:
          response.update(stream_status=stream_status.CAPPED)
      else:
        ResponseChunk.create(
          response_id=response_id,
          sequence=state['sequence'],
          payload=data,
        )
        state['sequence'] += 1
        state['total_bytes'] = next_total

    return [data]

  return tee
