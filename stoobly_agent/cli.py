#!/usr/bin/env python

import click
import json
import os
import pdb
import time
import threading

from .api import run as run_api
from .proxy import run as run_proxy
from .lib.env_vars import LOG_LEVEL
from .lib.settings import Settings

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
@click.version_option()
@click.group(
    epilog="Run 'stoobly COMMAND --help' for more information on a command.",
    context_settings=CONTEXT_SETTINGS,
)
@click.pass_context
def main(ctx):
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
@click.option('--proxy-host', default='0.0.0.0', help='Address to bind proxy to.')
@click.option('--proxy-port', default=8080, help='Proxy service port.')
@click.option('--ui-host', default='0.0.0.0', help='Address to bind UI to.')
@click.option('--ui-port', default=4200, help='UI service port.')
@click.option('--api-url', help='API URL.')
def run(**kwargs):
    if not os.getenv(LOG_LEVEL):
        os.environ[LOG_LEVEL] = kwargs['log_level']

    settings = Settings.instance()
    settings.proxy_url = f"http://{kwargs['proxy_host']}:{kwargs['proxy_port']}"
    settings.agent_url = f"http://{kwargs['ui_host']}:{kwargs['ui_port']}"

    if kwargs['api_url']:
        settings.api_url = kwargs['api_url']

    if not kwargs['headless']:
        initialize_ui(kwargs)

    initialize_proxy(kwargs)

@main.command()
@click.option('--pretty-print', is_flag=True, default=False, help='Pretty print the json.')
@click.option('--save-to-file', is_flag=True, default=False, help='To save to a file or not.')
def dump_config(**kwargs):
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
