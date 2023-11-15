import click
import datetime
import pdb
import os
import re
import requests

from urllib.parse import urlparse

from stoobly_agent.app.models.adapters.joined_request_adapter import JoinedRequestAdapter
from stoobly_agent.app.models.adapters.raw_http_request_adapter import RawHttpRequestAdapter
from stoobly_agent.app.models.factories.resource.local_db.helpers.log import Log
from stoobly_agent.app.models.factories.resource.local_db.helpers.log_event import LogEvent, REQUEST_RESOURCE, SCENARIO_RESOURCE
from stoobly_agent.app.models.helpers.apply import Apply

from .helpers.print_service import print_snapshots

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
@click.option('--pending', default=False, is_flag=True, help='Lists not yet processed snapshots.')
@click.option(
  '--resource',
  default=REQUEST_RESOURCE,
  type=click.Choice([REQUEST_RESOURCE, SCENARIO_RESOURCE]),
  help=f"Defaults to {REQUEST_RESOURCE}."
)
@click.option('--search', help='Regex pattern to filter snapshots by.')
@click.option('--select', multiple=True, help='Select column(s) to display.')
@click.option('--without-headers', is_flag=True, default=False, help='Disable printing column headers.')
def _list(**kwargs):
  log = Log()

  events = None

  if kwargs.get('pending'):
    events = log.unprocessed_events
  else:
    events = log.target_events

  formatted_events = []
  if kwargs.get('resource') == SCENARIO_RESOURCE:
    for event in events:
      if event.resource != SCENARIO_RESOURCE:
        continue
 
      if not __scenario_matches(event, kwargs.get('search')):
        continue

      path = os.path.relpath(event.snapshot().metadata_path)

      formatted_events.append({
        **__transform_scenario(event),
        'snapshot': path,
        **__transform_event(event),
      })
  else:
    for event in events:
      if event.resource != REQUEST_RESOURCE:
        continue

      request = __to_request(event)

      if not __request_matches(request, kwargs.get('search')):
        continue

      path = os.path.relpath(event.snapshot().path)

      formatted_events.append({
        **__transform_request(request),
        'snapshot': path,
        **__transform_event(event),
      })

  if len(formatted_events):
    print_snapshots(formatted_events, **kwargs)

def __transform_event(event: LogEvent):
  event_dict = {}

  event_dict['uuid'] = event.uuid
  event_dict['action'] = event.action

  if event.created_at:
    event_dict['created_at'] = datetime.datetime.fromtimestamp(event.created_at / 1000)

  return event_dict

def __to_request(event: LogEvent):
  snapshot = event.snapshot()
  raw_request = snapshot.request
  if not raw_request:
    return None

  adapter = JoinedRequestAdapter(raw_request)
  request_string = adapter.build_request_string().get()
  return RawHttpRequestAdapter(request_string).to_request()

def __request_matches(request: requests.Request, search: str):
  if not search:
    return True
  
  if not request:
    return False

  uri = urlparse(request.url)
  return re.match(search, request.url) or re.match(search, uri.path)

def __transform_request(request: requests.Request):
  event_dict = { 'method': '', 'host': '', 'port': '', 'path': '', 'query': ''}

  if request:
    uri = urlparse(request.url)
    event_dict['method'] = request.method
    event_dict['host'] = uri.hostname
    event_dict['port'] = uri.port
    event_dict['path'] = uri.path
    event_dict['query'] = uri.query

  return event_dict

def __scenario_matches(event: LogEvent, search: str):
  if not search:
    return True

  snapshot = event.snapshot()
  metadata = snapshot.metadata
  return re.match(search, metadata.get('name') or '')

def __transform_scenario(event: LogEvent):
  snapshot = event.snapshot()
  event_dict = {}

  metadata = snapshot.metadata
  event_dict['name'] = metadata.get('name')
  event_dict['description'] = metadata.get('description')

  return event_dict