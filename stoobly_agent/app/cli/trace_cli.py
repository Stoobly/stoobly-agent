import click
import json
import pdb
import sys

from stoobly_agent.lib.orm.trace import Trace
from stoobly_agent.lib.orm.trace_alias import TraceAlias
from stoobly_agent.lib.orm.trace_request import TraceRequest

from .helpers.print_service import FORMATS, print_traces, select_print_options
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
  help="Clone a trace alias"
)
@click.argument('trace_id')
def clone(**kwargs):
  trace = Trace.find_by(id=kwargs['trace_id'])
  if not trace:
    print(f"Could not find trace {trace.id}", file=sys.stderr)
    sys.exit(1)

  cloned_trace = trace.clone()
  if not cloned_trace:
    print(f"Could not clone trace {trace.id}", file=sys.stderr)
    sys.exit(1)

  print(cloned_trace.id)

@trace.command(
    help="Show all traces"
)
@click.option('--format', type=click.Choice(FORMATS), help='Format output.')
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

  print_traces(traces_json, **{ **print_options, 'filter': ['updated_at']})

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
@click.option('--format', type=click.Choice(FORMATS), help='Format output.')
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

  print_traces(json.loads(trace_aliases.get().to_json()), **{ **print_options, 'filter': ['trace_id', 'updated_at']})

@alias.command(
  help="Create a trace alias"
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

@alias.command(
  help="Show a trace alias"
)
@click.option('--name', required=True)
@click.argument('trace_id')
def show(**kwargs):
  trace_alias = TraceAlias.find_by(trace_id=kwargs['trace_id'], name=kwargs['name'])

  if not trace_alias:
    print('Not found', file=sys.stderr)
    sys.exit(1)
  else:
    sys.stdout.write(trace_alias.value)

@alias.command(
  help="Update a trace alias"
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

trace.add_command(alias)