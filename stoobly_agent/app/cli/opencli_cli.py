import sys

import click

from stoobly_agent.app.cli.helpers.json_print import json_print
from stoobly_agent.app.cli.helpers.opencli_resolve import (
  MAIN_GROUP,
  OpencliResolveError,
  list_group_rows,
  read_document,
)
from stoobly_agent.app.cli.helpers.print_service import FORMATS, JSON_FORMAT, select_print_options
from stoobly_agent.app.cli.helpers.tabulate_print_service import tabulate_print


@click.group(
  epilog="Run 'stoobly-agent opencli COMMAND --help' for more information on a command.",
  help="Show OpenCLI descriptions for command groups",
)
@click.pass_context
def opencli(ctx):
  pass


@opencli.command(name='list', help='List command groups that have an OpenCLI description')
@click.option('--format', type=click.Choice(FORMATS), help='Format output.')
@click.option('--select', multiple=True, help='Select column(s) to display.')
@click.option('--without-headers', is_flag=True, default=False, help='Disable printing column headers.')
def list_(**kwargs):
  print_options = select_print_options(kwargs)
  rows = list_group_rows()
  if print_options.get('format') == JSON_FORMAT:
    json_print(rows, **print_options)
  else:
    tabulate_print(
      rows,
      headers=not print_options.get('without_headers'),
      select=print_options.get('select') or [],
    )


@opencli.command(
  help=f"Print the OpenCLI YAML for a command group. Defaults to '{MAIN_GROUP}' (root index)."
)
@click.argument('group', required=False, default=None)
def show(group: str):
  try:
    sys.stdout.write(read_document(group))
  except OpencliResolveError as e:
    print(e, file=sys.stderr)
    sys.exit(1)
