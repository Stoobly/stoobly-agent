"""Tests for snapshot list search matching."""

import uuid
from unittest.mock import MagicMock

import pytest

from stoobly_agent.app.cli.helpers.snapshot_list_service import (
    _resolve_scenario_uuid,
    _scenario_key_filter_matches,
    _scenario_snapshot_search_matches,
)
from stoobly_agent.app.models.factories.resource.local_db.helpers.log_event import LogEvent
from stoobly_agent.app.models.factories.resource.local_db.helpers.snapshot_types import (
    PUT_ACTION,
    SCENARIO_RESOURCE,
)
from stoobly_agent.lib.api.keys.project_key import LOCAL_PROJECT_ID
from stoobly_agent.lib.api.keys.scenario_key import ScenarioKey


@pytest.mark.parametrize(
    'name, description, pattern, expected',
    [
        ('My TEST scenario', '', 'TEST', True),
        ('', 'contains TEST here', 'TEST', True),
        ('Other', 'no match', 'TEST', False),
        ('', '', 'TEST', False),
        ('', '', '', True),
    ],
)
def test_scenario_snapshot_search_matches(name, description, pattern, expected):
    snapshot = MagicMock()
    snapshot.metadata = {'name': name, 'description': description}
    assert _scenario_snapshot_search_matches(snapshot, pattern or None) == expected


def test_resolve_scenario_uuid_from_encoded_key():
    su = str(uuid.uuid4())
    encoded = ScenarioKey.encode(LOCAL_PROJECT_ID, su)
    assert _resolve_scenario_uuid(encoded) == su


def test_resolve_scenario_uuid_rejects_plain_uuid():
    su = str(uuid.uuid4())
    assert _resolve_scenario_uuid(su) is None


def test_resolve_scenario_uuid_invalid():
    assert _resolve_scenario_uuid('not-a-valid-key') is None


def test_scenario_key_filter_matches_event():
    su = str(uuid.uuid4())
    encoded = ScenarioKey.encode(LOCAL_PROJECT_ID, su)
    line = f"00000000-0000-0000-0000-000000000001 {SCENARIO_RESOURCE} {su} {PUT_ACTION} 0"
    event = LogEvent(line)
    assert _scenario_key_filter_matches(event, encoded) is True
    assert _scenario_key_filter_matches(event, su) is False
    assert _scenario_key_filter_matches(event, str(uuid.uuid4())) is False
    assert _scenario_key_filter_matches(event, None) is True
