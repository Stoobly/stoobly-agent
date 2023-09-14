import click
import datetime
import pdb

from stoobly_agent.app.models.factories.resource.local_db.helpers.log import Log
from stoobly_agent.app.models.factories.resource.local_db.helpers.log_event import LogEvent
from stoobly_agent.app.models.helpers.apply import Apply
from stoobly_agent.app.models.helpers.create_request_params_service import build_params

from .helpers.print_service import print_snapshots

LIST_FILTER_CHOICES = {
  'PENDING': 'pending'
}

@click.group(
    epilog="Run 'stoobly-agent project COMMAND --help' for more information on a command.",
    help="Manage snapshots"
)
@click.pass_context
def snapshot(ctx):
    pass

@snapshot.command(
  help="Apply snapshots",
)
@click.option('--force', default=False, help="Toggles whether resources are hard deleted.")
@click.argument('uuid', required=False)
def apply(**kwargs):
  apply = Apply(force=kwargs['force']).with_logger(print)

  if kwargs.get('uuid'):
    apply.single(kwargs['uuid'])
  else:
    apply.all()

@snapshot.command(
  help="List snapshots",
  name="list"
)
@click.option(
  '--filter', type=click.Choice(LIST_FILTER_CHOICES.values()),
)
@click.option('--select', multiple=True, help='Select column(s) to display.')
def _list(**kwargs):
  log = Log()

  events = None

  if kwargs.get('filter') == LIST_FILTER_CHOICES['PENDING']:
    events = log.unprocessed_events
  else:
    events = log.target_events

  formatted_events = list(map(__transform_event, events))

  if len(formatted_events):
    print_snapshots(formatted_events, **kwargs)

def __transform_event(event: LogEvent):
  event_dict = {}

  snapshot = event.snapshot()

  if event.is_scenario():
    metadata = snapshot.metadata
    event_dict['name'] = metadata.get('name')
    event_dict['description'] = metadata.get('description')
  elif event.is_request():
    raw_request = snapshot.request

    if raw_request:
      params = build_params(raw_request)
      flow = params.get('flow')
      request = flow.request

      event_dict['name'] = request.url
      event_dict['description'] = request.method
    else:
      event_dict['name'] = ''
      event_dict['description'] = ''

  event_dict['resource_key'] = ''

  resource = snapshot.find_resource()
  if resource:
    event_dict['resource_key'] = resource.key()

    if event.is_scenario():
      event_dict['name'] = resource.name
      event_dict['description'] = resource.description
    elif event.is_request():
      event_dict['name'] = resource.url
      event_dict['description'] = resource.method
  
  event_dict = { **event_dict, **event.to_dict() }

  if event.created_at:
    event_dict['created_at'] = datetime.datetime.fromtimestamp(event.created_at / 1000)

  return event_dict