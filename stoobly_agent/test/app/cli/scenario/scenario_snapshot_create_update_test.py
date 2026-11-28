import pytest
from click.testing import CliRunner

from stoobly_agent.app.cli.scenario_cli import scenario
from stoobly_agent.app.models.factories.resource.local_db.helpers.log import Log
from stoobly_agent.app.models.factories.resource.local_db.helpers.scenario_snapshot import ScenarioSnapshot
from stoobly_agent.cli import record
from stoobly_agent.lib.orm.request import Request
from stoobly_agent.lib.orm.scenario import Scenario
from stoobly_agent.test.test_helper import DETERMINISTIC_GET_REQUEST_URL, reset


@pytest.fixture
def runner():
  return CliRunner()


@pytest.fixture(autouse=True)
def _reset():
  return reset('stoobly-agent-test-scenario-snapshot-create-update')


@pytest.fixture
def created_scenario(runner: CliRunner):
  create_result = runner.invoke(scenario, ['create', 'bulk-create'])
  assert create_result.exit_code == 0
  return Scenario.last()


@pytest.fixture
def recorded_request(runner: CliRunner, created_scenario: Scenario):
  record_result = runner.invoke(
    record, ['--scenario-key', created_scenario.key(), DETERMINISTIC_GET_REQUEST_URL]
  )
  assert record_result.exit_code == 0
  return Request.last()


class TestScenarioSnapshotCreateWithoutKey:
  def test_create_without_key_snapshots_unsnapshotted(
    self, runner: CliRunner, created_scenario: Scenario, recorded_request: Request
  ):
    assert not ScenarioSnapshot.create(created_scenario.uuid).exists

    result = runner.invoke(scenario, ['snapshot', 'create'])
    assert result.exit_code == 0, result.output
    assert result.stdout.strip() != ''

    snapshot = ScenarioSnapshot.create(created_scenario.uuid)
    assert snapshot.exists

  def test_create_without_key_skips_already_snapshotted(
    self, runner: CliRunner, created_scenario: Scenario, recorded_request: Request
  ):
    first = runner.invoke(scenario, ['snapshot', 'create'])
    assert first.exit_code == 0

    log = Log()
    before = len(log.raw_events)

    result = runner.invoke(scenario, ['snapshot', 'create'])
    assert result.exit_code == 0
    assert result.stdout.strip() == ''

    log = Log()
    assert len(log.raw_events) == before


class TestScenarioSnapshotUpdate:
  def test_update_without_diff_is_noop(
    self, runner: CliRunner, created_scenario: Scenario, recorded_request: Request
  ):
    snap = runner.invoke(scenario, ['snapshot', 'create', created_scenario.key()])
    assert snap.exit_code == 0

    log = Log()
    before = len(log.raw_events)

    result = runner.invoke(scenario, ['snapshot', 'update'])
    assert result.exit_code == 0

    log = Log()
    assert len(log.raw_events) == before

  def test_update_with_metadata_diff_rewrites_snapshot(
    self, runner: CliRunner, created_scenario: Scenario, recorded_request: Request
  ):
    snap = runner.invoke(scenario, ['snapshot', 'create', created_scenario.key()])
    assert snap.exit_code == 0

    created_scenario.update({'name': 'bulk-update-renamed'})
    created_scenario = Scenario.find(created_scenario.id)
    assert created_scenario is not None

    log = Log()
    before = len(log.raw_events)

    result = runner.invoke(scenario, ['snapshot', 'update', created_scenario.key()])
    assert result.exit_code == 0

    log = Log()
    assert len(log.raw_events) == before + 1

    snapshot = ScenarioSnapshot.create(created_scenario.uuid)
    assert snapshot.metadata.get('name') == 'bulk-update-renamed'
