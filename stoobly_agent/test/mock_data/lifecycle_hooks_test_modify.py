from stoobly_agent.app.proxy.context import InterceptContext
from stoobly_agent.app.proxy.mock.context import MockContext
from stoobly_agent.app.proxy.replay.context import ReplayContext
from stoobly_agent.app.proxy.test.context import TestContext

# Constants for testing
BEFORE_NORMALIZE_REQUEST_HEADER_NAME = 'X-Before-Normalize-Request-Header'
BEFORE_NORMALIZE_REQUEST_HEADER_VALUE = 'before-normalize-request-value'

AFTER_NORMALIZE_RESPONSE_HEADER_NAME = 'X-After-Normalize-Response-Header'
AFTER_NORMALIZE_RESPONSE_HEADER_VALUE = 'after-normalize-response-value'

BEFORE_MOCK_REQUEST_HEADER_NAME = 'X-Before-Mock-Request-Header'
BEFORE_MOCK_REQUEST_HEADER_VALUE = 'before-mock-request-value'

AFTER_MOCK_RESPONSE_HEADER_NAME = 'X-After-Mock-Response-Header'
AFTER_MOCK_RESPONSE_HEADER_VALUE = 'after-mock-response-value'

# Markers to verify visibility
BEFORE_NORMALIZE_VISIBLE_IN_AFTER_NORMALIZE_MARKER = 'before-normalize-visible-in-after-normalize'
AFTER_NORMALIZE_VISIBLE_IN_BEFORE_MOCK_MARKER = 'after-normalize-visible-in-before-mock'
AFTER_NORMALIZE_VISIBLE_IN_BEFORE_TEST_MARKER = 'after-normalize-visible-in-before-test'
BEFORE_MOCK_VISIBLE_IN_AFTER_MOCK_MARKER = 'before-mock-visible-in-after-mock'
BEFORE_MOCK_NOT_VISIBLE_IN_BEFORE_TEST_MARKER = 'before-mock-not-visible-in-before-test'
AFTER_MOCK_NOT_VISIBLE_IN_BEFORE_TEST_MARKER = 'after-mock-not-visible-in-before-test'

BEFORE_TEST_REQUEST_HEADER_NAME = 'X-Before-Test-Request-Header'
BEFORE_TEST_REQUEST_HEADER_VALUE = 'before-test-request-value'

BEFORE_TEST_VISIBLE_IN_AFTER_TEST_MARKER = 'before-test-visible-in-after-test'
BEFORE_REQUEST_CALLED_MARKER = 'before-request-called'
BEFORE_MOCK_CALLED_MARKER = 'before-mock-called'
AFTER_MOCK_CALLED_MARKER = 'after-mock-called'
BEFORE_TEST_CALLED_MARKER = 'before-test-called'
AFTER_TEST_CALLED_MARKER = 'after-test-called'
BEFORE_RESPONSE_CALLED_MARKER = 'before-response-called'

def handle_before_request(context: InterceptContext):
  print(BEFORE_REQUEST_CALLED_MARKER)

def handle_before_normalize(context: ReplayContext):
  """Modify request in before_normalize."""
  context.flow.request.headers[BEFORE_NORMALIZE_REQUEST_HEADER_NAME] = BEFORE_NORMALIZE_REQUEST_HEADER_VALUE

def handle_after_normalize(context: ReplayContext):
  """Verify before_normalize changes are visible, and modify response."""
  # Verify before_normalize changes are visible
  if context.flow.request.headers.get(BEFORE_NORMALIZE_REQUEST_HEADER_NAME) == BEFORE_NORMALIZE_REQUEST_HEADER_VALUE:
    print(BEFORE_NORMALIZE_VISIBLE_IN_AFTER_NORMALIZE_MARKER)
  
  # Modify response
  context.flow.response.headers[AFTER_NORMALIZE_RESPONSE_HEADER_NAME] = AFTER_NORMALIZE_RESPONSE_HEADER_VALUE

def handle_before_mock(context: MockContext):
  """Verify after_normalize changes are visible, and modify request."""
  print(BEFORE_MOCK_CALLED_MARKER)
  # Verify after_normalize changes are visible
  response = context.flow.response
  if response and response.headers.get(AFTER_NORMALIZE_RESPONSE_HEADER_NAME) == AFTER_NORMALIZE_RESPONSE_HEADER_VALUE:
    print(AFTER_NORMALIZE_VISIBLE_IN_BEFORE_MOCK_MARKER)
  
  # Modify request
  context.flow.request.headers[BEFORE_MOCK_REQUEST_HEADER_NAME] = BEFORE_MOCK_REQUEST_HEADER_VALUE

def handle_after_mock(context: MockContext):
  """Verify before_mock changes are visible, and modify response."""
  print(AFTER_MOCK_CALLED_MARKER)
  # Verify before_mock changes are visible
  if context.flow.request.headers.get(BEFORE_MOCK_REQUEST_HEADER_NAME) == BEFORE_MOCK_REQUEST_HEADER_VALUE:
    print(BEFORE_MOCK_VISIBLE_IN_AFTER_MOCK_MARKER)
  
  # Modify response
  context.flow.response.headers[AFTER_MOCK_RESPONSE_HEADER_NAME] = AFTER_MOCK_RESPONSE_HEADER_VALUE

def handle_before_test(context: TestContext):
  """Verify after_normalize changes are visible, verify mock changes are NOT visible, and modify request."""
  print(BEFORE_TEST_CALLED_MARKER)
  # Verify after_normalize changes are visible
  if context.flow.response.headers.get(AFTER_NORMALIZE_RESPONSE_HEADER_NAME) == AFTER_NORMALIZE_RESPONSE_HEADER_VALUE:
    print(AFTER_NORMALIZE_VISIBLE_IN_BEFORE_TEST_MARKER)
  
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
  print(AFTER_TEST_CALLED_MARKER)
  # Verify before_test changes are visible
  if context.flow.request.headers.get(BEFORE_TEST_REQUEST_HEADER_NAME) == BEFORE_TEST_REQUEST_HEADER_VALUE:
    print(BEFORE_TEST_VISIBLE_IN_AFTER_TEST_MARKER)

def handle_before_response(context: InterceptContext):
  print(BEFORE_RESPONSE_CALLED_MARKER)
