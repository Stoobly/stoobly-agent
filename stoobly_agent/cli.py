#!/usr/bin/env python

import click

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
@click.option('--listen-host', default='0.0.0.0', help='Address to bind proxy to.')
@click.option('--listen-port', default=8080, help='Proxy service port.')
@click.option('--headless', help='Disable starting frontend.')
def run(**kwargs):
    #run_proxy(**kwargs)

    run_api('0.0.0.0', 3001)


