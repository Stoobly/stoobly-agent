from typing import TYPE_CHECKING, Callable, List, Optional

if TYPE_CHECKING:
  from mitmproxy.http import HTTPFlow as MitmproxyHTTPFlow

from stoobly_agent.config.constants import stream_status
from stoobly_agent.lib.logger import Logger
# TODO: do not reference ORM directly; go through the DB adapter instead
from stoobly_agent.lib.orm.request import Request
from stoobly_agent.lib.orm.response import Response
from stoobly_agent.lib.orm.response_chunk import ResponseChunk

LOG_ID = 'SSERecord'

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


def start_sse_record(flow: 'MitmproxyHTTPFlow', request_uuid: Optional[str]) -> Optional[Response]:
  """
  After the shared record upload path creates Request + envelope Response, mark
  streaming and tee body chunks into response_chunks (never into Response.raw).

  ``request_uuid`` is the Request.uuid from the local-db create result.
  """
  if flow.metadata.get(SSE_RESPONSE_ID_KEY):
    return Response.find(flow.metadata[SSE_RESPONSE_ID_KEY])

  if not request_uuid:
    Logger.instance(LOG_ID).error('Failed to start SSE record: missing request uuid')
    return None

  request_record = Request.find_by(uuid=request_uuid)
  if not request_record:
    return None

  response_record = request_record.response
  if not response_record:
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

  # response_hash stays the empty-body hash from create: it must align with
  # Response.raw (envelope-only). Chunk payloads are never folded into raw.
  flow.metadata[SSE_FINALIZED_KEY] = True
  Logger.instance(LOG_ID).debug(f"Finalized SSE record response_id={response_id} status={status}")


def sse_body_from_chunks(response: Response) -> bytes:
  chunks = ResponseChunk.where('response_id', response.id).order_by('sequence', 'asc').get()
  return b''.join(chunk.payload or b'' for chunk in chunks)


def split_sse_body(payload: bytes) -> List[bytes]:
  """Split on SSE event boundaries (``\\n\\n``), keeping delimiters with each event."""
  if not payload:
    return []

  events: List[bytes] = []
  start = 0
  while True:
    idx = payload.find(b'\n\n', start)
    if idx < 0:
      rest = payload[start:]
      if rest:
        events.append(rest)
      break
    events.append(payload[start:idx + 2])
    start = idx + 2

  return events if events else [payload]


def replace_response_chunks(response: Response, payload: bytes) -> None:
  """Replace all response_chunks for a streamed response; leave Response.raw alone."""
  from stoobly_agent.lib.orm import ORM

  parts = split_sse_body(payload)
  with ORM.instance().db.transaction():
    for existing in ResponseChunk.where('response_id', response.id).get():
      existing.delete()

    for sequence, part in enumerate(parts):
      ResponseChunk.create(
        response_id=response.id,
        sequence=sequence,
        payload=part,
      )

    response.update(stream_status=stream_status.COMPLETE)


def _build_tee(flow: 'MitmproxyHTTPFlow', response_id: int) -> Callable[[bytes], List[bytes]]:
  state = {
    'sequence': 0,
    'total_bytes': 0,
    'capped': False,
  }

  def _mark_capped(reason: str) -> None:
    state['capped'] = True
    try:
      response = Response.find(response_id)
      if response:
        response.update(stream_status=stream_status.CAPPED)
    except Exception as e:
      Logger.instance(LOG_ID).error(
        f"Failed to mark SSE capped response_id={response_id} reason={reason}: {e}"
      )

  def tee(data: bytes) -> List[bytes]:
    # Always forward to the client; never let DB/persistence failures abort the stream.
    if data == b'':
      try:
        finalize_sse_record(flow, capped=state['capped'])
      except Exception as e:
        Logger.instance(LOG_ID).error(
          f"Failed to finalize SSE record response_id={response_id}: {e}"
        )
      return []

    if not state['capped']:
      next_total = state['total_bytes'] + len(data)
      if state['sequence'] >= MAX_SSE_CHUNKS or next_total > MAX_SSE_BYTES:
        _mark_capped('size_or_count_cap')
      else:
        try:
          # Sync ORM insert on the stream callback: fine for typical SSE rates,
          # but can stall mitmproxy under high-frequency events (up to MAX_SSE_CHUNKS).
          # Follow-up: buffer/flush in batches or persist off the callback thread.
          ResponseChunk.create(
            response_id=response_id,
            sequence=state['sequence'],
            payload=data,
          )
          state['sequence'] += 1
          state['total_bytes'] = next_total
        except Exception as e:
          Logger.instance(LOG_ID).error(
            f"Failed to persist SSE chunk response_id={response_id} "
            f"sequence={state['sequence']}: {e}"
          )
          _mark_capped('persist_error')

    return [data]

  return tee
