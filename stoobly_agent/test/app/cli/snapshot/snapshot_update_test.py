import os
import pdb
import pytest
import time

from click.testing import CliRunner

from stoobly_agent.app.cli.request_cli import request
from stoobly_agent.app.cli.scenario_cli import scenario
from stoobly_agent.app.cli.snapshot_cli import snapshot
from stoobly_agent.app.models.adapters.joined_request_adapter import JoinedRequestAdapter
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

class TestUpdate():
  @pytest.fixture(scope='class', autouse=True)
  def settings(self):
    return reset()

  class TestEventColumns():

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
    def updated_event(self, runner: CliRunner, put_event: LogEvent):
      time.sleep(1) # Simulate update at different time
      
      # Get the snapshot file path from the event
      request_snapshot = put_event.snapshot()
      if put_event.is_request():
        file_path = request_snapshot.path
      else:
        file_path = request_snapshot.metadata_path
      
      apply_result = runner.invoke(snapshot, ['update', file_path])
      assert apply_result.exit_code == 0
      log = Log()
      events = log.events
      assert len(events) == 2
      return events[1]

    def test_it_has_different_uuid(self, updated_event: LogEvent, put_event: LogEvent):
      assert updated_event.uuid != put_event.uuid 

    def test_it_has_same_action(self, updated_event: LogEvent, put_event: LogEvent):
      assert updated_event.action == put_event.action

    def test_it_has_same_resource(self, updated_event: LogEvent, put_event: LogEvent):
      assert updated_event.resource == put_event.resource

    def test_it_has_same_resource_uuid(self, updated_event: LogEvent, put_event: LogEvent):
      assert updated_event.resource_uuid == put_event.resource_uuid

    def test_it_has_different_created_at(self, updated_event: LogEvent, put_event: LogEvent):
      assert updated_event.created_at != put_event.created_at

  class TestVerifyOption():

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
    def snapshot_contents(self, put_event: LogEvent):
      snapshot = put_event.snapshot()
      data_path = snapshot.path
      with open(data_path, 'ab') as fp:
        fp.write(b'test')

      with open(data_path, 'rb') as fp:
        return fp.read()

    @pytest.fixture(autouse=True, scope='class')
    def updated_event(self, runner: CliRunner, put_event: LogEvent):
      time.sleep(1) # Simulate update at different time

      # Get the snapshot file path from the event
      request_snapshot = put_event.snapshot()
      if put_event.is_request():
        file_path = request_snapshot.path
      else:
        file_path = request_snapshot.metadata_path

      apply_result = runner.invoke(snapshot, ['update', file_path])
      assert apply_result.exit_code == 0
      log = Log()
      events = log.events
      assert len(events) == 2
      return events[1]

    def test_it_updates_snapshot_contents(self, snapshot_contents: str, updated_event: LogEvent):
      snapshot = updated_event.snapshot()
      data_path = snapshot.path

      with open(data_path, 'rb') as fp:
        contents = fp.read()
        new_response = self.__to_python_response(contents)
        content_length = str(len(new_response.content)).encode()

        assert content_length in contents
        assert content_length not in snapshot_contents

    def __to_python_response(self, raw_request):
      adapter = JoinedRequestAdapter(raw_request)
      response_string = adapter.build_response_string().get()
      return RawHttpResponseAdapter(response_string).to_response()

  class TestWithLifecycleHooks():

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
      
      # Get the snapshot file path from the event
      request_snapshot = put_event.snapshot()
      if put_event.is_request():
        file_path = request_snapshot.path
      else:
        file_path = request_snapshot.metadata_path
      
      migrate_result = runner.invoke(snapshot, ['update', '--lifecycle-hooks-path', lifecycle_hooks_path, file_path], catch_exceptions=False)
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

  class TestWithLifecycleHooksAndScenario():

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
      
      # Get the scenario snapshot metadata path from the event
      scenario_snapshot = put_event.snapshot()
      file_path = scenario_snapshot.metadata_path
      
      migrate_result = runner.invoke(snapshot, 
        ['update', '--lifecycle-hooks-path', lifecycle_hooks_path, file_path]
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
