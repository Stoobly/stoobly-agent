"""Helpers for bulk snapshot create (unsnapshotted) and update (diffs)."""

from typing import Callable, Optional, Set

from stoobly_agent.app.cli.helpers.diff_request_print import analyze_request_diff
from stoobly_agent.app.models.factories.resource.local_db.helpers.log import Log
from stoobly_agent.app.models.factories.resource.local_db.helpers.log_event import (
  MalformedLogEventError,
  PUT_ACTION,
  REQUEST_RESOURCE,
  SCENARIO_RESOURCE,
)
from stoobly_agent.app.models.factories.resource.local_db.helpers.request_snapshot import (
  MalformedRequestSnapshotError,
  RequestSnapshot,
)
from stoobly_agent.app.models.factories.resource.local_db.helpers.scenario_snapshot import ScenarioSnapshot
from stoobly_agent.lib.orm.request import Request
from stoobly_agent.lib.orm.scenario import Scenario


def snapshotted_request_uuids(log: Optional[Log] = None) -> Set[str]:
  """UUIDs covered by latest PUT request snapshots (standalone or inside scenarios)."""
  log = log or Log()
  uuids: Set[str] = set()

  def _add(snapshot: RequestSnapshot):
    if snapshot.exists:
      uuids.add(snapshot.uuid)

  for event in log.target_events:
    if event.action != PUT_ACTION:
      continue
    if event.resource == REQUEST_RESOURCE:
      _add(event.snapshot())
    elif event.resource == SCENARIO_RESOURCE:
      scenario_snapshot: ScenarioSnapshot = event.snapshot()
      if not scenario_snapshot.exists:
        continue
      scenario_snapshot.iter_request_snapshots(_add)

  return uuids


def snapshotted_scenario_uuids(log: Optional[Log] = None) -> Set[str]:
  """UUIDs covered by latest PUT scenario snapshots."""
  log = log or Log()
  uuids: Set[str] = set()

  for event in log.target_events:
    if event.action != PUT_ACTION:
      continue
    if event.resource != SCENARIO_RESOURCE:
      continue
    snapshot = event.snapshot()
    if snapshot.exists:
      uuids.add(event.resource_id)

  return uuids


def unsnapshotted_requests(log: Optional[Log] = None):
  """Non-deleted requests with no existing snapshot (standalone or scenario-contained)."""
  covered = snapshotted_request_uuids(log)
  return [
    request
    for request in Request.where('is_deleted', False).get()
    if request.uuid not in covered
  ]


def unsnapshotted_scenarios(log: Optional[Log] = None):
  """Non-deleted scenarios with no existing snapshot."""
  covered = snapshotted_scenario_uuids(log)
  return [
    scenario
    for scenario in Scenario.where('is_deleted', False).get()
    if scenario.uuid not in covered
  ]


def request_snapshot_has_diff(snapshot: RequestSnapshot) -> bool:
  if not snapshot.exists:
    return False
  try:
    if snapshot.request is None:
      return False
  except MalformedRequestSnapshotError:
    raise

  current = snapshot.find_resource()
  if not current or not current.response:
    return False

  analysis = analyze_request_diff(snapshot, current)
  return bool(analysis and analysis.has_diff)


def scenario_snapshot_has_diff(snapshot: ScenarioSnapshot) -> bool:
  """Same conditions as scenario diff output (metadata, request diffs, missing requests)."""
  if not snapshot.exists:
    return False

  current_scenario = snapshot.find_resource()
  if not current_scenario:
    return False

  snapshot_meta = snapshot.metadata
  name_differs = (snapshot_meta.get('name') or '') != (getattr(current_scenario, 'name', None) or '')
  description_differs = (snapshot_meta.get('description') or '') != (
    getattr(current_scenario, 'description', None) or ''
  )
  if name_differs or description_differs:
    return True

  request_snapshots = []
  snapshot.iter_request_snapshots(lambda request_snapshot: request_snapshots.append(request_snapshot))

  for request_snapshot in request_snapshots:
    current_request = request_snapshot.find_resource()
    if not current_request or not current_request.response:
      continue
    analysis = analyze_request_diff(request_snapshot, current_request)
    if analysis and analysis.has_diff:
      return True

  snapshot_request_uuids = {request_snapshot.uuid for request_snapshot in request_snapshots}
  for request in current_scenario.requests or []:
    if request.uuid not in snapshot_request_uuids:
      return True

  return False


def iter_put_request_snapshots(
  handler: Callable[[RequestSnapshot], None],
  log: Optional[Log] = None,
  *,
  include_scenario_contained: bool = True,
):
  """Visit distinct PUT request snapshots. Optionally expand scenario-contained requests."""
  log = log or Log()
  visited: Set[str] = set()

  def _visit(snapshot: RequestSnapshot):
    if snapshot.uuid in visited or not snapshot.exists:
      return
    visited.add(snapshot.uuid)
    handler(snapshot)

  for event in log.target_events:
    if event.action != PUT_ACTION:
      continue
    if event.resource == REQUEST_RESOURCE:
      _visit(event.snapshot())
    elif include_scenario_contained and event.resource == SCENARIO_RESOURCE:
      scenario_snapshot: ScenarioSnapshot = event.snapshot()
      if not scenario_snapshot.exists:
        continue
      scenario_snapshot.iter_request_snapshots(_visit)


def iter_put_scenario_snapshots(handler: Callable[[ScenarioSnapshot], None], log: Optional[Log] = None):
  """Visit distinct PUT scenario snapshots, like bulk scenario diff."""
  log = log or Log()
  visited: Set[str] = set()

  for event in log.target_events:
    if event.action != PUT_ACTION:
      continue
    if event.resource != SCENARIO_RESOURCE:
      continue
    if event.resource_id in visited:
      continue
    visited.add(event.resource_id)
    snapshot = event.snapshot()
    if not snapshot.exists:
      continue
    handler(snapshot)


__all__ = [
  'MalformedLogEventError',
  'MalformedRequestSnapshotError',
  'iter_put_request_snapshots',
  'iter_put_scenario_snapshots',
  'request_snapshot_has_diff',
  'scenario_snapshot_has_diff',
  'snapshotted_request_uuids',
  'snapshotted_scenario_uuids',
  'unsnapshotted_requests',
  'unsnapshotted_scenarios',
]
