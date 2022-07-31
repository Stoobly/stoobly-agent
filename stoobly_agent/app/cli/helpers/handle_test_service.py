import json
import pdb
import requests
import sys

from typing import Callable, TypedDict, Union

from stoobly_agent.app.cli.helpers.handle_replay_service import JSON_FORMAT, print_request
from stoobly_agent.app.cli.helpers.test_facade import TestFacade
from stoobly_agent.app.cli.helpers.context import ReplayContext
from stoobly_agent.lib.api.interfaces.tests import TestShowResponse
from stoobly_agent.lib.logger import bcolors

class SessionContext(TypedDict):
  aggregate_failures: bool 
  passed: int
  output: dict
  project_id: int
  test_facade: TestFacade
  total: int

def handle_test_session_complete(session_context: SessionContext, format = None):
  format_handler = __default_session_complete_formatter

  if format == JSON_FORMAT:
    format_handler = __json_session_complete_formatter

  format_handler(session_context)

def handle_test_complete(
  context: ReplayContext, session_context: SessionContext, format = None
):
  format_handler = __default_test_complete_formatter
  if format == JSON_FORMAT:
    format_handler = __json_test_complete_formatter

  project_id = session_context['project_id']
  test_facade = session_context['test_facade']
  test = __get_test_response_with_context(context, project_id, test_facade)

  passed = bool(test.get('passed')) if isinstance(test, dict) else False
  session_context['passed'] += (1 if passed else 0)
  session_context['total'] += 1

  format_handler(context, session_context, test)

def exit_on_failure(session_context: SessionContext, complete = True):
  if session_context['passed'] != session_context['total']:
    if not complete:
      handle_test_session_complete(session_context)

    sys.exit(1)

def __json_test_complete_formatter(context: ReplayContext, session_context: SessionContext, res: TestShowResponse):
  if 'output' not in session_context:
    session_context['output'] = {}

  output = session_context['output']
  if not res:
    output['error'] = 'Test failed to run'
  elif isinstance(res, str):
    output['error'] = res
  else:
    if 'tests' not in output:
      output['tests'] = []

    seconds = context.end_time - context.start_time
    latency = round(seconds * 1000)
    test = {
      'log': res['log'] if 'log' in res else '',
      'passed': res['passed'],
      'response': { **__build_json_response(context.response), 'latency': latency} 
    }

    if not res['passed']:
      project_id = session_context['project_id']
      test_facade = session_context['test_facade']
      expected_response = __get_test_expected_response_with_context(context, project_id, test_facade)

      if expected_response:
        test['expected_response'] = { **__build_json_response(expected_response), 'latency': res['expected_latency']}

    output['tests'].append(test)

def __default_test_complete_formatter(context: ReplayContext, session_context: SessionContext, res: TestShowResponse):
  if not res:
    print_request(context)
    print("\nTest failed to run")
  elif isinstance(res, str):
    print(res, file=sys.stderr)
  else:
    print_request(context)

    if not res['passed']:
      passed_message = f"{bcolors.FAIL}failed{bcolors.ENDC}"
    else:
      passed_message = f"{bcolors.OKGREEN}passed{bcolors.ENDC}"

    print(f"\nTest {passed_message} using {bcolors.BOLD}{res['strategy']}{bcolors.ENDC} strategy")
    
    if res['log']:
      print(res['log'])

    if not res['passed']:
      project_id = session_context['project_id']
      test_facade = session_context['test_facade']
      expected_response = __get_test_expected_response_with_context(context, project_id, test_facade)

      if expected_response:
        print(f"\n{bcolors.BOLD}Expected Response{bcolors.ENDC}")
        print(expected_response.content.decode())
        print(f"Completed {expected_response.status_code} in {res['expected_latency']}ms")

def __default_session_complete_formatter(session_context: SessionContext):
  if 'output' in session_context:
    print(session_context['output'])

  passed = session_context['passed']
  total = session_context['total']

  if total > 1:
    if passed == total:
      print(f"\n{passed} / {total} {bcolors.OKGREEN}passed{bcolors.ENDC}")
    else:
      print(f"\n{passed} / {total} {bcolors.OKGREEN}passed{bcolors.ENDC} {total - passed} {bcolors.FAIL}failed{bcolors.ENDC}")

def __json_session_complete_formatter(session_context: SessionContext):
  if 'output' not in session_context:
    return

  session_context['output']['passed'] = session_context['passed']
  session_context['output']['total'] = session_context['total']
  print(json.dumps(session_context['output']))

def __get_test_response_with_context(context: ReplayContext, project_id: str, test_facade: TestFacade) -> Union[requests.Response, str]:
  try:
    res = test_facade.show_with_context(context, project_id)
    return res
  except AssertionError as e:
    return f"API Error: {e}"

def __get_test_expected_response_with_context(context: ReplayContext, project_id: str, test_facade: TestFacade) -> Union[requests.Response, str]:
  try:
    res = test_facade.expected_response_with_context(context, project_id)
    return res
  except AssertionError as e:
    return f"API Error: {e}"

def __build_json_response(response: requests.Response):
  return {
    'content': response.content.decode(),
    'status_code': response.status_code,
  }