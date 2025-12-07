from stoobly_agent.app.proxy.context import InterceptContext
from stoobly_agent.app.proxy.mock.context import MockContext
from stoobly_agent.app.proxy.replay.context import ReplayContext
from stoobly_agent.app.proxy.test.context import TestContext

# Constants for testing
BEFORE_REPLAY_REQUEST_HEADER_NAME = 'X-Before-Replay-Request-Header'
BEFORE_REPLAY_REQUEST_HEADER_VALUE = 'before-replay-request-value'

AFTER_REPLAY_RESPONSE_HEADER_NAME = 'X-After-Replay-Response-Header'
AFTER_REPLAY_RESPONSE_HEADER_VALUE = 'after-replay-response-value'

BEFORE_MOCK_REQUEST_HEADER_NAME = 'X-Before-Mock-Request-Header'
BEFORE_MOCK_REQUEST_HEADER_VALUE = 'before-mock-request-value'

AFTER_MOCK_RESPONSE_HEADER_NAME = 'X-After-Mock-Response-Header'
AFTER_MOCK_RESPONSE_HEADER_VALUE = 'after-mock-response-value'

# Markers to verify visibility
BEFORE_REPLAY_VISIBLE_IN_AFTER_REPLAY_MARKER = 'before-replay-visible-in-after-replay'
AFTER_REPLAY_VISIBLE_IN_BEFORE_MOCK_MARKER = 'after-replay-visible-in-before-mock'
AFTER_REPLAY_VISIBLE_IN_BEFORE_TEST_MARKER = 'after-replay-visible-in-before-test'
BEFORE_MOCK_VISIBLE_IN_AFTER_MOCK_MARKER = 'before-mock-visible-in-after-mock'
BEFORE_MOCK_NOT_VISIBLE_IN_BEFORE_TEST_MARKER = 'before-mock-not-visible-in-before-test'
AFTER_MOCK_NOT_VISIBLE_IN_BEFORE_TEST_MARKER = 'after-mock-not-visible-in-before-test'

BEFORE_TEST_REQUEST_HEADER_NAME = 'X-Before-Test-Request-Header'
BEFORE_TEST_REQUEST_HEADER_VALUE = 'before-test-request-value'

BEFORE_TEST_VISIBLE_IN_AFTER_TEST_MARKER = 'before-test-visible-in-after-test'

def handle_before_request(context: InterceptContext):
  pass

def handle_before_replay(context: ReplayContext):
  """Modify request in before_replay."""
  context.flow.request.headers[BEFORE_REPLAY_REQUEST_HEADER_NAME] = BEFORE_REPLAY_REQUEST_HEADER_VALUE

def handle_after_replay(context: ReplayContext):
  """Verify before_replay changes are visible, and modify response."""
  # Verify before_replay changes are visible
  if context.flow.request.headers.get(BEFORE_REPLAY_REQUEST_HEADER_NAME) == BEFORE_REPLAY_REQUEST_HEADER_VALUE:
    print(BEFORE_REPLAY_VISIBLE_IN_AFTER_REPLAY_MARKER)
  
  # Modify response
  context.flow.response.headers[AFTER_REPLAY_RESPONSE_HEADER_NAME] = AFTER_REPLAY_RESPONSE_HEADER_VALUE

def handle_before_mock(context: MockContext):
  """Verify after_replay changes are visible, and modify request."""
  # Verify after_replay changes are visible
  if context.flow.response.headers.get(AFTER_REPLAY_RESPONSE_HEADER_NAME) == AFTER_REPLAY_RESPONSE_HEADER_VALUE:
    print(AFTER_REPLAY_VISIBLE_IN_BEFORE_MOCK_MARKER)
  
  # Modify request
  context.flow.request.headers[BEFORE_MOCK_REQUEST_HEADER_NAME] = BEFORE_MOCK_REQUEST_HEADER_VALUE

def handle_after_mock(context: MockContext):
  """Verify before_mock changes are visible, and modify response."""
  # Verify before_mock changes are visible
  if context.flow.request.headers.get(BEFORE_MOCK_REQUEST_HEADER_NAME) == BEFORE_MOCK_REQUEST_HEADER_VALUE:
    print(BEFORE_MOCK_VISIBLE_IN_AFTER_MOCK_MARKER)
  
  # Modify response
  context.flow.response.headers[AFTER_MOCK_RESPONSE_HEADER_NAME] = AFTER_MOCK_RESPONSE_HEADER_VALUE

def handle_before_test(context: TestContext):
  """Verify after_replay changes are visible, verify mock changes are NOT visible, and modify request."""
  # Verify after_replay changes are visible
  if context.flow.response.headers.get(AFTER_REPLAY_RESPONSE_HEADER_NAME) == AFTER_REPLAY_RESPONSE_HEADER_VALUE:
    print(AFTER_REPLAY_VISIBLE_IN_BEFORE_TEST_MARKER)
  
  # Verify before_mock changes are NOT visible (mock operates on a copy)
  if context.flow.request.headers.get(BEFORE_MOCK_REQUEST_HEADER_NAME) != BEFORE_MOCK_REQUEST_HEADER_VALUE:
    print(BEFORE_MOCK_NOT_VISIBLE_IN_BEFORE_TEST_MARKER)
  
  # Verify after_mock changes are NOT visible (mock operates on a copy)
  if context.flow.response.headers.get(AFTER_MOCK_RESPONSE_HEADER_NAME) != AFTER_MOCK_RESPONSE_HEADER_VALUE:
    print(AFTER_MOCK_NOT_VISIBLE_IN_BEFORE_TEST_MARKER)
  
  # Modify request
  context.flow.request.headers[BEFORE_TEST_REQUEST_HEADER_NAME] = BEFORE_TEST_REQUEST_HEADER_VALUE

def handle_after_test(context: TestContext):
  """Verify before_test changes are visible."""
  # Verify before_test changes are visible
  if context.flow.request.headers.get(BEFORE_TEST_REQUEST_HEADER_NAME) == BEFORE_TEST_REQUEST_HEADER_VALUE:
    print(BEFORE_TEST_VISIBLE_IN_AFTER_TEST_MARKER)

def handle_before_response(context: InterceptContext):
  pass

