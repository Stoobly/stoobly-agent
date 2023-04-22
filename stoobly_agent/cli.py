import click
import json
import os
import pdb
import requests
import sys

from stoobly_agent import VERSION
from stoobly_agent.app.cli.helpers.context import ReplayContext
from stoobly_agent.app.cli.helpers.handle_mock_service import print_raw_response, RAW_FORMAT
from stoobly_agent.app.proxy.constants import custom_response_codes
from stoobly_agent.app.proxy.replay.replay_request_service import replay as replay_request
from stoobly_agent.config.constants import env_vars, mode
from stoobly_agent.config.data_dir import DataDir
from stoobly_agent.lib.utils.conditional_decorator import ConditionalDecorator

from .app.api import run as run_api
from .app.cli import ca_cert, config, feature, intercept, MainGroup, request, scenario, trace
from .app.settings import Settings
from .lib import logger
from .lib.orm.migrate_service import migrate as migrate_database

settings = Settings.instance()
is_remote = settings.cli.features.remote

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
    pass

# Attach subcommands to main
main.add_command(ca_cert)
main.add_command(config)
main.add_command(feature)
main.add_command(intercept)
main.add_command(request)
main.add_command(scenario)
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
@click.option('--connection-strategy', help=', '.join(CONNECTION_STRATEGIES), type=click.Choice(CONNECTION_STRATEGIES))
@click.option('--headless', is_flag=True, default=False, help='Disable starting UI.')
@click.option('--log-level', default=logger.INFO, type=click.Choice([logger.DEBUG, logger.INFO, logger.WARNING, logger.ERROR]), help='''
    Log levels can be "debug", "info", "warning", or "error"
''')
@click.option('--proxy-host', default='0.0.0.0', help='Address to bind proxy to.')
@click.option('--proxy-mode', default="regular", help='''
  Proxy mode can be "regular", "transparent", "socks5",
  "reverse:SPEC", or "upstream:SPEC". For reverse and
  upstream proxy modes, SPEC is host specification in
  the form of "http[s]://host[:port]".
''')
@click.option('--proxy-port', default=8080, help='Proxy service port.')
@click.option('--ssl-insecure', is_flag=True, default=False, help='Do not verify upstream server SSL/TLS certificates.')
@click.option('--ui-host', default='0.0.0.0', help='Address to bind UI to.')
@click.option('--ui-port', default=4200, help='UI service port.')
def run(**kwargs):
    from .app.proxy.run import run as run_proxy

    os.environ[env_vars.AGENT_PROXY_URL] = f"http://{kwargs['proxy_host']}:{kwargs['proxy_port']}"

    # Observe config for changes
    Settings.instance().watch()

    if not os.getenv(env_vars.LOG_LEVEL):
        os.environ[env_vars.LOG_LEVEL] = kwargs['log_level']

    if 'api_url' in kwargs and kwargs['api_url']:
        os.environ[env_vars.API_URL] = kwargs['api_url']

    if 'headless' in kwargs and not kwargs['headless']:
        run_api(**kwargs)

    run_proxy(**kwargs)

@main.command(
  help="Mock request"
)
@click.option('-d', '--data', default='', help='HTTP POST data')
@click.option('--format', type=click.Choice([RAW_FORMAT]), help='Format response')
@click.option('-H', '--header', multiple=True, help='Pass custom header(s) to server')
@ConditionalDecorator(lambda f: click.option('--project-key')(f), is_remote)
@click.option('-X', '--request', default='GET', help='Specify request command to use')
@click.option('--scenario-key')
@click.argument('url')
def mock(**kwargs):
  request = __build_request_from_curl(**kwargs)

  context = ReplayContext.from_python_request(request)
  response: requests.Response = replay_request(context, {
    **kwargs,
    'mode': mode.MOCK,
  })

  if response.status_code == custom_response_codes.NOT_FOUND:
    content = response.content
    print(f"Error: {content.decode(json.detect_encoding(content))}")
    sys.exit(1)

  if kwargs['format'] == RAW_FORMAT:
    print_raw_response(response)
  else:
    content = response.content
    print(content.decode(json.detect_encoding(content)))

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
  request = __build_request_from_curl(**kwargs)

  context = ReplayContext.from_python_request(request)
  response: requests.Response = replay_request(context, {
    **kwargs,
    'mode': mode.RECORD,
  })

  if kwargs['format'] == RAW_FORMAT:
    print_raw_response(response)
  else:
    content = response.content
    print(content.decode(json.detect_encoding(content)))

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