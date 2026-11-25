import os

import pytest
from click.testing import CliRunner

from stoobly_agent.app.cli.helpers.snapshot_format_service import get_snapshot_format
from stoobly_agent.app.models.factories.resource.local_db.helpers.log import Log
from stoobly_agent.app.models.factories.resource.local_db.helpers.log_event import LogEventV1, LogEventV2
from stoobly_agent.app.models.factories.resource.local_db.helpers.request_snapshot import (
  RequestSnapshot,
  RequestSnapshotV1,
  RequestSnapshotV2,
)
from stoobly_agent.app.models.factories.resource.local_db.helpers.scenario_snapshot import (
  ScenarioSnapshot,
  ScenarioSnapshotV1,
  ScenarioSnapshotV2,
)
from stoobly_agent.app.models.factories.resource.local_db.helpers.snapshot_format import (
  FORMAT_NONE,
  FORMAT_V1,
  FORMAT_V2,
  detect_snapshot_format,
  resolve_write_format,
)
from stoobly_agent.app.models.factories.resource.local_db.helpers.snapshot_service import (
  snapshot_request,
  snapshot_scenario,
)
from stoobly_agent.app.models.factories.resource.local_db.helpers.snapshot_types import PUT_ACTION
from stoobly_agent.app.cli.scenario_cli import scenario
from stoobly_agent.cli import record
from stoobly_agent.config.data_dir import DataDir
from stoobly_agent.lib.orm.request import Request
from stoobly_agent.lib.orm.scenario import Scenario
from stoobly_agent.test.test_helper import DETERMINISTIC_GET_REQUEST_URL, reset


@pytest.fixture(autouse=True)
def settings():
  return reset()


class TestRequestSnapshotV2Naming:
  def test_method_and_path(self):
    assert RequestSnapshotV2.build_request_slug('GET', '/api/users/1') == 'GET-api-users-1'

  def test_root_path(self):
    assert RequestSnapshotV2.build_request_slug('POST', '/') == 'POST'

  def test_rejects_dot_method(self):
    assert RequestSnapshotV2.build_request_slug('..', '/') == 'GET'
    assert RequestSnapshotV2.build_request_slug('.', '/') == 'GET'

  def test_rejects_method_with_separators(self):
    # Separators become '-', so join stays a single directory component
    assert RequestSnapshotV2.build_request_slug('GET/../x', '/') == 'GET-..-X'
    assert RequestSnapshotV2.build_request_slug('a\\b', '/') == 'A-B'
    assert '/' not in RequestSnapshotV2.build_request_slug('GET/evil', '/')
    assert '\\' not in RequestSnapshotV2.build_request_slug('GET\\evil', '/')

  def test_strips_whitespace_from_path(self):
    assert RequestSnapshotV2.build_request_slug('GET', '/api/foo bar') == 'GET-api-foo-bar'

  def test_relative_path_parse(self):
    assert RequestSnapshotV2.parse_request_relative_path('GET-api-users/abc.yaml') == ('GET-api-users', 'abc')

  def test_sanitize_scenario_name(self):
    assert ScenarioSnapshotV2.sanitize_scenario_filename('My Scenario!') == 'My Scenario!'
    assert ScenarioSnapshotV2.sanitize_scenario_filename('My-Scenario') == 'My-Scenario'
    assert ScenarioSnapshotV2.sanitize_scenario_filename('a/b') == 'a-b'


class TestSnapshotFormatDetect:
  def test_none_defaults_write_to_v2(self):
    data_dir = DataDir.instance()
    assert detect_snapshot_format(data_dir) == FORMAT_NONE
    assert resolve_write_format(data_dir) == FORMAT_V2

  def test_detects_v2_http(self):
    data_dir = DataDir.instance()
    requests_dir = data_dir.snapshots_requests_dir_path
    slug_dir = os.path.join(requests_dir, 'GET-api')
    os.makedirs(slug_dir, exist_ok=True)
    with open(os.path.join(slug_dir, '11111111-1111-1111-1111-111111111111.yaml'), 'wb') as fp:
      fp.write(b'x')

    assert detect_snapshot_format(data_dir) == FORMAT_V2
    assert resolve_write_format(data_dir) == FORMAT_V2

  def test_detects_v2_scenario_yaml(self):
    data_dir = DataDir.instance()
    scenarios_dir = data_dir.snapshots_scenarios_dir_path
    os.makedirs(scenarios_dir, exist_ok=True)
    with open(os.path.join(scenarios_dir, 'checkout.yaml'), 'w') as fp:
      fp.write('uuid: 11111111-1111-1111-1111-111111111111\n')

    assert detect_snapshot_format(data_dir) == FORMAT_V2
    assert resolve_write_format(data_dir) == FORMAT_V2

  def test_detects_v1_shard(self):
    data_dir = DataDir.instance()
    requests_dir = data_dir.snapshots_requests_dir_path
    shard = os.path.join(requests_dir, 'ab')
    os.makedirs(shard, exist_ok=True)
    with open(os.path.join(shard, 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa'), 'wb') as fp:
      fp.write(b'x')

    assert detect_snapshot_format(data_dir) == FORMAT_V1
    assert resolve_write_format(data_dir) == FORMAT_V1

  def test_detects_v1_scenario_uuid_file(self):
    data_dir = DataDir.instance()
    scenarios_dir = data_dir.snapshots_scenarios_dir_path
    os.makedirs(scenarios_dir, exist_ok=True)
    with open(os.path.join(scenarios_dir, 'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb'), 'w') as fp:
      fp.write('{"name":"legacy"}')

    assert detect_snapshot_format(data_dir) == FORMAT_V1
    assert resolve_write_format(data_dir) == FORMAT_V1

  def test_prefers_v2_when_both_present(self):
    data_dir = DataDir.instance()
    requests_dir = data_dir.snapshots_requests_dir_path

    shard = os.path.join(requests_dir, 'ab')
    os.makedirs(shard, exist_ok=True)
    with open(os.path.join(shard, 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa'), 'wb') as fp:
      fp.write(b'v1')

    slug_dir = os.path.join(requests_dir, 'GET-api')
    os.makedirs(slug_dir, exist_ok=True)
    with open(os.path.join(slug_dir, '11111111-1111-1111-1111-111111111111.yaml'), 'wb') as fp:
      fp.write(b'v2')

    assert detect_snapshot_format(data_dir) == FORMAT_V2
    assert resolve_write_format(data_dir) == FORMAT_V2

  def test_migrate_to_v2_overrides_detected_v1(self):
    data_dir = DataDir.instance()
    shard = os.path.join(data_dir.snapshots_requests_dir_path, 'ab')
    os.makedirs(shard, exist_ok=True)
    with open(os.path.join(shard, 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa'), 'wb') as fp:
      fp.write(b'x')

    assert detect_snapshot_format(data_dir) == FORMAT_V1
    assert resolve_write_format(data_dir, migrate_to_v2=True) == FORMAT_V2


class TestGetSnapshotFormat:
  def test_non_interactive_keeps_v1(self, monkeypatch):
    data_dir = DataDir.instance()
    shard = os.path.join(data_dir.snapshots_requests_dir_path, 'ab')
    os.makedirs(shard, exist_ok=True)
    with open(os.path.join(shard, 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa'), 'wb') as fp:
      fp.write(b'x')

    monkeypatch.setattr('stoobly_agent.app.cli.helpers.snapshot_format_service.sys.stdin.isatty', lambda: False)
    assert get_snapshot_format(data_dir, prompt=True) == FORMAT_V1

  def test_prompt_false_keeps_v1(self):
    data_dir = DataDir.instance()
    shard = os.path.join(data_dir.snapshots_requests_dir_path, 'ab')
    os.makedirs(shard, exist_ok=True)
    with open(os.path.join(shard, 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa'), 'wb') as fp:
      fp.write(b'x')

    assert get_snapshot_format(data_dir, prompt=False) == FORMAT_V1

  def test_empty_dir_writes_v2(self):
    assert get_snapshot_format(DataDir.instance(), prompt=False) == FORMAT_V2


class TestWriteFormatFollowsDetection:
  """
  snapshot_request / snapshot_scenario without format= must use resolve_write_format
  and write matching on-disk layout + history locator class.
  """

  @pytest.fixture
  def runner(self):
    return CliRunner()

  @pytest.fixture
  def recorded_request(self, runner: CliRunner):
    assert runner.invoke(record, [DETERMINISTIC_GET_REQUEST_URL]).exit_code == 0
    return Request.last()

  @pytest.fixture
  def created_scenario(self, runner: CliRunner, recorded_request: Request):
    assert runner.invoke(scenario, ['create', 'format-policy']).exit_code == 0
    created = Scenario.last()
    recorded_request.update(scenario_id=created.id)
    return created

  def test_empty_dir_writes_request_v2(self, recorded_request: Request):
    assert detect_snapshot_format(DataDir.instance()) == FORMAT_NONE

    path = snapshot_request(recorded_request, action=PUT_ACTION)
    snap = RequestSnapshot.create(recorded_request.uuid)

    assert isinstance(snap, RequestSnapshotV2)
    assert snap.format == FORMAT_V2
    assert path == snap.path
    assert path.endswith('.yaml')
    assert detect_snapshot_format(DataDir.instance()) == FORMAT_V2

    event = Log().events[-1]
    assert isinstance(event, LogEventV2)
    assert '/' in event.resource_uuid
    assert event.resource_id == recorded_request.uuid

  def test_existing_v1_keeps_writing_request_v1(self, recorded_request: Request):
    snapshot_request(recorded_request, action=PUT_ACTION, format=FORMAT_V1)
    assert detect_snapshot_format(DataDir.instance()) == FORMAT_V1
    assert resolve_write_format(DataDir.instance()) == FORMAT_V1

    # Second create with no explicit format must stay on v1
    path = snapshot_request(recorded_request, action=PUT_ACTION)
    snap = RequestSnapshot.create(recorded_request.uuid)

    assert isinstance(snap, RequestSnapshotV1)
    assert snap.format == FORMAT_V1
    assert path == snap.path
    assert not path.endswith('.yaml')
    assert detect_snapshot_format(DataDir.instance()) == FORMAT_V1

    event = Log().events[-1]
    assert isinstance(event, LogEventV1)
    assert event.resource_uuid == recorded_request.uuid

  def test_existing_v2_keeps_writing_request_v2(self, recorded_request: Request):
    snapshot_request(recorded_request, action=PUT_ACTION)  # empty -> v2
    assert detect_snapshot_format(DataDir.instance()) == FORMAT_V2

    path = snapshot_request(recorded_request, action=PUT_ACTION)
    snap = RequestSnapshot.create(recorded_request.uuid)

    assert isinstance(snap, RequestSnapshotV2)
    assert path.endswith('.yaml')
    assert isinstance(Log().events[-1], LogEventV2)

  def test_existing_v1_keeps_writing_scenario_v1(self, created_scenario: Scenario, recorded_request: Request):
    snapshot_scenario(created_scenario, action=PUT_ACTION, format=FORMAT_V1)
    assert detect_snapshot_format(DataDir.instance()) == FORMAT_V1

    path = snapshot_scenario(created_scenario, action=PUT_ACTION)
    snap = ScenarioSnapshot.create(created_scenario.uuid)

    assert isinstance(snap, ScenarioSnapshotV1)
    assert snap.format == FORMAT_V1
    assert path == snap.metadata_path
    assert not path.endswith('.yaml')

    event = Log().events[-1]
    assert isinstance(event, LogEventV1)
    assert event.resource_uuid == created_scenario.uuid

  def test_existing_v2_keeps_writing_scenario_v2(self, created_scenario: Scenario):
    snapshot_scenario(created_scenario, action=PUT_ACTION)  # empty -> v2
    assert detect_snapshot_format(DataDir.instance()) == FORMAT_V2

    path = snapshot_scenario(created_scenario, action=PUT_ACTION)
    snap = ScenarioSnapshot.create(created_scenario.uuid)

    assert isinstance(snap, ScenarioSnapshotV2)
    assert path.endswith('.yaml')
    assert isinstance(Log().events[-1], LogEventV2)
    stem = ScenarioSnapshotV2.sanitize_scenario_filename(created_scenario.name)
    assert Log().events[-1].resource_uuid == f'{stem}/{created_scenario.uuid}'
    assert Log().events[-1].resource_id == created_scenario.uuid
