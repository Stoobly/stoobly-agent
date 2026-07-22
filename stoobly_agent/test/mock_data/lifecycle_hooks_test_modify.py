from stoobly_agent.app.proxy.context import InterceptContext
from stoobly_agent.app.proxy.mock.context import MockContext
from stoobly_agent.app.proxy.replay.context import ReplayContext
from stoobly_agent.app.proxy.test.context import TestContext

# Constants for testing
BEFORE_DEVELOP_REQUEST_HEADER_NAME = 'X-Before-Develop-Request-Header'
BEFORE_DEVELOP_REQUEST_HEADER_VALUE = 'before-develop-request-value'

AFTER_DEVELOP_RESPONSE_HEADER_NAME = 'X-After-Develop-Response-Header'
AFTER_DEVELOP_RESPONSE_HEADER_VALUE = 'after-develop-response-value'

BEFORE_MOCK_REQUEST_HEADER_NAME = 'X-Before-Mock-Request-Header'
BEFORE_MOCK_REQUEST_HEADER_VALUE = 'before-mock-request-value'

AFTER_MOCK_RESPONSE_HEADER_NAME = 'X-After-Mock-Response-Header'
AFTER_MOCK_RESPONSE_HEADER_VALUE = 'after-mock-response-value'

# Markers to verify visibility
BEFORE_DEVELOP_VISIBLE_IN_AFTER_DEVELOP_MARKER = 'before-develop-visible-in-after-develop'
AFTER_DEVELOP_VISIBLE_IN_BEFORE_MOCK_MARKER = 'after-develop-visible-in-before-mock'
AFTER_DEVELOP_VISIBLE_IN_BEFORE_TEST_MARKER = 'after-develop-visible-in-before-test'
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

def handle_before_develop(context: ReplayContext):
  """Modify request in before_develop."""
  context.flow.request.headers[BEFORE_DEVELOP_REQUEST_HEADER_NAME] = BEFORE_DEVELOP_REQUEST_HEADER_VALUE

def handle_after_develop(context: ReplayContext):
  """Verify before_develop changes are visible, and modify response."""
  # Verify before_develop changes are visible
  if context.flow.request.headers.get(BEFORE_DEVELOP_REQUEST_HEADER_NAME) == BEFORE_DEVELOP_REQUEST_HEADER_VALUE:
    print(BEFORE_DEVELOP_VISIBLE_IN_AFTER_DEVELOP_MARKER)
  
  # Modify response
  context.flow.response.headers[AFTER_DEVELOP_RESPONSE_HEADER_NAME] = AFTER_DEVELOP_RESPONSE_HEADER_VALUE

def handle_before_mock(context: MockContext):
  """Verify after_develop changes are visible, and modify request."""
  print(BEFORE_MOCK_CALLED_MARKER)
  # Verify after_develop changes are visible
  response = context.flow.response
  if response and response.headers.get(AFTER_DEVELOP_RESPONSE_HEADER_NAME) == AFTER_DEVELOP_RESPONSE_HEADER_VALUE:
    print(AFTER_DEVELOP_VISIBLE_IN_BEFORE_MOCK_MARKER)
  
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
  """Verify after_develop changes are visible, verify mock changes are NOT visible, and modify request."""
  print(BEFORE_TEST_CALLED_MARKER)
  # Verify after_develop changes are visible
  if context.flow.response.headers.get(AFTER_DEVELOP_RESPONSE_HEADER_NAME) == AFTER_DEVELOP_RESPONSE_HEADER_VALUE:
    print(AFTER_DEVELOP_VISIBLE_IN_BEFORE_TEST_MARKER)
  
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
