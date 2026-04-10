import pytest

from click.testing import CliRunner

from stoobly_agent.app.cli.request_cli import request
from stoobly_agent.app.cli.scenario_cli import scenario
from stoobly_agent.app.cli.snapshot_cli import snapshot
from stoobly_agent.cli import record
from stoobly_agent.lib.orm.request import Request
from stoobly_agent.lib.orm.scenario import Scenario
from stoobly_agent.test.test_helper import DETERMINISTIC_GET_REQUEST_URL, NON_DETERMINISTIC_GET_REQUEST_URL, reset

@pytest.fixture(scope='module')
def runner():
  return CliRunner()

@pytest.fixture(scope='class', autouse=True)
def settings():
  return reset()

class TestSnapshotResetConfirmation():
  @pytest.fixture(scope='class')
  def created_scenario(self, runner: CliRunner):
    create_result = runner.invoke(scenario, ['create', 'test'])
    assert create_result.exit_code == 0
    return Scenario.last()

  @pytest.fixture(scope='class', autouse=True)
  def recorded_requests(self, runner: CliRunner, created_scenario: Scenario):
    record_result = runner.invoke(record, ['--scenario-key', created_scenario.key(), DETERMINISTIC_GET_REQUEST_URL])
    assert record_result.exit_code == 0
    record_result = runner.invoke(record, ['--scenario-key', created_scenario.key(), NON_DETERMINISTIC_GET_REQUEST_URL])
    assert record_result.exit_code == 0
    return created_scenario.requests

  @pytest.fixture(scope='class', autouse=True)
  def snapshot_result(self, runner: CliRunner, created_scenario: Scenario):
    snapshot_result = runner.invoke(scenario, ['snapshot', 'create', created_scenario.key()])
    assert snapshot_result.exit_code == 0
    return snapshot_result

  def test_it_aborts_without_confirmation(self, runner: CliRunner, created_scenario: Scenario):
    # Delete one request to observe change if reset proceeds
    requests = created_scenario.requests
    assert len(requests) == 2
    deleted_request_uuid = requests[1].uuid
    requests[1].delete()
    assert Request.find_by(uuid=deleted_request_uuid) is None

    # Decline confirmation
    result = runner.invoke(snapshot, ['reset'], input='n\n')
    assert result.exit_code == 0
    # No changes: request remains deleted
    assert Request.find_by(uuid=deleted_request_uuid) is None

    # Accept confirmation
    result = runner.invoke(snapshot, ['reset'], input='y\n')
    assert result.exit_code == 0
    # Request restored from snapshot
    assert Request.find_by(uuid=deleted_request_uuid) is not None

class TestSnapshotResetYesFlag():
  @pytest.fixture(scope='class')
  def created_scenario(self, runner: CliRunner):
    create_result = runner.invoke(scenario, ['create', 'test-yes'])
    assert create_result.exit_code == 0
    return Scenario.last()

  @pytest.fixture(scope='class', autouse=True)
  def recorded_requests(self, runner: CliRunner, created_scenario: Scenario):
    record_result = runner.invoke(record, ['--scenario-key', created_scenario.key(), DETERMINISTIC_GET_REQUEST_URL])
    assert record_result.exit_code == 0
    record_result = runner.invoke(record, ['--scenario-key', created_scenario.key(), NON_DETERMINISTIC_GET_REQUEST_URL])
    assert record_result.exit_code == 0
    return created_scenario.requests

  @pytest.fixture(scope='class', autouse=True)
  def snapshot_result(self, runner: CliRunner, created_scenario: Scenario):
    snapshot_result = runner.invoke(scenario, ['snapshot', 'create', created_scenario.key()])
    assert snapshot_result.exit_code == 0
    return snapshot_result

  def test_it_resets_without_prompt(self, runner: CliRunner, created_scenario: Scenario):
    # Change then reset
    requests = created_scenario.requests
    assert len(requests) == 2
    deleted_request_uuid = requests[0].uuid
    requests[0].delete()
    assert Request.find_by(uuid=deleted_request_uuid) is None

    result = runner.invoke(snapshot, ['reset', '--yes'])
    assert result.exit_code == 0
    assert Request.find_by(uuid=deleted_request_uuid) is not None

class TestSnapshotResetHard():
  @pytest.fixture(scope='class')
  def primary_scenario(self, runner: CliRunner):
    create_result = runner.invoke(scenario, ['create', 'primary'])
    assert create_result.exit_code == 0
    return Scenario.last()

  @pytest.fixture(scope='class', autouse=True)
  def primary_requests(self, runner: CliRunner, primary_scenario: Scenario):
    record_result = runner.invoke(record, ['--scenario-key', primary_scenario.key(), DETERMINISTIC_GET_REQUEST_URL])
    assert record_result.exit_code == 0
    record_result = runner.invoke(record, ['--scenario-key', primary_scenario.key(), NON_DETERMINISTIC_GET_REQUEST_URL])
    assert record_result.exit_code == 0
    return primary_scenario.requests

  @pytest.fixture(scope='class', autouse=True)
  def primary_snapshot(self, runner: CliRunner, primary_scenario: Scenario):
    snapshot_result = runner.invoke(scenario, ['snapshot', 'create', primary_scenario.key()])
    assert snapshot_result.exit_code == 0
    return snapshot_result

  @pytest.fixture(scope='class')
  def extra_scenario(self, runner: CliRunner):
    create_result = runner.invoke(scenario, ['create', 'extra'])
    assert create_result.exit_code == 0
    return Scenario.last()

  @pytest.fixture(scope='class', autouse=True)
  def extra_request(self, runner: CliRunner):
    record_result = runner.invoke(record, [DETERMINISTIC_GET_REQUEST_URL])
    assert record_result.exit_code == 0
    return Request.last()

  def test_it_deletes_non_snapshot_resources_then_restores_snapshots(self, runner: CliRunner, primary_scenario: Scenario, extra_scenario: Scenario, extra_request: Request):
    # Sanity: resources exist
    assert Scenario.find(primary_scenario.id) is not None
    assert Scenario.find(extra_scenario.id) is not None
    extra_request_uuid = extra_request.uuid
    assert Request.find_by(uuid=extra_request_uuid) is not None

    # Hard reset
    result = runner.invoke(snapshot, ['reset', '--hard', '--yes'])
    assert result.exit_code == 0

    # Extra (non-snapshotted) scenario/request are removed
    assert Scenario.find(extra_scenario.id) is None
    assert Request.find_by(uuid=extra_request_uuid) is None

    # Primary scenario restored from snapshot
    restored = Scenario.find_by(uuid=primary_scenario.uuid)
    assert restored is not None
    assert len(restored.requests) == 2

