import pdb
import sys

from typing import TypedDict

from stoobly_agent.app.cli.helpers.test_facade import TestFacade
from stoobly_agent.app.cli.helpers.context import ReplayContext
from stoobly_agent.lib.api.interfaces.tests import TestShowResponse
from stoobly_agent.lib.logger import bcolors

class SessionContext(TypedDict):
  aggregate_failures: bool 
  passed: int
  project_id: int
  test_facade: TestFacade
  total: int

def print_request(context: ReplayContext, additional: str = ''):
  response = context.response

  seconds = context.end_time - context.start_time
  ms = round(seconds * 1000)

  print(response.content)
  print(f"Completed {response.status_code} in {ms}ms{additional}")

def print_test(context: ReplayContext, res: TestShowResponse):
  if not res:
    print_request(context)
    print("\nTest failed to run")
  else:
    print_request(context, f" (Expected {res['expected_latency']}ms)")

    if not res['passed']:
      passed_message = f"{bcolors.FAIL}failed{bcolors.ENDC}"
    else:
      passed_message = f"{bcolors.OKGREEN}passed{bcolors.ENDC}"

    print(f"\nTest {passed_message} using {bcolors.BOLD}{res['strategy']}{bcolors.ENDC} strategy")
    print(res['log'])

def __get_test_response_with_context(context: ReplayContext, project_id: str, test_facade: TestFacade):
  try:
    res = test_facade.show_with_context(context, project_id)
    return res
  except AssertionError as e:
    return print(e, file=sys.stderr)

def handle_on_test_response(context: ReplayContext, session_context: SessionContext):
  project_id = session_context['project_id']
  test_facade = session_context['test_facade']
  res = __get_test_response_with_context(context, project_id, test_facade)

  passed = res['passed'] if res else False
  session_context['passed'] += (1 if passed else 0)
  session_context['total'] += 1

  print_test(context, res)

def exit_on_failure(session_context: SessionContext):
  if session_context['passed'] != session_context['total']:
    sys.exit(1)