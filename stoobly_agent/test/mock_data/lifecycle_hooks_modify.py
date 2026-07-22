from stoobly_agent.app.proxy.context import InterceptContext
from stoobly_agent.app.proxy.record.context import RecordContext
from stoobly_agent.app.proxy.replay.context import ReplayContext

# Constants for testing
BEFORE_DEVELOP_HEADER_NAME = 'X-Before-Develop-Header'
BEFORE_DEVELOP_HEADER_VALUE = 'before-develop-value'

AFTER_DEVELOP_HEADER_NAME = 'X-After-Develop-Header'
AFTER_DEVELOP_HEADER_VALUE = 'after-develop-value'

BEFORE_RECORD_HEADER_NAME = 'X-Before-Record-Header'
BEFORE_RECORD_HEADER_VALUE = 'before-record-value'

AFTER_RECORD_RESPONSE_HEADER_NAME = 'X-After-Record-Response-Header'
AFTER_RECORD_RESPONSE_HEADER_VALUE = 'after-record-response-value'

# Header to verify before_record changes persist to before_response
BEFORE_RESPONSE_VERIFIED_HEADER_NAME = 'X-Before-Response-Verified'
BEFORE_RESPONSE_VERIFIED_HEADER_VALUE = 'before-record-persisted'

# Markers to verify develop changes are visible in before_record
BEFORE_DEVELOP_VISIBLE_IN_BEFORE_RECORD_MARKER = 'before-develop-visible-in-before-record'
AFTER_DEVELOP_VISIBLE_IN_BEFORE_RECORD_MARKER = 'after-develop-visible-in-before-record'

def handle_before_request(context: InterceptContext):
  pass

def handle_before_develop(context: ReplayContext):
  """Modify outbound request before it's sent to upstream service."""
  context.flow.request.headers[BEFORE_DEVELOP_HEADER_NAME] = BEFORE_DEVELOP_HEADER_VALUE

def handle_after_develop(context: ReplayContext):
  """Modify response after it's received from upstream service."""
  context.flow.response.headers[AFTER_DEVELOP_HEADER_NAME] = AFTER_DEVELOP_HEADER_VALUE

def handle_before_record(context: RecordContext):
  """Modify request before it's stored."""
  # Add our own header
  context.flow.request.headers[BEFORE_RECORD_HEADER_NAME] = BEFORE_RECORD_HEADER_VALUE
  
  # Verify that before_develop changes are visible
  if context.flow.request.headers.get(BEFORE_DEVELOP_HEADER_NAME) == BEFORE_DEVELOP_HEADER_VALUE:
    print(BEFORE_DEVELOP_VISIBLE_IN_BEFORE_RECORD_MARKER)
  
  # Verify that after_develop changes are visible
  if context.flow.response.headers.get(AFTER_DEVELOP_HEADER_NAME) == AFTER_DEVELOP_HEADER_VALUE:
    print(AFTER_DEVELOP_VISIBLE_IN_BEFORE_RECORD_MARKER)

def handle_after_record(context: RecordContext):
  """Modify response after it's stored (for testing purposes)."""
  # Note: Modifications here won't affect stored data, but we can add a header to verify hook was called
  context.flow.response.headers[AFTER_RECORD_RESPONSE_HEADER_NAME] = AFTER_RECORD_RESPONSE_HEADER_VALUE

AFTER_DEVELOP_PERSISTS_MARKER = 'after-develop-persisted-to-before-response'

def handle_before_response(context: InterceptContext):
  """Verify which changes persist and are visible here."""
  # Check if the before_record header is present on the request
  # (It should NOT be, since before_record operates on a deep copy)
  if context.flow.request.headers.get(BEFORE_RECORD_HEADER_NAME) == BEFORE_RECORD_HEADER_VALUE:
    # Print to stdout to indicate the verification passed (can be checked in test)
    print(BEFORE_RESPONSE_VERIFIED_HEADER_VALUE)
    # Also set a header on the response (visible in returned response, not stored)
    context.flow.response.headers[BEFORE_RESPONSE_VERIFIED_HEADER_NAME] = BEFORE_RESPONSE_VERIFIED_HEADER_VALUE
  
  # Check if the after_develop header is present on the response
  # (It SHOULD be, since after_develop operates on the original flow)
  if context.flow.response.headers.get(AFTER_DEVELOP_HEADER_NAME) == AFTER_DEVELOP_HEADER_VALUE:
    print(AFTER_DEVELOP_PERSISTS_MARKER)
