import sys

import click

from stoobly_agent.app.cli.helpers.update_request_snapshots_service import update_request_snapshots
from stoobly_agent.app.cli.helpers.handle_replay_service import BODY_FORMAT, JSON_FORMAT
from stoobly_agent.config.data_dir import DataDir
from stoobly_agent.lib.intercepted_requests.simple_logger import SimpleInterceptedRequestsLogger
from stoobly_agent.app.models.factories.resource.local_db.helpers.log_event import DELETE_ACTION, PUT_ACTION, REQUEST_RESOURCE
from stoobly_agent.app.settings import Settings
from stoobly_agent.config.constants import alias_resolve_strategy, test_filter, test_output_level, test_strategy
from stoobly_agent.lib import logger
from stoobly_agent.lib.utils.conditional_decorator import ConditionalDecorator

from .handlers.request_cli_handler import (
  delete_handler, get_handler, list_handler, query_handler, replay_handler, reset_handler, snapshot_handler, test_handler, diff_handler, update_handler, response_update_handler
)
from .helpers.feature_flags import is_local as feature_is_local, is_remote as feature_is_remote
from .helpers.log_options import build_log_filters, log_list_options
from .helpers.print_service import FORMATS, print_snapshots, select_print_options
from .helpers.snapshot_list_service import list_snapshots, snapshot_list_options
from .helpers.validations import *
from .types.request import RequestTestOptions

settings = Settings.instance()
is_remote = feature_is_remote(settings)
is_local = feature_is_local(settings)
log_levels = [logger.DEBUG, logger.INFO, logger.WARNING, logger.ERROR]

@click.group(
  epilog="Run 'stoobly-agent request COMMAND --help' for more information on a command.",
  help="Manage requests"
)
@click.pass_context
def request(ctx):
    pass

@request.command(
  help="Delete a request"
)
@click.argument('request_key')
def delete(**kwargs):
  delete_handler(kwargs)

@request.command(
  help="Show all requests"
)
@click.option('--format', type=click.Choice(FORMATS), help='Format output.')
@click.option('--page', default=0)
@ConditionalDecorator(lambda f: click.option('--project-key')(f), is_remote)
@click.option('--scenario-key')
@click.option('--search', help='Query to filter requests by.')
@click.option('--select', multiple=True, help='Select column(s) to display.')
@click.option('--sort-by', default='created_at', help='created_at|path')
@click.option('--sort-order', default='desc', help='asc | desc')
@click.option('--size', default=10)
@click.option('--without-headers', is_flag=True, default=False, help='Disable printing column headers.')
def list(**kwargs):
  kwargs['is_remote'] = is_remote
  list_handler(kwargs)

@request.command(
  help="Replay a request"
)
@ConditionalDecorator(lambda f: click.option(
    '--alias-resolve-strategy', 
    default=alias_resolve_strategy.NONE, 
    type=click.Choice([alias_resolve_strategy.NONE, alias_resolve_strategy.FIFO, alias_resolve_strategy.LIFO]), 
    help='Strategy for resolving dynamic values for aliases.'
)(f), is_remote)
@ConditionalDecorator(lambda f: click.option('--assign', multiple=True, help='Assign alias values. Format: <NAME>=<VALUE>')(f), is_remote)
@click.option('--format', type=click.Choice([BODY_FORMAT, JSON_FORMAT]), help='Format replay response.')
@click.option('--host', help='Rewrite request host.')
@ConditionalDecorator(lambda f: click.option('--group-by', help='Repeat for each alias name.')(f), is_remote)
@click.option('--lifecycle-hooks-path', help='Path to lifecycle hooks script.')
@click.option(
  '--log-level', default=logger.WARNING, type=click.Choice(log_levels), 
  help=f'''
    Configure which logs to print. Defaults to {logger.WARNING}.
  '''
)
@ConditionalDecorator(
  lambda f: click.option(
    '--overwrite', is_flag=True, default=False, help='Replay request and overwrite existing response.'
  )(f), not is_remote
)
@click.option('--record', is_flag=True, default=False, help='Replay request and record.')
@ConditionalDecorator(lambda f: click.option('--save', is_flag=True, default=False, help='Save results.')(f), is_remote)
@click.option('--scenario-key', help='Record to scenario.')
@click.option('--scheme', type=click.Choice(['http', 'https']), help='Rewrite request scheme.')
@ConditionalDecorator(lambda f: click.option('--trace-id', help='Use existing trace.')(f), is_remote)
@ConditionalDecorator(lambda f: click.option('--validate', multiple=True, help='Validate one or more aliases. Format: <NAME>=?<TYPE>')(f), is_remote)
@click.argument('request_key')
def replay(**kwargs):
  replay_handler(kwargs)

if is_local:
  @request.command(
    help="Update a request"
  )
  @click.option('--body', help='Raw request body.')
  @click.option('--format', type=click.Choice(FORMATS), help='Format output.')
  @click.option('--header', multiple=True, help='Set or delete a header. Format: NAME:VALUE. Empty VALUE deletes the header.')
  @click.option('--host', help='Rewrite request host.')
  @click.option('--method', help='Rewrite request method.')
  @click.option('--path', help='Rewrite request path.')
  @click.option('--port', help='Rewrite request port.')
  @click.option('--scenario-key', is_flag=False, flag_value='', default=None, help='Assign scenario. Pass with no value to clear.')
  @click.option('--scheme', type=click.Choice(['http', 'https']), help='Rewrite request scheme.')
  @click.option('--select', multiple=True, help='Select column(s) to display.')
  @click.option('--url', help='Rewrite request URL.')
  @click.option('--without-headers', is_flag=True, default=False, help='Disable printing column headers.')
  @click.argument('request_key')
  def update(**kwargs):
    update_handler(kwargs)

  @click.group(
    epilog="Run 'stoobly-agent request snapshot COMMAND --help' for more information on a command.",
    help="Manage request snapshots"
  )
  @click.pass_context
  def snapshot(ctx):
    pass

  @snapshot.command(
    name='create',
    help="Create a request snapshot"
  )
  @click.option('--action', default=PUT_ACTION, type=click.Choice([DELETE_ACTION, PUT_ACTION]), help='Sets snapshot action.')
  @click.option('--decode', default=False, is_flag=True, help="Toggles whether to decode response body.")
  @click.option('--lifecycle-hooks-path', help='Path to lifecycle hooks script.')
  @click.option('--no-verify', is_flag=True, default=False)
  @click.argument('request_key')
  def snapshot_create(**kwargs):
    snapshot_path = snapshot_handler(kwargs)

    if snapshot_path is None:
      print("Error: Could not snapshot request", file=sys.stderr)
      sys.exit(1)

    update_request_snapshots(
      action=kwargs['action'],
      file_path=snapshot_path,
      lifecycle_hooks_path=kwargs.get('lifecycle_hooks_path'),
      no_verify=kwargs.get('no_verify', False),
      with_snapshot=False
    )

  @snapshot.command(
    name='reset',
    help="Reset a request to its snapshot state"
  )
  @click.option('--force', default=False, is_flag=True, help="Toggles whether request are hard deleted.")
  @click.argument('request_key')
  def snapshot_reset(**kwargs):
    reset_handler(kwargs)

  @snapshot.command(
    name='diff',
    help="Show diff between current request and its snapshot"
  )
  @click.option('--full', is_flag=True, default=False, help='Show full raw diff.')
  @click.option('--request-key', help='Show diffs only for this request key.')
  def snapshot_diff(**kwargs):
    diff_handler(kwargs)

  @snapshot.command(
    name='list',
    help='List request snapshots'
  )
  @snapshot_list_options
  def snapshot_list(**kwargs):
    print_options = select_print_options(kwargs)
    rows = list_snapshots(
      resource=REQUEST_RESOURCE,
      pending=kwargs.get('pending', False),
      scenario_key=kwargs.get('scenario_key'),
      search=kwargs.get('search'),
      size=kwargs.get('size'),
    )
    if len(rows):
      print_snapshots(rows, **print_options)

  request.add_command(snapshot)

@request.command(
  help="Test a request"
)
@click.option(
    '--alias-resolve-strategy', 
    default=alias_resolve_strategy.NONE, 
    type=click.Choice([alias_resolve_strategy.NONE, alias_resolve_strategy.FIFO, alias_resolve_strategy.LIFO]), 
    help='Strategy for resolving dynamic values for aliases.'
)
@click.option('--aggregate-failures', default=False, is_flag=True, help='Toggles whether to continue execution on failure.')
@click.option('--assign', multiple=True, help='Assign alias values. Format: <NAME>=<VALUE>')
@click.option('--filter', default=test_filter.ALL, type=click.Choice([test_filter.ALL, test_filter.ALIAS, test_filter.LINK]), help='For iterable responses, selectively test properties.')
@click.option('--format', type=click.Choice([BODY_FORMAT, JSON_FORMAT]), help='Format replay response.')
@click.option('--group-by', help='Repeat for each alias name.')
@click.option('--host', help='Rewrite request host.')
@click.option('--lifecycle-hooks-path', help='Path to lifecycle hooks script.')
@click.option('--openapi-specification-path', help='Path to OpenAPI specification file.')
@click.option(
  '--log-level', default=logger.WARNING, type=click.Choice(log_levels), 
  help=f'''
    Configure which logs to print. Defaults to {logger.WARNING}.
  '''
)
@click.option(
  '--output-level', default=test_output_level.PASSED, type=click.Choice([test_output_level.FAILED, test_output_level.SKIPPED, test_output_level.PASSED]),
  help=f'''
    Configure which tests to print. Defaults to {test_output_level.PASSED}.
  '''
)
@click.option('--public-dir-path', help='Path to public files. Used for mocking requests.')
@ConditionalDecorator(lambda f: click.option('--remote-project-key', help='Use remote project for endpoint definitions.')(f), is_local and is_remote)
@ConditionalDecorator(lambda f: click.option('--report-key', help='Save to report.')(f), is_remote)
@click.option('--response-fixtures-path', help='Path to response fixtures yaml. Used for mocking requests.')
@ConditionalDecorator(lambda f: click.option('--save', is_flag=True, default=False, help='Saves test results.')(f), is_remote)
@click.option('--scheme', type=click.Choice(['http', 'https']), help='Rewrite request scheme.')
@click.option('--strategy', default=test_strategy.DIFF, type=click.Choice([test_strategy.CONTRACT, test_strategy.CUSTOM, test_strategy.DIFF, test_strategy.FUZZY]), help='How to test responses.')
@click.option('--trace-id', help='Use existing trace.')
@click.option('--validate', multiple=True, help='Validate one or more aliases. Format: <NAME>=?<TYPE>')
@click.argument('request_key')
def test(**kwargs: RequestTestOptions):
  test_handler(kwargs)

@click.group(
  epilog="Run 'stoobly-agent request response COMMAND --help' for more information on a command.",
  help="Manage request responses"
)
@click.pass_context
def response(ctx):
    pass

@response.command(
  help="Retrieve mocked response"
)
@click.argument('request_key')
def show(**kwargs) -> None:
  get_handler(kwargs)

@response.command(
  help="Query properties in response"
)
@click.option('--query', required=True)
@click.argument('request_key')
def query(**kwargs):
  query_handler(kwargs)

if is_local:
  @response.command(
    name='update',
    help="Update a response"
  )
  @click.option('--body', help='Raw response body.')
  @click.option('--header', multiple=True, help='Set or delete a header. Format: NAME:VALUE. Empty VALUE deletes the header.')
  @click.option('--latency', type=int, help='Response latency in milliseconds.')
  @click.option('--status', type=int, help='HTTP status code.')
  @click.argument('request_key')
  def response_update(**kwargs):
    response_update_handler(kwargs)

@click.group(
  epilog="Run 'stoobly-agent request logs COMMAND --help' for more information on a command.",
  help="Manage intercepted requests logs"
)
@click.pass_context
def log(ctx):
    pass

@log.command(name="path", help="Get intercepted requests log path")
@click.option('--context-dir-path', default=None, help='Path to Stoobly data directory.')
def log_path(**kwargs):
  context_dir_path = kwargs.get('context_dir_path') or DataDir.instance().context_dir_path
  SimpleInterceptedRequestsLogger.get_log_file_path(data_dir_path=context_dir_path)

@log.command(name="list", help="List intercepted requests log entries")
@click.option('--context-dir-path', default=None, help='Path to Stoobly data directory.')
@log_list_options
def log_list(**kwargs):
  context_dir_path = kwargs.get('context_dir_path') or DataDir.instance().context_dir_path
  filters = build_log_filters(kwargs)

  SimpleInterceptedRequestsLogger.dump_logs(
    data_dir_path=context_dir_path,
    filters=filters if filters else None,
    output_format=kwargs.get('format'),
    select=kwargs.get('select'),
    without_headers=kwargs.get('without_headers', False),
    follow=kwargs.get('follow', False),
  )

@log.command(name="delete", help="Delete intercepted requests log entries")
@click.option('--context-dir-path', default=None, help='Path to Stoobly data directory.')
def log_delete(**kwargs):
  context_dir_path = kwargs.get('context_dir_path') or DataDir.instance().context_dir_path
  SimpleInterceptedRequestsLogger.truncate(data_dir_path=context_dir_path)

request.add_command(response)
request.add_command(log, name='logs')
