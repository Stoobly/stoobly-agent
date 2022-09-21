import json
import click
import pdb

from stoobly_agent.lib.orm.trace import Trace
from stoobly_agent.lib.orm.trace_alias import TraceAlias
from stoobly_agent.lib.orm.trace_request import TraceRequest

from .helpers.print_service import select_print_options
from .helpers.tabulate_print_service import tabulate_print
from .helpers.validations import *

@click.group(
    epilog="Run 'stoobly-agent trace COMMAND --help' for more information on a command.",
    help="Manage traces"
)
@click.pass_context
def trace(ctx):
    pass

@trace.command(
    help="Create a trace"
)
def create(**kwargs):
    trace = Trace.create()
    print(trace.id)

@trace.command(
    help="Show all traces"
)
@click.option('--select', multiple=True, help='Select column(s) to display.')
@click.option('--size', default=10)
@click.option('--sort-by', default='created_at', help='created_at|name')
@click.option('--sort-order', default='desc', help='asc | desc')
@click.option('--without-headers', is_flag=True, default=False, help='Disable printing column headers.')
def list(**kwargs):
  print_options = select_print_options(kwargs)

  traces = Trace.limit(kwargs['size']).order_by(kwargs['sort_by'], kwargs['sort_order'])

  traces_json = json.loads(traces.get().to_json())
  for trace_json in traces_json:
    id = trace_json['id']

    trace_requests = TraceRequest.where_for(trace_id=id)
    trace_json['trace_requests_count'] = trace_requests.count()

    trace_aliases = TraceAlias.where_for(trace_id=id)
    trace_json['trace_aliases_count'] = trace_aliases.count()

  __print(traces_json, **print_options)

@click.group(
  epilog="Run 'stoobly-agent trace alias COMMAND --help' for more information on a command.",
  help="Manage trace aliases",
)
@click.pass_context
def alias(ctx):
  pass

@alias.command(
    help="Show all aliases for a trace"
)
@click.option('--name', help='Filter by name.')
@click.option('--select', multiple=True, help='Select column(s) to display.')
@click.option('--size', default=10)
@click.option('--sort-by', default='created_at', help='created_at|name')
@click.option('--sort-order', default='desc', help='asc | desc')
@click.option('--without-headers', is_flag=True, default=False, help='Disable printing column headers.')
@click.argument('trace_id')
def list(**kwargs):
  print_options = select_print_options(kwargs)

  columns = {
    'trace_id': kwargs['trace_id']
  }

  if kwargs['name']:
    columns['name'] = kwargs['name']

  trace_aliases = TraceAlias.where_for(**columns)
  trace_aliases = trace_aliases.limit(kwargs['size']).order_by(kwargs['sort_by'], kwargs['sort_order'])

  __print(json.loads(trace_aliases.get().to_json()), **{ **print_options, 'filter': ['trace_id']})

@alias.command(
  help="Create an alias for a trace"
)
@click.option('--name', required=True)
@click.option('--value', required=True)
@click.argument('trace_id')
def create(**kwargs):
  try:
    value = eval(kwargs['value'])
  except Exception as e:
    value = kwargs['value']

  trace_alias = TraceAlias.create(trace_id=kwargs['trace_id'], name=kwargs['name'], value=value)
  print(trace_alias.id)

def __print(traces, **kwargs):
  tabulate_print(
      traces, 
      filter=kwargs.get('filter') or [],
      headers=not kwargs.get('without_headers'),
      select=kwargs.get('select') or []
  )

trace.add_command(alias)

@alias.command(
  help="Create an alias for a trace"
)
@click.option('--name', required=True)
@click.option('--value', required=True)
@click.argument('trace_id')
def update(**kwargs):
  try:
    value = eval(kwargs['value'])
  except Exception as e:
    value = kwargs['value']

  trace_alias = TraceAlias.find_by(trace_id=kwargs['trace_id'], name=kwargs['name'])
  if not trace_alias:
    trace_alias = TraceAlias.create(trace_id=kwargs['trace_id'], name=kwargs['name'], value=value)
  else:
    trace_alias.update(value=value)
  
  print(trace_alias.id)

def __print(traces, **kwargs):
  tabulate_print(
      traces, 
      filter=kwargs.get('filter') or [],
      headers=not kwargs.get('without_headers'),
      select=kwargs.get('select') or []
  )

trace.add_command(alias)