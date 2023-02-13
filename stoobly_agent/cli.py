import click
import os
import pdb
import sys

from stoobly_agent import VERSION
from stoobly_agent.config.constants import env_vars
from stoobly_agent.config.data_dir import DataDir
from stoobly_agent.lib.utils.conditional_decorator import ConditionalDecorator

from .app.api import run as run_api
from .app.cli import ca_cert, config, feature, intercept, MainGroup, request, scenario, trace
from .app.proxy import CONNECTION_STRATEGIES, INTERCEPT_MODES, run as run_proxy
from .app.settings import Settings
from .lib import logger
from .lib.orm.migrate_service import migrate as migrate_database

settings = Settings.instance()
is_remote = settings.cli.features.remote

# Makes sure database is up to date
migrate_database(VERSION)

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
@click.option('--headless', is_flag=True, default=False, help='Disable starting UI.')
@click.option('--connection-strategy', help=', '.join(CONNECTION_STRATEGIES), type=click.Choice(CONNECTION_STRATEGIES))
@click.option('--intercept-mode', help=', '.join(INTERCEPT_MODES), type=click.Choice(INTERCEPT_MODES))
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
    os.environ[env_vars.AGENT_PROXY_URL] = f"http://{kwargs['proxy_host']}:{kwargs['proxy_port']}"

    if not os.getenv(env_vars.LOG_LEVEL):
        os.environ[env_vars.LOG_LEVEL] = kwargs['log_level']

    if 'api_url' in kwargs and kwargs['api_url']:
        os.environ[env_vars.API_URL] = kwargs['api_url']

    if 'headless' in kwargs and not kwargs['headless']:
        run_api(**kwargs)

    if kwargs['intercept_mode'] and kwargs['intercept_mode'] not in INTERCEPT_MODES:
        print(f"Error: Invalid value for --intercept-mode, values: {', '.join(INTERCEPT_MODES)}", file=sys.stderr)
        sys.exit(1)

    run_proxy(**kwargs)