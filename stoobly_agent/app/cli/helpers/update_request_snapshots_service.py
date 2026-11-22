import os
import sys
from typing import Callable, Dict, List, Optional, Tuple

from stoobly_agent.app.models.factories.resource.local_db.helpers.log import Log
from stoobly_agent.app.models.factories.resource.local_db.helpers.log_event import LogEvent, REQUEST_RESOURCE, SCENARIO_RESOURCE
from stoobly_agent.app.models.factories.resource.local_db.helpers.request_snapshot import RequestSnapshot
from stoobly_agent.app.models.factories.resource.local_db.helpers.scenario_snapshot import ScenarioSnapshot
from stoobly_agent.app.models.factories.resource.local_db.helpers.snapshot_types import DELETE_ACTION, PUT_ACTION, Action
from stoobly_agent.config.data_dir import DataDir

def update_request_snapshots(
    file_path: Optional[str],
    action: Action = PUT_ACTION,
    lifecycle_hooks_path: Optional[str] = None,
    no_verify: bool = False,
    with_snapshot: bool = True,
    resource_uuid: Optional[str] = None,
):
    """
    Update request snapshots given a file path.
    
    Args:
        file_path: Path to a request snapshot or scenario snapshot metadata file
        lifecycle_hooks_path: Path to lifecycle hooks script
        with_snapshot: Whether to clone the event before updating
        no_verify: Whether to skip verification of requests
    """
    if file_path is None:
        print("Error: No file path provided", file=sys.stderr)
        sys.exit(1)

    log = Log()
    data_dir = DataDir.instance()
    
    # Normalize the path
    abs_path = os.path.abspath(file_path)
    
    # Determine if it's a request snapshot or scenario snapshot
    request_snapshots_dir = data_dir.snapshots_requests_dir_path
    scenarios_dir = data_dir.snapshots_scenarios_dir_path

    request_snapshots = []
    
    # Check if it's a request snapshot path
    if abs_path.startswith(request_snapshots_dir):
        request_snapshot = RequestSnapshot.from_path(abs_path, data_dir=data_dir, uuid=resource_uuid)
        if not request_snapshot:
            print(f"Error: Invalid request snapshot path format: {file_path}", file=sys.stderr)
            sys.exit(1)

        uuid = request_snapshot.uuid
        event = _find_event_by_resource_uuid(log, REQUEST_RESOURCE, uuid)
        if not event:
            print(f"Error: No event found for request snapshot {uuid}", file=sys.stderr)
            sys.exit(1)

        if not no_verify:
            _verify_request(request_snapshot)

        request_snapshots.append((request_snapshot, event))

    # Check if it's a scenario snapshot metadata path
    elif abs_path.startswith(scenarios_dir):
        scenario_snapshot = ScenarioSnapshot.from_path(abs_path, data_dir=data_dir, uuid=resource_uuid)
        if not scenario_snapshot:
            print(f"Error: Invalid scenario snapshot path format: {file_path}", file=sys.stderr)
            sys.exit(1)

        uuid = scenario_snapshot.uuid
        event = _find_event_by_resource_uuid(log, SCENARIO_RESOURCE, uuid)
        if not event:
            print(f"Error: No event found for scenario snapshot {uuid}", file=sys.stderr)
            sys.exit(1)

        if not no_verify:
            scenario_snapshot.iter_request_snapshots(_verify_request)

        scenario_snapshot.iter_request_snapshots(
            lambda snapshot: request_snapshots.append((snapshot, event))
        )
    else:
        print(f"Error: Path {file_path} is not a valid snapshot path", file=sys.stderr)
        sys.exit(1)

    snapshot_migrations = {}

    # Process request snapshots (for both request and scenario snapshots)
    if not lifecycle_hooks_path:
        snapshot_migrations = _apply_print(request_snapshots)
    else:
        snapshot_migrations = _apply_lifecycle_hooks(
            request_snapshots,
            lifecycle_hooks_path=lifecycle_hooks_path,
        )

    for snapshot_migration in snapshot_migrations.values():
        if snapshot_migration.skip:
            continue

        if action == PUT_ACTION: 
            if snapshot_migration.dirty:
                _commit_snapshot_migration(snapshot_migration)

            if with_snapshot:
                new_event = snapshot_migration.event.duplicate_as_put()
                log.append(str(new_event))
        elif action == DELETE_ACTION:
            if with_snapshot:
                new_event = snapshot_migration.event.duplicate_as_delete()
                log.append(str(new_event))

        # If the event is a scenario, only create new event once
        if snapshot_migration.event.is_scenario():
            with_snapshot = False

def _apply_lifecycle_hooks(
    request_snapshots: List[Tuple[RequestSnapshot, LogEvent]],
    lifecycle_hooks_path: str,
):
    """
    Iterate over request snapshots and apply lifecycle hooks.
    
    Args:
        request_snapshots: List of tuples (request_snapshot, event)
        lifecycle_hooks_path: Path to lifecycle hooks script
    """
    from runpy import run_path
    from stoobly_agent.config.constants.lifecycle_hooks import BEFORE_MIGRATE
    from stoobly_agent.app.cli.types.snapshot_migration import SnapshotMigration
    
    try:
        lifecycle_hooks = run_path(lifecycle_hooks_path)
    except Exception as e:
        print(f"Error: Failed to load lifecycle hooks from {lifecycle_hooks_path}: {e}", file=sys.stderr)
        lifecycle_hooks = {}
    
    before_migrate_hook: Callable[[SnapshotMigration], bool] = None
    if BEFORE_MIGRATE not in lifecycle_hooks:
        print(f"Error: Lifecycle hook {BEFORE_MIGRATE} not found in {lifecycle_hooks_path}", file=sys.stderr)
        sys.exit(1)
    else:
        before_migrate_hook = lifecycle_hooks[BEFORE_MIGRATE]
    
    snapshot_migrations = {}
    for request_snapshot, event in request_snapshots:
        if request_snapshot.uuid not in snapshot_migrations:
            snapshot_migration = SnapshotMigration(request_snapshot, event)
            snapshot_migrations[request_snapshot.uuid] = snapshot_migration
            
            if before_migrate_hook(snapshot_migration):
                snapshot_migration.skip = True

    return snapshot_migrations

def _apply_print(request_snapshots: List[Tuple[RequestSnapshot, LogEvent]]):
    from stoobly_agent.app.cli.types.snapshot_migration import SnapshotMigration

    snapshot_migrations: Dict[str, SnapshotMigration] = {}

    """Print the path to each request snapshot."""
    for request_snapshot, event in request_snapshots:
        snapshot_migrations[request_snapshot.uuid] = SnapshotMigration(request_snapshot, event)
        print(request_snapshot.path)

    return snapshot_migrations

def _find_event_by_resource_uuid(log: Log, resource: str, resource_uuid: str) -> LogEvent:
    """Find the most recent event for a given resource UUID (or scenario name identity)."""
    for event in reversed(log.target_events):
        if event.resource != resource:
            continue
        if event.resource_id == resource_uuid:
            return event
        # v2 scenarios: name/uuid or legacy name-only; match via snapshot / locator
        if resource == SCENARIO_RESOURCE:
            snapshot = event.snapshot()
            if snapshot.uuid == resource_uuid:
                return event
            # DELETE may have already removed YAML; match locator or legacy name
            from stoobly_agent.app.models.factories.resource.local_db.helpers.scenario_snapshot import (
              ScenarioSnapshotV2,
            )
            from stoobly_agent.lib.orm.scenario import Scenario
            scenario = Scenario.find_by(uuid=resource_uuid)
            if scenario:
              locator = ScenarioSnapshotV2.history_locator_for(
                scenario.uuid, scenario.name
              )
              if event.resource_uuid == locator:
                return event
              if event.resource_id == scenario.name or event.resource_uuid == scenario.name:
                return event

    # If resource is request and no event found, check if it belongs to a scenario event
    if resource == REQUEST_RESOURCE:
        for event in reversed(log.target_events):
            if event.resource != SCENARIO_RESOURCE:
                continue

            scenario_snapshot = event.snapshot()
            # Check if the request UUID is in this scenario's request snapshots
            for request_snapshot in scenario_snapshot.request_snapshots:
                if request_snapshot.uuid == resource_uuid:
                    return event

    return None

def _commit_snapshot_migration(snapshot_migration):
    """Save a snapshot migration by writing the request/response and optionally appending a new event."""
    from stoobly_agent.app.proxy.record.join_request_service import join_request_from_request_response
    
    request_uuid = snapshot_migration.snapshot.uuid
    joined_request = join_request_from_request_response(
        snapshot_migration.request, 
        snapshot_migration.response, 
        id=request_uuid
    )
    raw_request = joined_request.build()
    snapshot_migration.snapshot.write_raw(raw_request)
    
def _verify_request(snapshot: RequestSnapshot):
    """Verify and fix a request snapshot if needed."""
    from stoobly_agent.app.cli.helpers.verify_raw_request_service import verify_raw_request
    from stoobly_agent.app.models.factories.resource.local_db.helpers.request_snapshot import RequestSnapshotV2

    raw_request = snapshot.request
    if not raw_request:
        return

    verified_raw_request = verify_raw_request(raw_request)

    # Always rewrite v2 so on-disk form is normalized (strips trailing junk, re-externalizes bodies)
    if raw_request != verified_raw_request or isinstance(snapshot, RequestSnapshotV2):
        snapshot.write_raw(verified_raw_request)
