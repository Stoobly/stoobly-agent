"""Format and collect snapshot rows for CLI list commands."""

import datetime
import functools
import os
import re
from typing import TYPE_CHECKING, List, Optional
from urllib.parse import urlparse

import click

from stoobly_agent.app.models.adapters.raw_joined import RawJoinedRequestAdapterFactory
from stoobly_agent.app.models.factories.resource.local_db.helpers.log import Log
from stoobly_agent.app.models.factories.resource.local_db.helpers.log_event import (
    LogEvent,
    REQUEST_RESOURCE,
    SCENARIO_RESOURCE,
)
from stoobly_agent.app.models.factories.resource.local_db.helpers.request_snapshot import RequestSnapshot
from stoobly_agent.app.models.factories.resource.local_db.helpers.scenario_snapshot import ScenarioSnapshot
from stoobly_agent.lib.api.keys.scenario_key import InvalidScenarioKey, ScenarioKey

from .print_service import FORMATS

if TYPE_CHECKING:
    from requests import Request


def snapshot_list_options(func):
    """Shared Click options for scenario/request snapshot list (same as former `snapshot list`, minus --resource)."""

    decorators = [
        click.option('--format', type=click.Choice(FORMATS), help='Format output.'),
        click.option('--pending', default=False, is_flag=True, help='Lists not yet processed snapshots.'),
        click.option(
            '--scenario-key',
            help='Only include snapshots for this scenario (scenario key).',
        ),
        click.option('--search', help='Regex pattern to filter snapshots by.'),
        click.option('--select', multiple=True, help='Select column(s) to display.'),
        click.option('--size', default=10, help='Number of rows to display.'),
        click.option('--without-headers', is_flag=True, default=False, help='Disable printing column headers.'),
    ]
    return functools.reduce(lambda f, d: d(f), reversed(decorators), func)


def list_snapshots(
    *,
    resource: str,
    pending: bool = False,
    scenario_key: Optional[str] = None,
    search: Optional[str] = None,
    size: Optional[int] = None,
) -> List[dict]:
    """Return formatted rows for the given snapshot resource type."""
    log = Log()
    if pending:
        events = log.unprocessed_events
    else:
        events = log.target_events

    if not events:
        return []

    return _format_events(
        events,
        resource=resource,
        scenario_key=scenario_key,
        search=search,
        size=size,
    )


def _format_events(
    events: List[LogEvent],
    *,
    resource: str,
    scenario_key: Optional[str],
    search: Optional[str],
    size: Optional[int],
) -> List[dict]:
    count = 0
    formatted_events: List[dict] = []
    limit = 10 if size is None else size

    if resource == SCENARIO_RESOURCE:
        for event in events:
            if count == limit:
                break

            if event.resource != SCENARIO_RESOURCE:
                continue

            if not _scenario_key_filter_matches(event, scenario_key):
                continue

            snapshot = event.snapshot()
            if not _scenario_snapshot_search_matches(snapshot, search):
                continue

            formatted_events.append({
                **_transform_scenario(snapshot),
                **_transform_event(event),
            })

            count += 1
    else:
        joined_events = []
        for event in events:
            if event.resource != REQUEST_RESOURCE:
                scenario_snapshot: ScenarioSnapshot = event.snapshot()
                scenario_snapshot.iter_request_snapshots(lambda snapshot: joined_events.append((event, snapshot)))
            else:
                joined_events.append((event, event.snapshot()))

        for joined_event in joined_events:
            if count == limit:
                break

            event, snapshot = joined_event
            request = _to_request(snapshot)

            if not _scenario_key_filter_matches(event, scenario_key):
                continue

            if not _request_matches(request, search):
                continue

            path = os.path.relpath(snapshot.path)
            scenario_name = ''

            if event.resource == SCENARIO_RESOURCE:
                ss: ScenarioSnapshot = event.snapshot()
                scenario_name = ss.metadata.get('name')

            formatted_events.append({
                **_transform_request(request),
                'snapshot': path,
                **_transform_event(event),
                'scenario': scenario_name,
            })

            count += 1

    return formatted_events


def _transform_event(event: LogEvent):
    event_dict = {}

    event_dict['uuid'] = event.uuid
    event_dict['action'] = event.action

    if event.created_at:
        event_dict['created_at'] = datetime.datetime.fromtimestamp(event.created_at / 1000)

    return event_dict


def _to_request(snapshot: RequestSnapshot):
    raw_request = snapshot.request
    if not raw_request:
        return None

    return RawJoinedRequestAdapterFactory(raw_request).python_request()


def _request_matches(request: 'Request', search: Optional[str]):
    if not search:
        return True

    if not request:
        return False

    if re.match(search, request.url):
        return True

    uri = urlparse(request.url)
    if uri.hostname and re.match(search, uri.hostname):
        return True

    if re.match(search, uri.path):
        return True

    return False


def _transform_request(request: 'Request'):
    event_dict = {'method': '', 'host': '', 'port': '', 'path': '', 'query': ''}

    if request:
        uri = urlparse(request.url)
        event_dict['method'] = request.method
        event_dict['host'] = uri.hostname
        event_dict['port'] = uri.port
        event_dict['path'] = uri.path
        event_dict['query'] = uri.query

    return event_dict


def _scenario_snapshot_search_matches(snapshot: ScenarioSnapshot, search: Optional[str]):
    """Match --search against scenario name or description (substring via re.search)."""
    if not search:
        return True

    metadata = snapshot.metadata
    name = metadata.get('name') or ''
    description = metadata.get('description') or ''
    try:
        return bool(re.search(search, name) or re.search(search, description))
    except re.error:
        return False


def _resolve_scenario_uuid(scenario_key: str) -> Optional[str]:
    """Resolve a scenario UUID from a scenario key string."""
    if not scenario_key or not scenario_key.strip():
        return None
    s = scenario_key.strip()
    try:
        return ScenarioKey(s).id
    except InvalidScenarioKey:
        return None


def _scenario_key_filter_matches(event: LogEvent, scenario_key: Optional[str]) -> bool:
    if not scenario_key or not scenario_key.strip():
        return True

    resolved = _resolve_scenario_uuid(scenario_key)
    if not resolved:
        return False

    if event.resource != SCENARIO_RESOURCE:
        return False

    return event.resource_uuid == resolved


def _transform_scenario(snapshot: ScenarioSnapshot):
    event_dict = {}

    metadata = snapshot.metadata
    event_dict['name'] = metadata.get('name')
    event_dict['description'] = metadata.get('description')

    return event_dict
