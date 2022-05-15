import sys

from stoobly_agent.app.cli.helpers.test_facade import TestFacade
from stoobly_agent.app.proxy.replay.context import ReplayContext
from stoobly_agent.app.settings import Settings
from stoobly_agent.config.constants import custom_headers
from stoobly_agent.lib.api.keys.test_key import TestKey

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

def handle_on_request_response(context: ReplayContext):
    response = context.response

    seconds = context.end_time - context.start_time
    ms = round(seconds * 1000)

    print(response.content)
    print(f"Completed {response.status_code} in {ms}ms")

def handle_on_test_response(context: ReplayContext, project_id: str,  settings: Settings):
    handle_on_request_response(context)

    facade = TestFacade(settings)

    try:
        res = facade.show_with_context(context, project_id)
    except AssertionError as e:
        return print(e, file=sys.stderr)

    if res:
        print("\nTest Results:")
        print_tests([res])