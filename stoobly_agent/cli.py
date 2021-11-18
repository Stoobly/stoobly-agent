#!/usr/bin/env python

import click
import distro
import json
import os
import pdb
import threading
import time

from .api import run as run_api
from .lib import env_vars
from .lib.ca_cert_installer import CACertInstaller
from .lib.cli.exec import run_command, run_command_with_proxy_export
from .lib.settings import Settings
from .proxy import run as run_proxy, get_proxy_url

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
@click.version_option()
@click.group(
    epilog="Run 'stoobly COMMAND --help' for more information on a command.",
    context_settings=CONTEXT_SETTINGS,
)
@click.pass_context
def main(ctx):
    pass

@click.group()
@click.pass_context
def config(ctx):
    pass

@click.group()
@click.pass_context
def ca_cert(ctx):
    pass

@main.command()
@click.option('--headless', is_flag=True, default=False, help='Disable starting UI.')
@click.option('--log-level', default='info', help='''
    Log level can be "debug", "info", "warning" or "error".
''')
@click.option('--mode', default="regular", help='''
    Mode can be "regular", "transparent", "socks5",
    "reverse:SPEC", or "upstream:SPEC". For reverse and
    upstream proxy modes, SPEC is host specification in
    the form of "http[s]://host[:port]".
'''
)
@click.option('--ssl-insecure', is_flag=True, default=False, help='Do not verify upstream server SSL/TLS certificates.')
@click.option('--proxy-host', default='0.0.0.0', help='Address to bind proxy to.')
@click.option('--proxy-port', default=8080, help='Proxy service port.')
@click.option('--ui-host', default='0.0.0.0', help='Address to bind UI to.')
@click.option('--ui-port', default=4200, help='UI service port.')
@click.option('--api-url', help='API URL.')
def run(**kwargs):
    if not os.getenv(env_vars.LOG_LEVEL):
        os.environ[env_vars.LOG_LEVEL] = kwargs['log_level']

    os.environ[env_vars.AGENT_PROXY_URL] = f"http://{kwargs['proxy_host']}:{kwargs['proxy_port']}"
    os.environ[env_vars.AGENT_URL] = f"http://{kwargs['ui_host']}:{kwargs['ui_port']}"

    if kwargs['api_url']:
        os.environ[env_vars.API_URL] = kwargs['api_url']

    if not kwargs['headless']:
        initialize_ui(kwargs)

    initialize_proxy(kwargs)

@main.command()
@click.option('--command', is_flag=True, default=False, help='Read commands from the command_string operand instead of from the standard input.')
@click.option('--shell', default='sh', help='Shell script to run interpret command(s).')
@click.argument('file_path')
def exec(**kwargs):
    is_command = kwargs['command']
    shell = kwargs['shell']
    file_path = kwargs['file_path']
    proxy_url = get_proxy_url()

    if not proxy_url:
        run_command(shell, file_path, is_command)
    else:
        run_command_with_proxy_export(shell, file_path, is_command, proxy_url)

@ca_cert.command()
def install(**kwargs):
    distro_name = distro.name(pretty=True)

    installer = CACertInstaller()

    # Ubuntu or other Debian based
    if distro.like() == 'debian':
        print(f"Installing CA certificate for {distro_name}...")
        installer.handle_debian()
    # MacOS
    elif distro.id() == 'darwin':
        installer.handle_darwin()
    # elif distro.id() == 'rhel':
    #     return
    else:
        print(f"{distro_name} is not supported yet for automatic CA cert installation.")

@ca_cert.command()
def uninstall():
    return

@config.command()
@click.option('--pretty-print', is_flag=True, default=False, help='Pretty print the json.')
@click.option('--save-to-file', is_flag=True, default=False, help='To save to a file or not.')
def dump(**kwargs):
    settings = Settings.instance()

    output = settings.to_json(pretty_print=kwargs['pretty_print'])

    if kwargs['save_to_file']:
        timestamp = str(int(time.time() * 1000))
        config_dump_file_name = f"stoobly_agent_config_dump_{timestamp}.json"

        with open(config_dump_file_name, 'w') as output_file:
            output_file.write(output)

        print(f"Config successfully dumped to {config_dump_file_name}")
    else:
        print(output)

# Attach subcommands to main
main.add_command(ca_cert)
main.add_command(config)

### Helpers

def initialize_ui(kwargs):
    ui_host = kwargs['ui_host']
    ui_port = kwargs['ui_port']

    print(f"UI server listening at http://{ui_host}:{ui_port}\n")

    thread = threading.Thread(target=run_api, args=(ui_host, ui_port))
    thread.start()

def initialize_proxy(kwargs):
    options = kwargs.copy()

    # Filter out non-mitmproxy options
    options['listen_host'] = options['proxy_host']
    options['listen_port'] = options['proxy_port']

    del options['headless']
    del options['log_level']
    del options['proxy_host']
    del options['proxy_port']
    del options['ui_host']
    del options['ui_port']
    del options['api_url']

    run_proxy(**options)
