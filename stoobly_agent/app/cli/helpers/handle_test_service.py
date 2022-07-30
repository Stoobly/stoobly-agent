import pdb
import sys

from typing import TypedDict

import requests

from stoobly_agent.app.cli.helpers.handle_replay_service import default_format_handler, print_request
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

def print_test(res: TestShowResponse, context: ReplayContext):
  if not res:
    print_request(context)
    print("\nTest failed to run")
  else:
    print_request(context, lambda context: default_format_handler(context, f" (Expected {res['expected_latency']}ms)"))

    if not res['passed']:
      passed_message = f"{bcolors.FAIL}failed{bcolors.ENDC}"
    else:
      passed_message = f"{bcolors.OKGREEN}passed{bcolors.ENDC}"

    print(f"\nTest {passed_message} using {bcolors.BOLD}{res['strategy']}{bcolors.ENDC} strategy")
    
    if res['log']:
      print(res['log'])

def print_expectation(res: requests.Response):
  if not res:
    return
  
  print("\nExpected Response")
  print(res.content.decode())

def handle_on_test_response(context: ReplayContext, session_context: SessionContext):
  project_id = session_context['project_id']
  test_facade = session_context['test_facade']

  test = __get_test_response_with_context(context, project_id, test_facade)

  passed = test['passed'] if test else False
  session_context['passed'] += (1 if passed else 0)
  session_context['total'] += 1

  print_test(test, context)

  if not passed:
    expected_response = __get_test_expected_response_with_context(context, project_id, test_facade)
    print_expectation(expected_response)

def exit_on_failure(session_context: SessionContext):
  if session_context['passed'] != session_context['total']:
    sys.exit(1)

def __get_test_response_with_context(context: ReplayContext, project_id: str, test_facade: TestFacade):
  try:
    res = test_facade.show_with_context(context, project_id)
    return res
  except AssertionError as e:
    return print(f"API Error: {e}", file=sys.stderr)

def __get_test_expected_response_with_context(context: ReplayContext, project_id: str, test_facade: TestFacade):
  try:
    res = test_facade.expected_response_with_context(context, project_id)
    return res
  except AssertionError as e:
    return print(f"API Error: {e}", file=sys.stderr)