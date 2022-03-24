import click
import os
import pdb
import threading

from stoobly_agent.config.constants import env_vars

from .app.api import run as run_api
from .app.cli import ca_cert, config, feature, request
from .app.cli.utils.migrate_service import migrate as migrate_database
from .app.proxy import INTERCEPT_MODES, run as run_proxy
from .app.settings import Settings

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
settings = Settings.instance()

@click.version_option()
@click.group(
    epilog="Run 'stoobly-agent COMMAND --help' for more information on a command.",
    context_settings=CONTEXT_SETTINGS,
)
@click.pass_context
def main(ctx):
    pass

# Attach subcommands to main
main.add_command(ca_cert)
main.add_command(config)
main.add_command(feature)
main.add_command(request)

if settings.features.get('dev_tools'):
    from .app.cli import dev_tools
    main.add_command(dev_tools)

if settings.features.get('exec'):
    from .app.cli.decorators.exec import ExecDecorator
    ExecDecorator(main).decorate()

if settings.features.get('remote'):
    from .app.cli import report, scenario
    main.add_command(report)
    main.add_command(scenario)

@main.command(
    help="Run proxy and/or UI",
)
@click.option('--api-url', help='API URL.')
@click.option('--headless', is_flag=True, default=False, help='Disable starting UI.')
@click.option('--intercept-mode', help=', '.join(INTERCEPT_MODES))
@click.option('--log-level', default='info', help='''
    Log levels can be "debug", "info", "warning", or "error"
''')
@click.option('--proxy-host', default='0.0.0.0', help='Address to bind proxy to.')
@click.option('--proxy-mode', default="regular", help='''
    Proxy mode can be "regular", "transparent", "socks5",
    "reverse:SPEC", or "upstream:SPEC". For reverse and
    upstream proxy modes, SPEC is host specification in
    the form of "http[s]://host[:port]".
'''
)
@click.option('--proxy-port', default=8080, help='Proxy service port.')
@click.option('--ssl-insecure', is_flag=True, default=False, help='Do not verify upstream server SSL/TLS certificates.')
@click.option('--test-script', help='Provide a custom script for testing.')
@click.option('--ui-host', default='0.0.0.0', help='Address to bind UI to.')
@click.option('--ui-port', default=4200, help='UI service port.')
def run(**kwargs):
    os.environ[env_vars.AGENT_PROXY_URL] = f"http://{kwargs['proxy_host']}:{kwargs['proxy_port']}"
    os.environ[env_vars.AGENT_URL] = f"http://{kwargs['ui_host']}:{kwargs['ui_port']}"

    if not os.getenv(env_vars.LOG_LEVEL):
        os.environ[env_vars.LOG_LEVEL] = kwargs['log_level']

    if kwargs['api_url']:
        os.environ[env_vars.API_URL] = kwargs['api_url']

    if kwargs['test_script']:
        os.environ[env_vars.TEST_SCRIPT] = kwargs['test_script']

    if not kwargs['headless']:
        __initialize_ui(kwargs)

    migrate_database()

    run_proxy(**kwargs)

### Helpers

def __initialize_ui(kwargs):
    ui_host = kwargs['ui_host']
    ui_port = kwargs['ui_port']

    print(f"UI server listening at http://{ui_host}:{ui_port}\n")

    thread = threading.Thread(target=run_api, args=(ui_host, ui_port))
    thread.start()


