from stoobly_agent.app.proxy.context import InterceptContext
from stoobly_agent.app.proxy.mock.context import MockContext
from stoobly_agent.app.proxy.record.context import RecordContext
from stoobly_agent.app.proxy.replay.context import ReplayContext
from stoobly_agent.app.proxy.test.context import TestContext

def handle_before_request(context: InterceptContext):
  print('before_request')

def handle_before_record(context: RecordContext):
  print('before_record')

def handle_before_mock(context: MockContext):
  print('before_mock')

def handle_before_replay(context: ReplayContext):
  print('before_replay')

def handle_before_test(context: ReplayContext):
  print('before_test')

def handle_after_record(context: RecordContext):
  print('after_record')

def handle_after_mock(context: MockContext):
  print('after_mock')

def handle_after_replay(context: ReplayContext):
  print('after_replay')

def handle_after_test(context: TestContext):
  print('after_test')

def handle_before_response(context: InterceptContext):
  print('before_response')