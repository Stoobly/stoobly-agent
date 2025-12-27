import click
import json
import os
import pdb
import sys

from stoobly_agent import VERSION
from stoobly_agent.app.cli.helpers.handle_mock_service import RAW_FORMAT
from stoobly_agent.app.cli.helpers.validations import validate_project_key, validate_scenario_key
from stoobly_agent.app.cli.intercept_cli import mode_options
from stoobly_agent.config.constants import env_vars, mode
from stoobly_agent.config.data_dir import DataDir
from stoobly_agent.lib.logger import Logger
from stoobly_agent.lib.utils.conditional_decorator import ConditionalDecorator
from .app.cli import MainGroup
from .app.cli.helpers.feature_flags import local, remote
from .app.settings import Settings
from .lib import logger
from .lib.orm.migrate_service import migrate as migrate_database

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

if settings.cli.features.exec:
    from .app.cli.decorators.exec import ExecDecorator
    ExecDecorator(main).decorate()

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
@click.option('--ca-certs-dir-path', default=DataDir.instance().ca_certs_dir_path, help='Path to ca certs directory used to sign SSL certs.')
@click.option('--certs', help='''
  SSL certificates of the form "[domain=]path". The domain may include a wildcard, and is equal to "*" if not specified. The file at path is a certificate in PEM format. If a private key is included in the
  PEM, it is used, else the default key in the conf dir is used. The PEM file should contain the full certificate chain, with the leaf certificate as the first entry. May be passed multiple times.
''')
@click.option('--cert-passphrase', help='''
  Passphrase for decrypting the private key provided in the --cert option. Note that passing cert_passphrase on the command line makes your passphrase visible in your system's process list. Specify it in
  config.yaml to avoid this.
''')
@click.option('--connection-strategy', help=', '.join(CONNECTION_STRATEGIES), type=click.Choice(CONNECTION_STRATEGIES))
@click.option('--detached', type=click.Path(), help='Run in detached mode and redirect output to the specified file path.')
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
@click.option('--intercept-mode', type=click.Choice(mode_options), help='Set intercept mode.')
@click.option('--log-level', default=logger.INFO, type=click.Choice([logger.DEBUG, logger.INFO, logger.WARNING, logger.ERROR]), help='''
    Log levels can be "debug", "info", "warning", or "error"
''')
@click.option('--lifecycle-hooks-path', help='Path to lifecycle hooks script.')
@click.option('--proxy-host', default='0.0.0.0', help='Address to bind proxy to.')
@click.option('--proxyless', is_flag=True, default=False, help='Disable starting proxy.')
@click.option('--proxy-mode', default="regular", help='''
  Proxy mode can be "regular", "transparent", "socks5",
  "reverse:SPEC", or "upstream:SPEC". For reverse and
  upstream proxy modes, SPEC is host specification in
  the form of "http[s]://host[:port]".
''')
@click.option('--proxy-port', default=8080, type=click.IntRange(1, 65535), help='Proxy service port.')
@click.option('--public-directory-path', multiple=True, help='Path to public files. Used for mocking requests. Can take the form <FOLDER-PATH>[:<ORIGIN>].')
@click.option('--response-fixtures-path', multiple=True, help='Path to response fixtures yaml. Used for mocking requests. Can take the form <FILE-PATH>[:<ORIGIN>].')
@click.option('--request-log-enable', is_flag=True, default=False, required=False, help='Enable intercepted requests logging.')
@click.option('--request-log-level', default=logger.INFO, type=click.Choice([logger.DEBUG, logger.INFO, logger.WARNING, logger.ERROR]), help='Log level for intercepted requests.')
@click.option('--request-log-truncate', is_flag=True, default=True, required=False, help='Truncate the intercepted requests log.')
@click.option('--ssl-insecure', is_flag=True, default=False, help='Do not verify upstream server SSL/TLS certificates.')
@click.option('--ui-host', default='0.0.0.0', help='Address to bind UI to.')
@click.option('--ui-port', default=4200, type=click.IntRange(1, 65535), help='UI service port.')
@click.option('--upstream-auth', help='Add HTTP Basic authentication to upstream proxy and reverse proxy requests. Format: username:password')
def run(**kwargs):
    from .app.proxy.run import run as run_proxy

    # Observe config for changes
    settings: Settings = Settings.instance()
    settings.watch()

    if not os.path.exists(kwargs.get('ca_certs_dir_path')):
      kwargs['ca_certs_dir_path'] = DataDir.instance().ca_certs_dir_path

    if kwargs.get('headless'):
      os.environ[env_vars.AGENT_HEADLESS] = '1'

    if kwargs.get('intercept'):
      os.environ[env_vars.AGENT_INTERCEPT_ACTIVE] = '1'

    if kwargs.get('intercept_mode'):
      os.environ[env_vars.AGENT_INTERCEPT_MODE] = kwargs['intercept_mode']
      settings.proxy.intercept.mode = kwargs['intercept_mode']

    if kwargs.get('lifecycle_hooks_path'):
      os.environ[env_vars.AGENT_LIFECYCLE_HOOKS_PATH] = kwargs['lifecycle_hooks_path']

    if kwargs.get('public_directory_path'):
      # Join multiple paths with commas
      public_dirs = kwargs['public_directory_path']
      if isinstance(public_dirs, (list, tuple)):
        os.environ[env_vars.AGENT_PUBLIC_DIRECTORY_PATH] = ','.join(public_dirs)
      else:
        os.environ[env_vars.AGENT_PUBLIC_DIRECTORY_PATH] = public_dirs

    if kwargs.get('response_fixtures_path'):
      response_fixtures_paths = kwargs.get('response_fixtures_path', ())
      if response_fixtures_paths:
        response_fixtures = ','.join(response_fixtures_paths)
        os.environ[env_vars.AGENT_RESPONSE_FIXTURES_PATH] = response_fixtures

    if not os.getenv(env_vars.LOG_LEVEL):
      os.environ[env_vars.LOG_LEVEL] = kwargs['log_level']

    if kwargs.get('api_url'):
      os.environ[env_vars.API_URL] = kwargs['api_url']

    if not kwargs.get('headless'):
      ui_url = f"http://{kwargs['ui_host']}:{kwargs['ui_port']}"
      os.environ[env_vars.AGENT_UI_URL] = ui_url
      settings.ui.active = True
      settings.ui.url = ui_url

    if not kwargs.get('proxyless'):
      proxy_url = f"http://{kwargs['proxy_host']}:{kwargs['proxy_port']}"
      os.environ[env_vars.AGENT_PROXY_URL] = proxy_url
      settings.proxy.url = proxy_url

    if kwargs.get('request_log_enable'):
      from stoobly_agent.lib.intercepted_requests_logger import InterceptedRequestsLogger
      # If truncating, do that first (it handles enable internally)
      if kwargs.get('request_log_truncate'):
        InterceptedRequestsLogger.truncate()
      else:
        InterceptedRequestsLogger.enable_logger_file()

      # Set log level after logger is enabled
      request_log_level = kwargs.get('request_log_level')
      if request_log_level:
        InterceptedRequestsLogger.set_log_level(request_log_level)

    if kwargs.get('detached'):
      # Run in detached mode with output redirection
      import subprocess
      import sys
      
      # Build the command to run in background
      cmd = [sys.executable, '-m', 'stoobly_agent'] + sys.argv[1:]
      # Remove the --detached flag and its value from the command
      detached_index = None
      for i, arg in enumerate(cmd):
        if arg == '--detached':
          detached_index = i
          break
      if detached_index is not None:
        cmd.pop(detached_index)  # Remove --detached
        if detached_index < len(cmd) and not cmd[detached_index].startswith('--'):
          cmd.pop(detached_index)  # Remove the file path
      
      # Start the process in background with output redirection
      with open(kwargs['detached'], 'w') as output_file:
        process = subprocess.Popen(
          cmd,
          stdout=output_file,
          stderr=subprocess.STDOUT,  # Redirect stderr to stdout
          preexec_fn=os.setsid  # Create new process group
        )
      
      print(process.pid)
      return
    else:
      # Run in foreground mode
      if not kwargs.get('headless'):
        settings.commit()

        from .app.api import run as run_api
        run_api(**kwargs)

      if not kwargs.get('proxyless'):
        log_id = 'Proxy'
        Logger.instance(log_id).info(f"starting with mode {kwargs['proxy_mode']} and listening at {kwargs['proxy_host']}:{kwargs['proxy_port']}")
        Logger.instance(log_id).info(f"{'' if settings.proxy.intercept.active else 'not yet '}configured to {settings.proxy.intercept.mode}")
        run_proxy(**kwargs)

@main.command(
  help="Mock request"
)
@click.option('-d', '--data', default='', help='HTTP POST data')
@ConditionalDecorator(lambda f: click.option('--remote-project-key', help='Use remote project for endpoint definitions.')(f), is_remote and is_local)
@click.option('--format', type=click.Choice([RAW_FORMAT]), help='Format response')
@click.option('-H', '--header', multiple=True, help='Pass custom header(s) to server')
@click.option('--lifecycle-hooks-path', help='Path to lifecycle hooks script.')
@click.option('-o', '--output', help='Write to file instead of stdout')
@ConditionalDecorator(lambda f: click.option('--project-key')(f), is_remote)
@click.option('--public-directory-path', multiple=True, help='Path to public files. Used for mocking requests. Can take the form <FOLDER-PATH>[:<ORIGIN>].')
@click.option('--response-fixtures-path', multiple=True, help='Path to response fixtures yaml. Used for mocking requests. Can take the form <FILE-PATH>[:<ORIGIN>].')
@click.option('-X', '--request', default='GET', help='Specify request command to use')
@click.option('--scenario-key')
@click.argument('url')
def mock(**kwargs):
  from stoobly_agent.app.cli.helpers.handle_mock_service import print_raw_response
  from stoobly_agent.app.proxy.constants import custom_response_codes
  from stoobly_agent.lib.utils.decode import decode
  
  if kwargs.get('remote_project_key'):
    validate_project_key(kwargs['remote_project_key'])

  response = __replay(mode.MOCK, **kwargs)

  if response.status_code == custom_response_codes.NOT_FOUND:
    content = response.content
    print(f"Error: {decode(content)}")
    sys.exit(1)

  if kwargs['format'] == RAW_FORMAT:
    print_raw_response(response, kwargs['output'])
  else:
    content = response.content

    if not kwargs['output']:
      print(decode(content), end='')
    else:
      with open(kwargs['output'], 'w') as fp:
        fp.write(decode(content)) 

@main.command(
  help="Record request"
)
@click.option('-d', '--data', default='', help='HTTP POST data')
@click.option('--format', type=click.Choice([RAW_FORMAT]), help='Format response')
@click.option('-H', '--header', multiple=True, help='Pass custom header(s) to server')
@click.option('--lifecycle-hooks-path', help='Path to lifecycle hooks script.')
@click.option('-o', '--output', help='Write to file instead of stdout')
@ConditionalDecorator(lambda f: click.option('--project-key')(f), is_remote)
@click.option('-X', '--request', default='GET', help='Specify request command to use')
@click.option('--scenario-key')
@click.argument('url')
def record(**kwargs):
  from stoobly_agent.app.cli.helpers.handle_mock_service import print_raw_response
  
  response = __replay(mode.RECORD, **kwargs) 

  if kwargs['format'] == RAW_FORMAT:
    print_raw_response(response, kwargs['output'])
  else:
    content: bytes = response.raw.data

    if not kwargs['output']:
      try:
        print(content.decode(json.detect_encoding(content)), end='')
      except UnicodeDecodeError:
        print('Warning: Binary output can mess up your terminal.')
    else:
      with open(kwargs['output'], 'w') as fp:
        fp.write(content.decode(json.detect_encoding(content))) 

def __build_request_from_curl(**kwargs):
  import requests
  
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

def __replay(mode, **kwargs):
  from stoobly_agent.app.cli.helpers.context import ReplayContext
  from stoobly_agent.app.proxy.replay.replay_request_service import replay as replay_request
  
  if kwargs.get('scenario_key'):
    validate_scenario_key(kwargs['scenario_key'])

  request = __build_request_from_curl(**kwargs)

  context = ReplayContext.from_python_request(request)
  return replay_request(context, {
    **kwargs,
    'mode': mode,
  })