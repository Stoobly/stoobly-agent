from stoobly_agent.app.proxy.context import InterceptContext
from stoobly_agent.app.proxy.record.context import RecordContext
from stoobly_agent.app.proxy.replay.context import ReplayContext

# Constants for testing
BEFORE_REPLAY_HEADER_NAME = 'X-Before-Replay-Header'
BEFORE_REPLAY_HEADER_VALUE = 'before-replay-value'

AFTER_REPLAY_HEADER_NAME = 'X-After-Replay-Header'
AFTER_REPLAY_HEADER_VALUE = 'after-replay-value'

BEFORE_RECORD_HEADER_NAME = 'X-Before-Record-Header'
BEFORE_RECORD_HEADER_VALUE = 'before-record-value'

AFTER_RECORD_RESPONSE_HEADER_NAME = 'X-After-Record-Response-Header'
AFTER_RECORD_RESPONSE_HEADER_VALUE = 'after-record-response-value'

# Header to verify before_record changes persist to before_response
BEFORE_RESPONSE_VERIFIED_HEADER_NAME = 'X-Before-Response-Verified'
BEFORE_RESPONSE_VERIFIED_HEADER_VALUE = 'before-record-persisted'

# Markers to verify replay changes are visible in before_record
BEFORE_REPLAY_VISIBLE_IN_BEFORE_RECORD_MARKER = 'before-replay-visible-in-before-record'
AFTER_REPLAY_VISIBLE_IN_BEFORE_RECORD_MARKER = 'after-replay-visible-in-before-record'

def handle_before_request(context: InterceptContext):
  pass

def handle_before_replay(context: ReplayContext):
  """Modify outbound request before it's sent to upstream service."""
  context.flow.request.headers[BEFORE_REPLAY_HEADER_NAME] = BEFORE_REPLAY_HEADER_VALUE

def handle_after_replay(context: ReplayContext):
  """Modify response after it's received from upstream service."""
  context.flow.response.headers[AFTER_REPLAY_HEADER_NAME] = AFTER_REPLAY_HEADER_VALUE

def handle_before_record(context: RecordContext):
  """Modify request before it's stored."""
  # Add our own header
  context.flow.request.headers[BEFORE_RECORD_HEADER_NAME] = BEFORE_RECORD_HEADER_VALUE
  
  # Verify that before_replay changes are visible
  if context.flow.request.headers.get(BEFORE_REPLAY_HEADER_NAME) == BEFORE_REPLAY_HEADER_VALUE:
    print(BEFORE_REPLAY_VISIBLE_IN_BEFORE_RECORD_MARKER)
  
  # Verify that after_replay changes are visible
  if context.flow.response.headers.get(AFTER_REPLAY_HEADER_NAME) == AFTER_REPLAY_HEADER_VALUE:
    print(AFTER_REPLAY_VISIBLE_IN_BEFORE_RECORD_MARKER)

def handle_after_record(context: RecordContext):
  """Modify response after it's stored (for testing purposes)."""
  # Note: Modifications here won't affect stored data, but we can add a header to verify hook was called
  context.flow.response.headers[AFTER_RECORD_RESPONSE_HEADER_NAME] = AFTER_RECORD_RESPONSE_HEADER_VALUE

AFTER_REPLAY_PERSISTS_MARKER = 'after-replay-persisted-to-before-response'

def handle_before_response(context: InterceptContext):
  """Verify which changes persist and are visible here."""
  # Check if the before_record header is present on the request
  # (It should NOT be, since before_record operates on a deep copy)
  if context.flow.request.headers.get(BEFORE_RECORD_HEADER_NAME) == BEFORE_RECORD_HEADER_VALUE:
    # Print to stdout to indicate the verification passed (can be checked in test)
    print(BEFORE_RESPONSE_VERIFIED_HEADER_VALUE)
    # Also set a header on the response (visible in returned response, not stored)
    context.flow.response.headers[BEFORE_RESPONSE_VERIFIED_HEADER_NAME] = BEFORE_RESPONSE_VERIFIED_HEADER_VALUE
  
  # Check if the after_replay header is present on the response
  # (It SHOULD be, since after_replay operates on the original flow)
  if context.flow.response.headers.get(AFTER_REPLAY_HEADER_NAME) == AFTER_REPLAY_HEADER_VALUE:
    print(AFTER_REPLAY_PERSISTS_MARKER)

