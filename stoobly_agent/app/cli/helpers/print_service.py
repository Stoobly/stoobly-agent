import sys

from stoobly_agent.app.cli.helpers.test_facade import TestFacade
from stoobly_agent.app.proxy.replay.context import ReplayContext
from stoobly_agent.app.settings import Settings
from stoobly_agent.lib.logger import bcolors

from .tabulate_print_service import tabulate_print

def select_print_options(kwargs):
    print_options = {
        'select': kwargs['select'],
        'without_headers': kwargs['without_headers']
    }

    del kwargs['without_headers']
    del kwargs['select']

    return print_options

def print_tests(requests, **kwargs):
    tabulate_print(
      requests, 
      filter=['created_at', 'id', 'log', 'position', 'project_id', 'report_id', 'scenario_id', 'starred', 'updated_at'],
      headers=not kwargs.get('without_headers'),
      select=kwargs.get('select') or []
    )

def handle_on_request_response(context: ReplayContext, additional: str = ''):
    response = context.response

    seconds = context.end_time - context.start_time
    ms = round(seconds * 1000)

    print(response.content)
    print(f"Completed {response.status_code} in {ms}ms{additional}")

def handle_on_test_response(context: ReplayContext, project_id: str,  settings: Settings):
    facade = TestFacade(settings)

    try:
        res = facade.show_with_context(context, project_id)
    except AssertionError as e:
        return print(e, file=sys.stderr)

    if not res:
        handle_on_request_response(context)
        print("\nTest failed to run")
    else:
        handle_on_request_response(context, f" (Expected {res['expected_latency']}ms)")

        if not res['passed']:
            passed_message = f"{bcolors.FAIL}failed{bcolors.ENDC}"
        else:
            passed_message = f"{bcolors.OKGREEN}passed{bcolors.ENDC}"

        print(f"\nTest {passed_message} using {bcolors.BOLD}{res['strategy']}{bcolors.ENDC} strategy")
        print(res['log'])