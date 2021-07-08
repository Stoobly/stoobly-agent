#!/usr/bin/env python

import click
import pdb
import threading

from stoobly_agent.proxy import run as run_proxy
from stoobly_agent.api import run as run_api

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
@click.version_option()
@click.group(
    epilog="Run 'stoobly-agent COMMAND --help' for more information on a command.",
    context_settings=CONTEXT_SETTINGS,
)
@click.pass_context
def main(ctx):
    pass

@main.command()
@click.option('--proxy-host', default='0.0.0.0', help='Address to bind proxy to.')
@click.option('--proxy-port', default=8080, help='Proxy service port.')
@click.option('--ui-host', default='0.0.0.0', help='Address to bind UI to.')
@click.option('--ui-port', default=4200, help='UI service port.')
@click.option('--headless', default=False, help='Disable starting frontend.')
def run(**kwargs):
    if not kwargs['headless']:
        thread = threading.Thread(target=run_api, args=(kwargs.get('ui_host'), kwargs.get('ui_port')))
        thread.start()

    # Filter out non-mitmproxy options
    kwargs['listen_host'] = kwargs['proxy_host']
    kwargs['listen_port'] = kwargs['proxy_port']

    del kwargs['proxy_host']
    del kwargs['proxy_port']
    del kwargs['ui_host']
    del kwargs['ui_port']
    del kwargs['headless']

    run_proxy(**kwargs)


