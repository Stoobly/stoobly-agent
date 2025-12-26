import os
import pdb
import pytest
import time

from click.testing import CliRunner

from stoobly_agent.app.cli.request_cli import request
from stoobly_agent.app.cli.scenario_cli import scenario
from stoobly_agent.app.cli.snapshot_cli import snapshot
from stoobly_agent.app.models.adapters.raw_http_request_adapter import RawHttpRequestAdapter
from stoobly_agent.app.models.adapters.raw_http_response_adapter import RawHttpResponseAdapter
from stoobly_agent.app.models.factories.resource.local_db.helpers.log import Log
from stoobly_agent.app.models.factories.resource.local_db.helpers.log_event import LogEvent
from stoobly_agent.cli import record
from stoobly_agent.lib.orm.request import Request
from stoobly_agent.lib.orm.scenario import Scenario
from stoobly_agent.test.test_helper import DETERMINISTIC_GET_REQUEST_URL, reset

@pytest.fixture(scope='module')
def runner():
  return CliRunner()

class TestMigrate():
  @pytest.fixture(scope='class', autouse=True)
  def settings(self):
    return reset()

  class TestWithoutScenarioKey():

    @pytest.fixture(scope='class')
    def recorded_request(self, runner: CliRunner):
      record_result = runner.invoke(record, [DETERMINISTIC_GET_REQUEST_URL])
      assert record_result.exit_code == 0
      return Request.last()

    @pytest.fixture(autouse=True, scope='class')
    def put_event(self, runner: CliRunner, recorded_request: Request):
      snapshot_result = runner.invoke(request, ['snapshot', recorded_request.key()])
      assert snapshot_result.exit_code == 0

      log = Log()
      events = log.events
      return events[len(events) - 1]

    @pytest.fixture(autouse=True, scope='class')
    def migrated_event(self, runner: CliRunner, put_event: LogEvent):
      time.sleep(1) # Simulate update at different time

      current_dir = os.path.dirname(os.path.abspath(__file__))
      lifecycle_hooks_path = os.path.join(current_dir, 'lifecycle_hooks_migrate.py')
      migrate_result = runner.invoke(snapshot, ['migrate', lifecycle_hooks_path], catch_exceptions=False)
      assert migrate_result.exit_code == 0

      log = Log()
      events = log.events
      assert len(events) == 2
      assert events[0].uuid == put_event.uuid
      return events[1]

    @pytest.fixture(scope='class')
    def migrated_request(self, runner: CliRunner, recorded_request: Request):
      apply_result = runner.invoke(snapshot, ['apply'], catch_exceptions=False)
      assert apply_result.exit_code == 0

      request = Request.find(recorded_request.id)
      assert request != None

      return request

    def test_it_has_different_uuid(self, migrated_event: LogEvent, put_event: LogEvent):
      assert migrated_event.uuid != put_event.uuid 

    def test_it_has_same_action(self, migrated_event: LogEvent, put_event: LogEvent):
      assert migrated_event.action == put_event.action

    def test_it_has_same_resource(self, migrated_event: LogEvent, put_event: LogEvent):
      assert migrated_event.resource == put_event.resource

    def test_it_has_same_resource_uuid(self, migrated_event: LogEvent, put_event: LogEvent):
      assert migrated_event.resource_uuid == put_event.resource_uuid

    def test_it_has_different_created_at(self, migrated_event: LogEvent, put_event: LogEvent):
      assert migrated_event.created_at != put_event.created_at

    def test_it_migrates_request(self, migrated_request: Request):
      python_request = RawHttpRequestAdapter(migrated_request.raw).to_request()
      assert python_request.headers['X-Test'] == '1'

    def test_it_migrates_response(self, migrated_request: Request):
      python_response = RawHttpResponseAdapter(migrated_request.response.raw).to_response()
      assert python_response.content == b'Test'

  class TestWithScenarioKey():

    @pytest.fixture(scope='class')
    def created_scenario(self, runner: CliRunner):
        create_result = runner.invoke(scenario, ['create', 'test'])
        assert create_result.exit_code == 0
        return Scenario.last()

    @pytest.fixture(scope='class')
    def recorded_request_one(self, runner: CliRunner, created_scenario: Scenario):
      record_result = runner.invoke(record, ['--scenario-key', created_scenario.key(), DETERMINISTIC_GET_REQUEST_URL])
      assert record_result.exit_code == 0
      return Request.last()

    @pytest.fixture(scope='class')
    def recorded_request_two(self, runner: CliRunner):
      record_result = runner.invoke(record, [DETERMINISTIC_GET_REQUEST_URL])
      assert record_result.exit_code == 0
      return Request.last()

    @pytest.fixture(autouse=True, scope='class')
    def put_event(self, runner: CliRunner, recorded_request_one: Request):
      snapshot_result = runner.invoke(scenario, ['snapshot', recorded_request_one.scenario.key()])
      assert snapshot_result.exit_code == 0

      log = Log()
      events = log.events
      return events[len(events) - 1]

    @pytest.fixture(autouse=True, scope='class')
    def put_event_two(self, runner: CliRunner, recorded_request_two: Request):
      snapshot_result = runner.invoke(request, ['snapshot', recorded_request_two.key()])
      assert snapshot_result.exit_code == 0

      log = Log()
      events = log.events
      return events[len(events) - 1]

    @pytest.fixture(autouse=True, scope='class')
    def migrated_event(
      self, runner: CliRunner, put_event: LogEvent, put_event_two: LogEvent, created_scenario: Scenario
    ):
      time.sleep(1) # Simulate update at different time

      current_dir = os.path.dirname(os.path.abspath(__file__))
      lifecycle_hooks_path = os.path.join(current_dir, 'lifecycle_hooks_migrate.py')
      migrate_result = runner.invoke(snapshot, 
        ['migrate', '--scenario-key', created_scenario.key(), lifecycle_hooks_path]
      )
      assert migrate_result.exit_code == 0

      log = Log()
      events = log.events

      assert len(events) == 3
      assert events[0].uuid == put_event.uuid
      assert events[1].uuid == put_event_two.uuid
      return events[2]

    @pytest.fixture(scope='class')
    def migrated_request(self, runner: CliRunner, recorded_request_one: Request):
      apply_result = runner.invoke(snapshot, ['apply'], catch_exceptions=False)
      assert apply_result.exit_code == 0

      request = Request.find(recorded_request_one.id)
      assert request != None

      return request

    def test_it_has_different_uuid(self, migrated_event: LogEvent, put_event: LogEvent):
      assert migrated_event.uuid != put_event.uuid 

    def test_it_has_same_action(self, migrated_event: LogEvent, put_event: LogEvent):
      assert migrated_event.action == put_event.action

    def test_it_has_same_resource(self, migrated_event: LogEvent, put_event: LogEvent):
      assert migrated_event.resource == put_event.resource

    def test_it_has_same_resource_uuid(self, migrated_event: LogEvent, put_event: LogEvent):
      assert migrated_event.resource_uuid == put_event.resource_uuid

    def test_it_has_different_created_at(self, migrated_event: LogEvent, put_event: LogEvent):
      assert migrated_event.created_at != put_event.created_at

    def test_it_migrates_request(self, migrated_request: Request):
      python_request = RawHttpRequestAdapter(migrated_request.raw).to_request()
      assert python_request.headers['X-Test'] == '1'

    def test_it_migrates_response(self, migrated_request: Request):
      python_response = RawHttpResponseAdapter(migrated_request.response.raw).to_response()
      assert python_response.content == b'Test'