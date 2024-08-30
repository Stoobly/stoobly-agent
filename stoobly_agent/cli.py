import click
import json
import os
import pdb
import requests
import sys

from stoobly_agent import VERSION
from stoobly_agent.app.cli.helpers.context import ReplayContext
from stoobly_agent.app.cli.helpers.handle_mock_service import print_raw_response, RAW_FORMAT
from stoobly_agent.app.cli.helpers.validations import validate_project_key, validate_scenario_key
from stoobly_agent.app.proxy.constants import custom_response_codes
from stoobly_agent.app.proxy.replay.replay_request_service import replay as replay_request
from stoobly_agent.config.constants import env_vars, mode
from stoobly_agent.config.data_dir import DataDir
from stoobly_agent.lib.utils.conditional_decorator import ConditionalDecorator

from .app.api import run as run_api
from .app.cli import ca_cert, config, endpoint, feature, intercept, MainGroup, request, scenario, scaffold, snapshot, trace
from .app.cli.helpers.feature_flags import local, remote
from .app.settings import Settings
from .lib import logger
from .lib.orm.migrate_service import migrate as migrate_database
from .lib.utils.decode import decode

settings: Settings = Settings.instance()
is_remote = remote(settings)
is_local = local(settings)

# Makes sure database is up to date
migrate_database(VERSION)

CONNECTION_STRATEGIES = ['eager', 'lazy']
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.version_option()
@click.group(
    cls=MainGroup,
    context_settings=CONTEXT_SETTINGS,
    epilog="Run 'stoobly-agent COMMAND --help' for more information on a command.",
)
@click.pass_context
def main(ctx):
  ctx.terminal_width = 256

# Attach subcommands to main
main.add_command(ca_cert)
main.add_command(config)
main.add_command(endpoint)
main.add_command(feature)
main.add_command(intercept)
main.add_command(request)
main.add_command(scaffold)
main.add_command(scenario)
main.add_command(snapshot)
main.add_command(trace)

if settings.cli.features.dev_tools:
    from .app.cli import dev_tools
    main.add_command(dev_tools)

if settings.cli.features.exec:
    from .app.cli.decorators.exec import ExecDecorator
    ExecDecorator(main).decorate()

if settings.cli.features.remote:
    from .app.cli import project, report
    main.add_command(project)
    main.add_command(report)

@main.command(
    help="Initialize a new context"
)
def init(**kwargs):
    DataDir.instance().create()
    settings.reset_and_load()

@main.command(
    help="Run proxy and/or UI",
)
@ConditionalDecorator(lambda f: click.option('--api-url', help='API URL.')(f), is_remote)
@click.option('--certs', help='''
  SSL certificates of the form "[domain=]path". The domain may include a wildcard, and is equal to "*" if not specified. The file at path is a certificate in PEM format. If a private key is included in the
  PEM, it is used, else the default key in the conf dir is used. The PEM file should contain the full certificate chain, with the leaf certificate as the first entry. May be passed multiple times.
''')
@click.option('--cert-passphrase', help='''
  Passphrase for decrypting the private key provided in the --cert option. Note that passing cert_passphrase on the command line makes your passphrase visible in your system's process list. Specify it in
  config.yaml to avoid this.
''')
@click.option('--confdir', default=os.path.join(os.path.expanduser('~'), '.mitmproxy'), help='Location of the default mitmproxy configuration files.')
@click.option('--connection-strategy', help=', '.join(CONNECTION_STRATEGIES), type=click.Choice(CONNECTION_STRATEGIES))
@click.option('--flow-detail', default='1', type=click.Choice(['0', '1', '2', '3', '4']), help='''
  The display detail level for flows in mitmdump: 0 (quiet) to 4 (very verbose).
  0: no output
  1: shortened request URL with response status code
  2: full request URL with response status code and HTTP headers
  3: 2 + truncated response content, content of WebSocket and TCP messages (content_view_lines_cutoff: 512)
  4: 3 + nothing is truncated
''')
@click.option('--headless', is_flag=True, default=False, help='Disable starting UI.')
@click.option('--intercept', is_flag=True, default=False, help='Enable intercept on run.')
@click.option('--log-level', default=logger.INFO, type=click.Choice([logger.DEBUG, logger.INFO, logger.WARNING, logger.ERROR]), help='''
    Log levels can be "debug", "info", "warning", or "error"
''')
@click.option('--lifecycle-hooks-path', help='Path to lifecycle hooks script.')
@click.option('--modify-headers', multiple=True, help='''
  Header modify pattern of the form "[/flow-filter]/header-name/[@]header-value", where the separator can be any character. The @ allows to provide a file path that is used to read the header value string.
  An empty header-value removes existing header-name headers. May be passed multiple times.
''')
@click.option('--proxy-host', default='0.0.0.0', help='Address to bind proxy to.')
@click.option('--proxyless', is_flag=True, default=False, help='Disable starting proxy.')
@click.option('--proxy-mode', default="regular", help='''
  Proxy mode can be "regular", "transparent", "socks5",
  "reverse:SPEC", or "upstream:SPEC". For reverse and
  upstream proxy modes, SPEC is host specification in
  the form of "http[s]://host[:port]".
''')
@click.option('--proxy-port', default=8080, help='Proxy service port.')
@click.option('--public-directory-path', help='Path to public files. Used for mocking requests.')
@click.option('--response-fixtures-path', help='Path to response fixtures yaml. Used for mocking requests.')
@click.option('--ssl-insecure', is_flag=True, default=False, help='Do not verify upstream server SSL/TLS certificates.')
@click.option('--ui-host', default='0.0.0.0', help='Address to bind UI to.')
@click.option('--ui-port', default=4200, help='UI service port.')
def run(**kwargs):
    from .app.proxy.run import run as run_proxy

    os.environ[env_vars.AGENT_PROXY_URL] = f"http://{kwargs['proxy_host']}:{kwargs['proxy_port']}"

    if kwargs.get('lifecycle_hooks_path'):
      os.environ[env_vars.AGENT_LIFECYCLE_HOOKS_PATH] = kwargs['lifecycle_hooks_path']

    if kwargs.get('public_directory_path'):
      os.environ[env_vars.AGENT_PUBLIC_DIRECTORY_PATH] = kwargs['public_directory_path']

    if kwargs.get('response_fixtures_path'):
      os.environ[env_vars.AGENT_RESPONSE_FIXTURES_PATH] = kwargs['response_fixtures_path']

    # Observe config for changes
    Settings.instance().watch()

    if not os.getenv(env_vars.LOG_LEVEL):
        os.environ[env_vars.LOG_LEVEL] = kwargs['log_level']

    if 'api_url' in kwargs and kwargs['api_url']:
        os.environ[env_vars.API_URL] = kwargs['api_url']

    if 'headless' in kwargs and not kwargs['headless']:
        run_api(**kwargs)

    if 'proxyless' in kwargs and not kwargs['proxyless']:
        run_proxy(**kwargs)

@main.command(
  help="Mock request"
)
@click.option('-d', '--data', default='', help='HTTP POST data')
@ConditionalDecorator(lambda f: click.option('--remote-project-key', help='Use remote project for endpoint definitions.')(f), is_remote and is_local)
@click.option('--format', type=click.Choice([RAW_FORMAT]), help='Format response')
@click.option('-H', '--header', multiple=True, help='Pass custom header(s) to server')
@click.option('--lifecycle-hooks-path', help='Path to lifecycle hooks script.')
@ConditionalDecorator(lambda f: click.option('--project-key')(f), is_remote)
@click.option('--public-directory-path', help='Path to public files. Used for mocking requests.')
@click.option('--response-fixtures-path', help='Path to response fixtures yaml. Used for mocking requests.')
@click.option('-X', '--request', default='GET', help='Specify request command to use')
@click.option('--scenario-key')
@click.argument('url')
def mock(**kwargs):
  if kwargs.get('remote_project_key'):
    validate_project_key(kwargs['remote_project_key'])

  if kwargs.get('scenario_key'):
    validate_scenario_key(kwargs['scenario_key'])

  request = __build_request_from_curl(**kwargs)

  context = ReplayContext.from_python_request(request)
  response: requests.Response = replay_request(context, {
    **kwargs,
    'mode': mode.MOCK,
  })

  if response.status_code == custom_response_codes.NOT_FOUND:
    content = response.content
    print(f"Error: {decode(content)}")
    sys.exit(1)

  if kwargs['format'] == RAW_FORMAT:
    print_raw_response(response)
  else:
    content = response.content
    print(decode(content), end='')

@main.command(
  help="Record request"
)
@click.option('-d', '--data', default='', help='HTTP POST data')
@click.option('--format', type=click.Choice([RAW_FORMAT]), help='Format response')
@click.option('-H', '--header', multiple=True, help='Pass custom header(s) to server')
@ConditionalDecorator(lambda f: click.option('--project-key')(f), is_remote)
@click.option('-X', '--request', default='GET', help='Specify request command to use')
@click.option('--scenario-key')
@click.argument('url')
def record(**kwargs):
  if kwargs.get('scenario_key'):
    validate_scenario_key(kwargs['scenario_key'])

  request = __build_request_from_curl(**kwargs)

  context = ReplayContext.from_python_request(request)
  response: requests.Response = replay_request(context, {
    **kwargs,
    'mode': mode.RECORD,
  })

  if kwargs['format'] == RAW_FORMAT:
    print_raw_response(response)
  else:
    try:
      content = response.raw.data
      print(content.decode(json.detect_encoding(content)), end='')
    except UnicodeDecodeError:
      print('Warning: Binary output can mess up your terminal.')

def __build_request_from_curl(**kwargs):
  headers = {}
  for header in kwargs['header']:
    toks = header.split(':')

    if len(toks) != 2:
      continue

    headers[toks[0].strip()] = toks[1].strip()

  return requests.Request(
    data=kwargs['data'],
    headers=headers,
    method=kwargs['request'],
    url=kwargs['url']
  )
