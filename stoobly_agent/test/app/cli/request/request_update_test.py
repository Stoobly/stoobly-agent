import pytest

from click.testing import CliRunner

from stoobly_agent.app.cli.request_cli import request
from stoobly_agent.app.models.adapters.raw_http_request_adapter import RawHttpRequestAdapter
from stoobly_agent.cli import record
from stoobly_agent.lib.orm.request import Request
from stoobly_agent.lib.orm.scenario import Scenario
from stoobly_agent.test.test_helper import DETERMINISTIC_GET_REQUEST_URL, reset


@pytest.fixture(scope='module')
def runner():
  return CliRunner()


@pytest.fixture(autouse=True, scope='module')
def settings():
  return reset()


class TestUpdate:

  @pytest.fixture(autouse=True, scope='class')
  def recorded_request(self, runner: CliRunner):
    record_result = runner.invoke(record, [DETERMINISTIC_GET_REQUEST_URL])
    assert record_result.exit_code == 0
    return Request.last()

  def test_it_requires_an_update_option(self, runner: CliRunner, recorded_request: Request):
    result = runner.invoke(request, ['update', recorded_request.key()])
    assert result.exit_code == 1
    assert 'At least one update option is required' in result.output

  def test_it_rejects_invalid_request_key(self, runner: CliRunner):
    result = runner.invoke(request, ['update', 'p0.rINVALID', '--path', '/new-path'])
    assert result.exit_code == 1


class TestUpdatePath:

  @pytest.fixture(autouse=True, scope='class')
  def recorded_request(self, runner: CliRunner):
    record_result = runner.invoke(record, [DETERMINISTIC_GET_REQUEST_URL])
    assert record_result.exit_code == 0
    return Request.last()

  @pytest.fixture(autouse=True, scope='class')
  def update_result(self, runner: CliRunner, recorded_request: Request):
    result = runner.invoke(request, ['update', recorded_request.key(), '--path', '/new-path'])
    assert result.exit_code == 0
    return result

  def test_it_updates_path(self, recorded_request: Request):
    refreshed = Request.find(recorded_request.id)
    assert refreshed.path == '/new-path'


class TestUpdateBody:

  @pytest.fixture(autouse=True, scope='class')
  def recorded_request(self, runner: CliRunner):
    record_result = runner.invoke(record, [DETERMINISTIC_GET_REQUEST_URL])
    assert record_result.exit_code == 0
    return Request.last()

  @pytest.fixture(autouse=True, scope='class')
  def update_result(self, runner: CliRunner, recorded_request: Request):
    result = runner.invoke(request, ['update', recorded_request.key(), '--body', '{"x":1}'])
    assert result.exit_code == 0
    return result

  def test_it_updates_body(self, recorded_request: Request):
    refreshed = Request.find(recorded_request.id)
    python_request = RawHttpRequestAdapter(refreshed.raw).to_request()
    assert python_request.data == b'{"x":1}'


class TestUpdateHeaders:

  @pytest.fixture(autouse=True, scope='class')
  def recorded_request(self, runner: CliRunner):
    record_result = runner.invoke(record, [DETERMINISTIC_GET_REQUEST_URL])
    assert record_result.exit_code == 0
    return Request.last()

  @pytest.fixture(scope='class')
  def original_headers(self, recorded_request: Request):
    return dict(RawHttpRequestAdapter(recorded_request.raw).headers)

  @pytest.fixture(autouse=True, scope='class')
  def set_header_result(self, runner: CliRunner, recorded_request: Request):
    result = runner.invoke(
      request,
      ['update', recorded_request.key(), '--header', 'X-Test:1'],
    )
    assert result.exit_code == 0
    return result

  def test_it_sets_header(self, recorded_request: Request):
    refreshed = Request.find(recorded_request.id)
    headers = RawHttpRequestAdapter(refreshed.raw).headers
    assert headers.get('X-Test') == '1'

  def test_it_preserves_other_headers(self, recorded_request: Request, original_headers: dict):
    refreshed = Request.find(recorded_request.id)
    headers = RawHttpRequestAdapter(refreshed.raw).headers

    for key, value in original_headers.items():
      assert headers.get(key) == value

  class TestWhenDeletingHeader:

    @pytest.fixture(autouse=True, scope='class')
    def delete_header_result(self, runner: CliRunner, recorded_request: Request):
      result = runner.invoke(
        request,
        ['update', recorded_request.key(), '--header', 'X-Test:'],
      )
      assert result.exit_code == 0
      return result

    def test_it_deletes_header(self, recorded_request: Request):
      refreshed = Request.find(recorded_request.id)
      headers = RawHttpRequestAdapter(refreshed.raw).headers
      assert 'X-Test' not in headers

  class TestWhenValueContainsColons:

    @pytest.fixture(autouse=True, scope='class')
    def set_header_result(self, runner: CliRunner, recorded_request: Request):
      result = runner.invoke(
        request,
        ['update', recorded_request.key(), '--header', 'X-Custom: a:b:c'],
      )
      assert result.exit_code == 0
      return result

    def test_it_preserves_colons_in_value(self, recorded_request: Request):
      refreshed = Request.find(recorded_request.id)
      headers = RawHttpRequestAdapter(refreshed.raw).headers
      assert headers.get('X-Custom') == 'a:b:c'

  class TestWhenHeaderFormatIsInvalid:

    def test_it_rejects_header_without_colon(self, runner: CliRunner, recorded_request: Request):
      result = runner.invoke(
        request,
        ['update', recorded_request.key(), '--header', 'NoColon'],
      )
      assert result.exit_code == 1
      assert 'Invalid header format' in result.output

    def test_it_rejects_header_without_name(self, runner: CliRunner, recorded_request: Request):
      result = runner.invoke(
        request,
        ['update', recorded_request.key(), '--header', ':value'],
      )
      assert result.exit_code == 1
      assert 'Header name is required' in result.output


class TestUpdateScenario:

  @pytest.fixture(autouse=True, scope='class')
  def scenario(self):
    record = Scenario.create(name='update scenario test')
    yield record
    record.delete()

  @pytest.fixture(autouse=True, scope='class')
  def recorded_request(self, runner: CliRunner):
    record_result = runner.invoke(record, [DETERMINISTIC_GET_REQUEST_URL])
    assert record_result.exit_code == 0
    return Request.last()

  class TestWhenAssigningTrashedRequest:

    @pytest.fixture(autouse=True, scope='class')
    def trashed_request(self, runner: CliRunner, recorded_request: Request):
      delete_result = runner.invoke(request, ['delete', recorded_request.key()])
      assert delete_result.exit_code == 0
      return Request.find(recorded_request.id)

    @pytest.fixture(autouse=True, scope='class')
    def assign_result(self, runner: CliRunner, trashed_request: Request, scenario: Scenario):
      result = runner.invoke(
        request,
        ['update', trashed_request.key(), '--scenario-key', scenario.key()],
      )
      assert result.exit_code == 0
      return result

    def test_it_assigns_scenario_id(self, trashed_request: Request, scenario: Scenario):
      refreshed = Request.find(trashed_request.id)
      assert refreshed.scenario_id == scenario.id

    def test_it_restores_from_trash(self, trashed_request: Request):
      refreshed = Request.find(trashed_request.id)
      assert refreshed.is_deleted == False

  class TestWhenClearingScenario:

    @pytest.fixture(autouse=True, scope='class')
    def request_in_scenario(self, runner: CliRunner, recorded_request: Request, scenario: Scenario):
      assign_result = runner.invoke(
        request,
        ['update', recorded_request.key(), '--scenario-key', scenario.key()],
      )
      assert assign_result.exit_code == 0
      return Request.find(recorded_request.id)

    @pytest.fixture(autouse=True, scope='class')
    def clear_result(self, runner: CliRunner, request_in_scenario: Request):
      result = runner.invoke(
        request,
        ['update', request_in_scenario.key(), '--scenario-key'],
      )
      assert result.exit_code == 0
      return result

    def test_it_clears_scenario_id(self, request_in_scenario: Request):
      refreshed = Request.find(request_in_scenario.id)
      assert refreshed.scenario_id is None
