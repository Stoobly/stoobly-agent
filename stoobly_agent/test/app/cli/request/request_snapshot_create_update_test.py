import pytest
from click.testing import CliRunner

from stoobly_agent.app.cli.request_cli import request
from stoobly_agent.app.models.factories.resource.local_db.helpers.log import Log
from stoobly_agent.app.models.factories.resource.local_db.helpers.log_event import DELETE_ACTION
from stoobly_agent.app.models.factories.resource.local_db.helpers.request_snapshot import RequestSnapshot
from stoobly_agent.cli import record
from stoobly_agent.lib.orm.request import Request
from stoobly_agent.test.test_helper import DETERMINISTIC_GET_REQUEST_URL, reset


@pytest.fixture
def runner():
  return CliRunner()


@pytest.fixture(autouse=True)
def _reset():
  return reset('stoobly-agent-test-request-snapshot-create-update')


@pytest.fixture
def recorded_request(runner: CliRunner):
  record_result = runner.invoke(record, [DETERMINISTIC_GET_REQUEST_URL])
  assert record_result.exit_code == 0
  return Request.last()


class TestRequestSnapshotCreateWithoutKey:
  def test_create_without_key_snapshots_unsnapshotted(self, runner: CliRunner, recorded_request: Request):
    assert not RequestSnapshot.create(recorded_request.uuid).exists

    result = runner.invoke(request, ['snapshot', 'create'])
    assert result.exit_code == 0

    snapshot = RequestSnapshot.create(recorded_request.uuid)
    assert snapshot.exists
    assert snapshot.path in result.stdout

  def test_create_without_key_skips_already_snapshotted(self, runner: CliRunner, recorded_request: Request):
    first = runner.invoke(request, ['snapshot', 'create', recorded_request.key()])
    assert first.exit_code == 0

    log = Log()
    before = len(log.raw_events)

    result = runner.invoke(request, ['snapshot', 'create'])
    assert result.exit_code == 0
    assert result.stdout.strip() == ''

    log = Log()
    assert len(log.raw_events) == before

  def test_create_without_key_rejects_delete(self, runner: CliRunner, recorded_request: Request):
    log = Log()
    before = len(log.raw_events)

    result = runner.invoke(request, ['snapshot', 'create', '--action', DELETE_ACTION])
    assert result.exit_code != 0
    assert 'DELETE requires a request key' in result.output

    log = Log()
    assert len(log.raw_events) == before
    assert not RequestSnapshot.create(recorded_request.uuid).exists


class TestRequestSnapshotUpdate:
  def test_update_without_diff_is_noop(self, runner: CliRunner, recorded_request: Request):
    snap = runner.invoke(request, ['snapshot', 'create', recorded_request.key()])
    assert snap.exit_code == 0

    log = Log()
    before = len(log.raw_events)

    result = runner.invoke(request, ['snapshot', 'update'])
    assert result.exit_code == 0

    log = Log()
    assert len(log.raw_events) == before

  def test_update_with_diff_rewrites_snapshot(self, runner: CliRunner, recorded_request: Request):
    snap = runner.invoke(request, ['snapshot', 'create', recorded_request.key()])
    assert snap.exit_code == 0

    current = Request.find(recorded_request.id)
    assert current.response is not None
    current.response.raw = b'HTTP/1.1 502\r\nContent-Length: 4\r\n\r\nnope'
    current.response.save()

    log = Log()
    before = len(log.raw_events)

    result = runner.invoke(request, ['snapshot', 'update', recorded_request.key()])
    assert result.exit_code == 0

    log = Log()
    assert len(log.raw_events) == before + 1

    result = runner.invoke(request, ['snapshot', 'diff', '--request-key', recorded_request.key(), '--full'])
    assert result.exit_code == 0
    assert '~ Response body' not in result.output
