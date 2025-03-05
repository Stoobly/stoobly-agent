import click
import datetime
import pdb
import os
import re
import requests
import sys

from urllib.parse import urlparse
from typing import List

from stoobly_agent.app.models.adapters.raw_joined import RawJoinedRequestAdapterFactory
from stoobly_agent.app.models.factories.resource.local_db.helpers.log import Log
from stoobly_agent.app.models.factories.resource.local_db.helpers.log_event import LogEvent, PUT_ACTION, REQUEST_RESOURCE, SCENARIO_RESOURCE
from stoobly_agent.app.models.factories.resource.local_db.helpers.request_snapshot import RequestSnapshot
from stoobly_agent.app.models.factories.resource.local_db.helpers.scenario_snapshot import ScenarioSnapshot
from stoobly_agent.app.models.helpers.apply import Apply
from stoobly_agent.config.data_dir import DataDir
from stoobly_agent.lib.api.keys import RequestKey, ScenarioKey

from .helpers.print_service import FORMATS, print_snapshots, select_print_options
from .helpers.verify_raw_request_service import verify_raw_request

@click.group(
    epilog="Run 'stoobly-agent project COMMAND --help' for more information on a command.",
    help="Manage snapshots."
)
@click.pass_context
def snapshot(ctx):
    pass

@snapshot.command(
  help="Apply snapshots.",
)
@click.option('--force', is_flag=True, default=False, help="Toggles whether resources are hard deleted.")
@click.argument('uuid', required=False)
def apply(**kwargs):
  apply = Apply(force=kwargs['force']).with_logger(print)
  completed = True

  if kwargs.get('uuid'):
    completed = apply.single(kwargs['uuid'])
  else:
    completed = apply.all()

  if not completed:
    sys.exit(1)

@snapshot.command(
  help="Copy snapshots to a different data directory."
)
@click.option('--request-key', multiple=True, help='')
@click.option('--scenario-key', multiple=True, help='')
@click.argument('destination', required=True)
def copy(**kwargs):
  destination = kwargs['destination']
  __copy_scenarios(kwargs['scenario_key'], destination)
  __copy_requests(kwargs['request_key'], destination)

@snapshot.command(
  help="List snapshots.",
  name="list"
)
@click.option('--format', type=click.Choice(FORMATS), help='Format output.')
@click.option('--pending', default=False, is_flag=True, help='Lists not yet processed snapshots.')
@click.option(
  '--resource',
  default=REQUEST_RESOURCE,
  type=click.Choice([REQUEST_RESOURCE, SCENARIO_RESOURCE]),
  help=f"Defaults to {REQUEST_RESOURCE}."
)
@click.option('--scenario', help='Scenario name regex pattern to filter snapshots by')
@click.option('--search', help='Regex pattern to filter snapshots by.')
@click.option('--select', multiple=True, help='Select column(s) to display.')
@click.option('--size', default=10, help='Number of rows to display.')
@click.option('--without-headers', is_flag=True, default=False, help='Disable printing column headers.')
def _list(**kwargs):
  print_options = select_print_options(kwargs)

  log = Log()

  events = None
  if kwargs.get('pending'):
    events = log.unprocessed_events
  else:
    events = log.target_events

  if events:
    formatted_events = __format_events(events, **kwargs)

    if len(formatted_events):
      print_snapshots(formatted_events, **print_options)

@snapshot.command(
  help="Prune deleted snapshots."
)
@click.option('--dry-run', is_flag=True, default=False)
def prune(**kwargs):
  log = Log()
  log.prune(kwargs['dry_run'])

@snapshot.command(
  help="Update a snapshot.",
)
@click.option('--format', type=click.Choice(FORMATS), help='Format output.')
@click.option('--select', multiple=True, help='Select column(s) to display.')
@click.option('--verify', is_flag=True, default=False)
@click.option('--without-headers', is_flag=True, default=False, help='Disable printing column headers.')
@click.argument('uuid')
def update(**kwargs):
  print_options = select_print_options(kwargs)

  log = Log()

  event = None
  for _event in log.events:
    if _event.uuid == kwargs['uuid']:
      event = _event
      break

  if not event:
    print(f"Error: {kwargs['uuid']} not found", file=sys.stderr)
    sys.exit(1)

  if kwargs['verify']:
    if event.is_request(): 
      snapshot: RequestSnapshot = event.snapshot()
      __verify_request(snapshot)
    elif event.is_scenario():
      snapshot: ScenarioSnapshot = event.snapshot()
      snapshot.iter_request_snapshots(__verify_request)

  new_event = event.duplicate()
  log.append(str(new_event))

  formatted_events = __format_events([new_event], **kwargs)

  if len(formatted_events):
    print_snapshots(formatted_events, **print_options)

def __format_events(events: List[LogEvent], **kwargs):
  count = 0
  formatted_events = []
  size = 10 if kwargs.get('size') == None else kwargs['size']

  if kwargs.get('resource') == SCENARIO_RESOURCE:
    for event in events:
      if count == size:
        break

      if event.resource != SCENARIO_RESOURCE:
        continue

      if not __scenario_matches(event, kwargs.get('scenario')):
        continue

      snapshot = event.snapshot()
      if not __description_matches(snapshot, kwargs.get('search')):
        continue

      path = os.path.relpath(snapshot.metadata_path)

      formatted_events.append({
        **__transform_scenario(snapshot),
        'snapshot': path,
        **__transform_event(event)
      })

      count += 1
  else:
    joined_events = []
    for event in events:
      if event.resource != REQUEST_RESOURCE:
        snapshot: ScenarioSnapshot = event.snapshot()
        snapshot.iter_request_snapshots(lambda snapshot: joined_events.append((event, snapshot))) 
      else:
        joined_events.append((event, event.snapshot()))

    for joined_event in joined_events:
      if count == size:
        break

      event, snapshot = joined_event
      request = __to_request(snapshot)

      if not __scenario_matches(event, kwargs.get('scenario')):
        continue

      if not __request_matches(request, kwargs.get('search')):
        continue

      path = os.path.relpath(snapshot.path)
      scenario = ''

      if event.resource == SCENARIO_RESOURCE:
        snapshot: ScenarioSnapshot = event.snapshot()
        scenario = snapshot.metadata.get('name')

      formatted_events.append({
        **__transform_request(request),
        'snapshot': path,
        **__transform_event(event),
        'scenario': scenario
      })

      count += 1

  return formatted_events

def __verify_request(snapshot: RequestSnapshot):
  raw_request = snapshot.request
  if not raw_request:
    return

  verified_raw_request = verify_raw_request(raw_request)

  if raw_request != verified_raw_request:
    snapshot.write_raw(verified_raw_request)

def __transform_event(event: LogEvent):
  event_dict = {}

  event_dict['uuid'] = event.uuid
  event_dict['action'] = event.action

  if event.created_at:
    event_dict['created_at'] = datetime.datetime.fromtimestamp(event.created_at / 1000)

  return event_dict

def __to_request(snapshot: RequestSnapshot):
  raw_request = snapshot.request
  if not raw_request:
    return None

  return RawJoinedRequestAdapterFactory(raw_request).python_request()

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

def __description_matches(snapshot: ScenarioSnapshot, search: str):
  if not search:
    return True

  metadata = snapshot.metadata
  return re.match(search, metadata.get('description') or '')

def __scenario_matches(event: LogEvent, search: str):
  if not search:
    return True

  if event.resource != SCENARIO_RESOURCE:
    return False

  snapshot = event.snapshot()
  metadata = snapshot.metadata
  return re.match(search, metadata.get('name') or '')

def __transform_scenario(snapshot: ScenarioSnapshot):
  event_dict = {}

  metadata = snapshot.metadata
  event_dict['name'] = metadata.get('name')
  event_dict['description'] = metadata.get('description')

  return event_dict

def __copy_requests(request_keys: list, destination: str):
  log = Log()

  data_dir = DataDir.instance(destination)
  destination_log = Log(data_dir)

  for request_key in request_keys:
    found = False

    for event in log.target_events:
      if event.action != PUT_ACTION:
        continue

      if event.resource != REQUEST_RESOURCE:
        continue

      key = RequestKey(request_key)
      if event.resource_uuid != key.id:
        continue

      snapshot: RequestSnapshot = event.snapshot()
      snapshot.copy(destination)
      resource = snapshot.find_resource()

      if not resource:
        print(f"Could not find request {key.id}", file=sys.stderr)
      else:
        destination_log.put(resource)
        found = True

      if not found:
        print(f"No snapshot found for {key}", file=sys.stderr)

def __copy_scenarios(scenario_keys: list, destination: str):
  log = Log()

  data_dir =  DataDir.instance(destination)
  destination_log = Log(data_dir)

  for scenario_key in scenario_keys:
    found = False

    for event in log.target_events:
      if event.action != PUT_ACTION:
        continue

      if event.resource != SCENARIO_RESOURCE:
        continue

      key = ScenarioKey(scenario_key)
      if event.resource_uuid != key.id:
        continue

      snapshot: ScenarioSnapshot = event.snapshot()
      snapshot.copy(destination)
      resource = snapshot.find_resource()

      if not resource:
        print(f"Could not find scenario {key.id}", file=sys.stderr)
      else:
        destination_log.put(resource)
        found = True

      if not found:
        print(f"No snapshot found for {key}", file=sys.stderr)