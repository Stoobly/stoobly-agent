import click

from stoobly_agent.app.cli.helpers.handle_replay_service import BODY_FORMAT, JSON_FORMAT
from stoobly_agent.config.data_dir import DataDir
from stoobly_agent.lib.intercepted_requests.simple_logger import SimpleInterceptedRequestsLogger
from stoobly_agent.app.models.factories.resource.local_db.helpers.log_event import DELETE_ACTION, PUT_ACTION
from stoobly_agent.app.settings import Settings
from stoobly_agent.config.constants import alias_resolve_strategy, test_filter, test_output_level, test_strategy
from stoobly_agent.lib import logger
from stoobly_agent.lib.utils.conditional_decorator import ConditionalDecorator

from .handlers.request_cli_handler import (
  delete_handler, get_handler, list_handler, query_handler, replay_handler, reset_handler, snapshot_handler, test_handler
)
from .helpers.feature_flags import local, remote
from .helpers.print_service import FORMATS
from .helpers.validations import *
from .types.request import RequestTestOptions

settings = Settings.instance()
is_remote = remote(settings)
is_local = local(settings)
log_levels = [logger.DEBUG, logger.INFO, logger.WARNING, logger.ERROR]

@click.group(
  epilog="Run 'stoobly-agent request COMMAND --help' for more information on a command.",
  help="Manage requests"
)
@click.pass_context
def request(ctx):
    pass

@request.command(
  help="Delete recorded request"
)
@click.argument('request_key')
def delete(**kwargs):
  delete_handler(kwargs)

@request.command(
  help="Show recorded requests"
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
    help="Snapshot a request"
  )
  @click.option('--action', default=PUT_ACTION, type=click.Choice([DELETE_ACTION, PUT_ACTION]), help='Sets snapshot action.')
  @click.option('--decode', default=False, is_flag=True, help="Toggles whether to decode response body.")
  @click.argument('request_key')
  def snapshot(**kwargs):
    snapshot_handler(kwargs)

  @request.command(
      help="Reset a request to its snapshot state"
  )
  @click.option('--force', default=False, is_flag=True, help="Toggles whether request are hard deleted.")
  @click.argument('request_key')
  def reset(**kwargs):
    reset_handler(kwargs)

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
@click.option('--public-directory-path', multiple=True, help='Path to public files. Used for mocking requests. Can take the form <FOLDER-PATH>[:<ORIGIN>].')
@ConditionalDecorator(lambda f: click.option('--remote-project-key', help='Use remote project for endpoint definitions.')(f), is_remote and is_local)
@ConditionalDecorator(lambda f: click.option('--report-key', help='Save to report.')(f), is_remote)
@click.option('--response-fixtures-path', multiple=True, help='Path to response fixtures yaml. Used for mocking requests. Can take the form <FILE-PATH>[:<ORIGIN>].')
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
def get(**kwargs) -> None:
  get_handler(kwargs)

@response.command(
  help="Query properties in response"
)
@click.option('--query', required=True)
@click.argument('request_key')
def query(**kwargs):
  query_handler(kwargs)

@click.group(
  epilog="Run 'stoobly-agent request log COMMAND --help' for more information on a command.",
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
@click.option('--format', type=click.Choice(FORMATS), help='Format output.')
@click.option('--level', default=None, type=click.Choice(['DEBUG', 'INFO', 'WARNING', 'ERROR'], case_sensitive=False), help='Filter by log level.')
@click.option('--message', default=None, help='Filter by log message (e.g., "Mock success", "Mock failure").')
@click.option('--method', default=None, type=click.Choice(['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'HEAD', 'OPTIONS'], case_sensitive=False), help='Filter by HTTP method.')
@click.option('--namespace', default=None, help='Filter by workflow namespace.')
@click.option('--request-key', default=None, help='Filter by request key.')
@click.option('--scenario-key', default=None, help='Filter by scenario key.')
@click.option('--scenario-name', default=None, help='Filter by scenario name.')
@click.option('--select', multiple=True, help='Select column(s) to display.')
@click.option('--service-name', default=None, help='Filter by service name.')
@click.option('--status-code', default=None, type=click.IntRange(min=100, max=599), help='Filter by HTTP status code.')
@click.option('--test-title', default=None, help='Filter by test title.')
@click.option('--url', default=None, help='Filter by URL (substring match).')
@click.option('--without-headers', is_flag=True, default=False, help='Disable printing column headers.')
def log_list(**kwargs):
  context_dir_path = kwargs.get('context_dir_path') or DataDir.instance().context_dir_path

  # Extract print options
  output_format = kwargs.get('format', None)
  select = kwargs.get('select', None)
  without_headers = kwargs.get('without_headers', False)

  # Build filters dict from provided options
  filter_keys = ['level', 'message', 'method', 'scenario_key', 'scenario_name', 'service_name', 'status_code', 'url', 'request_key', 'test_title', 'namespace']
  filters = {}
  for key in filter_keys:
    value = kwargs.get(key)
    if value is not None:
      filters[key] = value

  # Pass print options to dump_logs
  SimpleInterceptedRequestsLogger.dump_logs(
    data_dir_path=context_dir_path,
    filters=filters if filters else None,
    output_format=output_format,
    select=select,
    without_headers=without_headers
  )

@log.command(name="delete", help="Delete intercepted requests log entries")
@click.option('--context-dir-path', default=None, help='Path to Stoobly data directory.')
def log_delete(**kwargs):
  context_dir_path = kwargs.get('context_dir_path') or DataDir.instance().context_dir_path
  SimpleInterceptedRequestsLogger.truncate(data_dir_path=context_dir_path)

request.add_command(response)
request.add_command(log)
