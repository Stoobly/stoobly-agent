import pdb
import pytest
import time

from click.testing import CliRunner

from stoobly_agent.app.models.adapters.joined_request_adapter import JoinedRequestAdapter
from stoobly_agent.app.models.adapters.raw_http_response_adapter import RawHttpResponseAdapter
from stoobly_agent.app.models.factories.resource.local_db.helpers.log import Log
from stoobly_agent.app.models.factories.resource.local_db.helpers.log_event import LogEvent
from stoobly_agent.cli import record, request, snapshot
from stoobly_agent.lib.orm.request import Request
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
      apply_result = runner.invoke(snapshot, ['update', put_event.uuid])
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

      apply_result = runner.invoke(snapshot, ['update', '--verify', put_event.uuid])
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