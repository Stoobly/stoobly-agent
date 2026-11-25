import os
from unittest.mock import patch

import pytest
import yaml

from stoobly_agent.app.cli.helpers.update_request_snapshots_service import (
  update_request_snapshots,
)
from stoobly_agent.app.models.adapters.raw_joined import SnapshotEntryAdapter
from stoobly_agent.app.models.factories.resource.local_db.helpers.log import Log
from stoobly_agent.app.models.factories.resource.local_db.helpers.log_event import (
  LogEventV2,
  PUT_ACTION,
  SCENARIO_RESOURCE,
)
from stoobly_agent.app.models.factories.resource.local_db.helpers.request_snapshot import (
  RequestSnapshotV2,
)
from stoobly_agent.app.models.factories.resource.local_db.helpers.scenario_snapshot import (
  ScenarioSnapshotV2,
)
from stoobly_agent.app.proxy.record.joined_request import REQUEST_DELIMITTER
from stoobly_agent.config.data_dir import DataDir
from stoobly_agent.test.test_helper import reset

REQUEST_UUID = 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa'
SCENARIO_UUID = 'dddddddd-dddd-dddd-dddd-dddddddddddd'


@pytest.fixture(autouse=True)
def settings():
  return reset()


def _joined(marker: bytes = b'') -> bytes:
  # Absolute-form URL so mitmproxy_request (lifecycle path) has a hostname.
  request = b'GET http://example.com/api HTTP/1.1\r\nHost: example.com\r\n\r\n' + marker
  response = b'HTTP/1.1 200\r\nContent-Length: 0\r\n\r\n'
  return REQUEST_DELIMITTER.join([
    f'1 {REQUEST_UUID} 1\r\n'.encode() + request,
    f'2 {REQUEST_UUID} 1 1\r\n'.encode() + response,
  ])


def _write_scenario_with_embed(joined: bytes) -> str:
  data_dir = DataDir.instance()
  slug = RequestSnapshotV2.build_request_slug('GET', '/api')
  slug_dir = os.path.join(data_dir.snapshots_requests_dir_path, slug)
  os.makedirs(slug_dir, exist_ok=True)
  entry = SnapshotEntryAdapter.from_joined(joined, slug_dir).adapt()

  scenarios_dir = data_dir.snapshots_scenarios_dir_path
  os.makedirs(scenarios_dir, exist_ok=True)
  yaml_path = os.path.join(scenarios_dir, 'checkout.yaml')
  with open(yaml_path, 'w') as fp:
    yaml.safe_dump({
      'uuid': SCENARIO_UUID,
      'description': '',
      'requests': {REQUEST_UUID: entry},
    }, fp, sort_keys=False)

  Log().append(
    LogEventV2.serialize(SCENARIO_RESOURCE, f'checkout/{SCENARIO_UUID}', PUT_ACTION)
  )
  return yaml_path


class TestUpdateRequestSnapshotsEmbedVerify:
  def test_persists_verified_embed_into_scenario_yaml(self):
    original = _joined(b'')
    verified = _joined(b'changed')
    yaml_path = _write_scenario_with_embed(original)

    with open(yaml_path, 'r') as fp:
      before = yaml.safe_load(fp)
    original_entry = before['requests'][REQUEST_UUID]

    with patch(
      'stoobly_agent.app.cli.helpers.verify_raw_request_service.verify_raw_request',
      return_value=verified,
    ):
      update_request_snapshots(yaml_path, no_verify=False, with_snapshot=False)

    with open(yaml_path, 'r') as fp:
      after = yaml.safe_load(fp)

    updated_entry = after['requests'][REQUEST_UUID]
    assert updated_entry != original_entry

    # No standalone request yaml for scenario embeds
    slug = RequestSnapshotV2.build_request_slug('GET', '/api')
    slug_dir = os.path.join(DataDir.instance().snapshots_requests_dir_path, slug)
    standalone = os.path.join(slug_dir, f'{REQUEST_UUID}.yaml')
    assert not os.path.isfile(standalone)

    # Disk embed matches what verify wrote (entry form after externalize)
    expected_entry = SnapshotEntryAdapter.from_joined(verified, slug_dir).adapt()
    assert updated_entry == expected_entry

    snap = ScenarioSnapshotV2(SCENARIO_UUID, DataDir.instance(), name='checkout')
    reloaded = []
    snap.iter_request_snapshots(lambda s: reloaded.append(s.request))
    assert len(reloaded) == 1
    assert b'changed' in reloaded[0]

  def test_in_place_mutation_keeps_shared_entry_identity(self):
    from stoobly_agent.app.cli.helpers.update_request_snapshots_service import (
      _verify_request,
    )

    original = _joined(b'')
    verified = _joined(b'changed')
    yaml_path = _write_scenario_with_embed(original)

    with open(yaml_path, 'r') as fp:
      data = yaml.safe_load(fp)
    entry = data['requests'][REQUEST_UUID]
    entry_id = id(entry)

    snapshot = RequestSnapshotV2.from_entry(
      entry, DataDir.instance(), uuid=REQUEST_UUID
    )

    with patch(
      'stoobly_agent.app.cli.helpers.verify_raw_request_service.verify_raw_request',
      return_value=verified,
    ):
      assert _verify_request(snapshot) is True

    assert id(snapshot._entry) == entry_id
    assert snapshot._entry is entry
    assert data['requests'][REQUEST_UUID] is entry


class TestUpdateRequestSnapshotsEmbedLifecycle:
  def test_dirty_lifecycle_persists_embed_without_standalone(self, tmp_path):
    """
    Dirty lifecycle commits must update the scenario embed map in place.

    write_raw() would create a forbidden requests/<slug>/<uuid>.yaml that
    migrate later deletes, leaving the stale embed — edits would be lost.
    """
    original = _joined(b'')
    yaml_path = _write_scenario_with_embed(original)

    with open(yaml_path, 'r') as fp:
      before = yaml.safe_load(fp)
    original_entry = before['requests'][REQUEST_UUID]

    hooks_path = tmp_path / 'lifecycle_hooks_visit.py'
    hooks_path.write_text(
      "from stoobly_agent.app.cli.types.snapshot_migration import SnapshotMigration\n"
      "\n"
      "def handle_snapshot_visit(snapshot_migration: SnapshotMigration):\n"
      "  request = snapshot_migration.request\n"
      "  response = snapshot_migration.response\n"
      "  request.headers['X-Test'] = '1'\n"
      "  response.content = b'Test'\n"
      "  snapshot_migration.request = request\n"
      "  snapshot_migration.response = response\n"
    )

    update_request_snapshots(
      yaml_path,
      lifecycle_hooks_path=str(hooks_path),
      no_verify=True,
      with_snapshot=False,
    )

    with open(yaml_path, 'r') as fp:
      after = yaml.safe_load(fp)

    updated_entry = after['requests'][REQUEST_UUID]
    assert updated_entry != original_entry

    slug = RequestSnapshotV2.build_request_slug('GET', '/api')
    slug_dir = os.path.join(DataDir.instance().snapshots_requests_dir_path, slug)
    standalone = os.path.join(slug_dir, f'{REQUEST_UUID}.yaml')
    assert not os.path.isfile(standalone)

    snap = ScenarioSnapshotV2(SCENARIO_UUID, DataDir.instance(), name='checkout')
    reloaded = []
    snap.iter_request_snapshots(lambda s: reloaded.append(s))
    assert len(reloaded) == 1
    assert reloaded[0].mitmproxy_request.headers.get('X-Test') == '1'
    assert reloaded[0].mitmproxy_response.content == b'Test'
