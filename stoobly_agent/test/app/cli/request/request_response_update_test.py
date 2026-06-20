import pytest

from click.testing import CliRunner

from stoobly_agent.app.cli.request_cli import request
from stoobly_agent.app.models.adapters.raw_http_response_adapter import RawHttpResponseAdapter
from stoobly_agent.app.proxy.record.response_string_control import ResponseStringControl
from stoobly_agent.cli import record
from stoobly_agent.lib.orm.request import Request
from stoobly_agent.lib.utils.decode import decode
from stoobly_agent.test.test_helper import DETERMINISTIC_GET_REQUEST_URL, reset


@pytest.fixture(scope='module')
def runner():
  return CliRunner()


@pytest.fixture(autouse=True, scope='module')
def settings():
  return reset()


class TestResponseUpdate:

  @pytest.fixture(autouse=True, scope='class')
  def recorded_request(self, runner: CliRunner):
    record_result = runner.invoke(record, [DETERMINISTIC_GET_REQUEST_URL])
    assert record_result.exit_code == 0
    return Request.last()

  def test_it_requires_an_update_option(self, runner: CliRunner, recorded_request: Request):
    result = runner.invoke(request, ['response', 'update', recorded_request.key()])
    assert result.exit_code == 1
    assert 'At least one update option is required' in result.output

  def test_it_rejects_invalid_request_key(self, runner: CliRunner):
    result = runner.invoke(request, ['response', 'update', 'p0.rINVALID', '--body', 'test'])
    assert result.exit_code == 1


class TestResponseUpdateBody:

  @pytest.fixture(autouse=True, scope='class')
  def recorded_request(self, runner: CliRunner):
    record_result = runner.invoke(record, [DETERMINISTIC_GET_REQUEST_URL])
    assert record_result.exit_code == 0
    return Request.last()

  @pytest.fixture(autouse=True, scope='class')
  def update_result(self, runner: CliRunner, recorded_request: Request):
    result = runner.invoke(
      request,
      ['response', 'update', recorded_request.key(), '--body', '{"x":1}'],
    )
    assert result.exit_code == 0
    return result

  def test_it_updates_body(self, recorded_request: Request):
    refreshed = Request.find(recorded_request.id)
    python_response = RawHttpResponseAdapter(refreshed.response.raw).to_response()
    assert decode(python_response.content) == '{"x":1}'


class TestResponseUpdateHeaders:

  @pytest.fixture(autouse=True, scope='class')
  def recorded_request(self, runner: CliRunner):
    record_result = runner.invoke(record, [DETERMINISTIC_GET_REQUEST_URL])
    assert record_result.exit_code == 0
    return Request.last()

  @pytest.fixture(scope='class')
  def original_headers(self, recorded_request: Request):
    return dict(RawHttpResponseAdapter(recorded_request.response.raw).headers)

  @pytest.fixture(autouse=True, scope='class')
  def set_header_result(self, runner: CliRunner, recorded_request: Request):
    result = runner.invoke(
      request,
      ['response', 'update', recorded_request.key(), '--header', 'X-Test:1'],
    )
    assert result.exit_code == 0
    return result

  def test_it_sets_header(self, recorded_request: Request):
    refreshed = Request.find(recorded_request.id)
    headers = RawHttpResponseAdapter(refreshed.response.raw).headers
    assert headers.get('X-Test') == '1'

  def test_it_preserves_other_headers(self, recorded_request: Request, original_headers: dict):
    refreshed = Request.find(recorded_request.id)
    headers = RawHttpResponseAdapter(refreshed.response.raw).headers

    for key, value in original_headers.items():
      assert headers.get(key) == value

  class TestWhenDeletingHeader:

    @pytest.fixture(autouse=True, scope='class')
    def delete_header_result(self, runner: CliRunner, recorded_request: Request):
      result = runner.invoke(
        request,
        ['response', 'update', recorded_request.key(), '--header', 'X-Test:'],
      )
      assert result.exit_code == 0
      return result

    def test_it_deletes_header(self, recorded_request: Request):
      refreshed = Request.find(recorded_request.id)
      headers = RawHttpResponseAdapter(refreshed.response.raw).headers
      assert 'X-Test' not in headers

  class TestWhenValueContainsColons:

    @pytest.fixture(autouse=True, scope='class')
    def set_header_result(self, runner: CliRunner, recorded_request: Request):
      result = runner.invoke(
        request,
        ['response', 'update', recorded_request.key(), '--header', 'X-Custom: a:b:c'],
      )
      assert result.exit_code == 0
      return result

    def test_it_preserves_colons_in_value(self, recorded_request: Request):
      refreshed = Request.find(recorded_request.id)
      headers = RawHttpResponseAdapter(refreshed.response.raw).headers
      assert headers.get('X-Custom') == 'a:b:c'

  class TestWhenReplacingHeaderWithDifferentCase:

    @pytest.fixture(autouse=True, scope='class')
    def seed_mixed_case_header(self, runner: CliRunner, recorded_request: Request):
      result = runner.invoke(
        request,
        ['response', 'update', recorded_request.key(), '--header', 'X-Case-Test:original'],
      )
      assert result.exit_code == 0

    @pytest.fixture(autouse=True, scope='class')
    def replace_header_with_lowercase_name(self, runner: CliRunner, recorded_request: Request, seed_mixed_case_header):
      result = runner.invoke(
        request,
        ['response', 'update', recorded_request.key(), '--header', 'x-case-test:updated'],
      )
      assert result.exit_code == 0
      return result

    def test_it_replaces_existing_header_case_insensitively(self, recorded_request: Request):
      refreshed = Request.find(recorded_request.id)
      headers = RawHttpResponseAdapter(refreshed.response.raw).headers
      matching_keys = [k for k in headers if k.lower() == 'x-case-test']
      assert len(matching_keys) == 1
      assert headers[matching_keys[0]] == 'updated'

  class TestWhenHeaderFormatIsInvalid:

    def test_it_rejects_header_without_colon(self, runner: CliRunner, recorded_request: Request):
      result = runner.invoke(
        request,
        ['response', 'update', recorded_request.key(), '--header', 'NoColon'],
      )
      assert result.exit_code == 1
      assert 'Invalid header format' in result.output

    def test_it_rejects_header_without_name(self, runner: CliRunner, recorded_request: Request):
      result = runner.invoke(
        request,
        ['response', 'update', recorded_request.key(), '--header', ':value'],
      )
      assert result.exit_code == 1
      assert 'Header name is required' in result.output


class TestResponseUpdateStatus:

  @pytest.fixture(autouse=True, scope='class')
  def recorded_request(self, runner: CliRunner):
    record_result = runner.invoke(record, [DETERMINISTIC_GET_REQUEST_URL])
    assert record_result.exit_code == 0
    return Request.last()

  @pytest.fixture(autouse=True, scope='class')
  def update_result(self, runner: CliRunner, recorded_request: Request):
    result = runner.invoke(
      request,
      ['response', 'update', recorded_request.key(), '--status', '201'],
    )
    assert result.exit_code == 0
    return result

  def test_it_updates_status(self, recorded_request: Request):
    refreshed = Request.find(recorded_request.id)
    assert RawHttpResponseAdapter(refreshed.response.raw).status == 201


class TestResponseUpdateLatency:

  @pytest.fixture(autouse=True, scope='class')
  def recorded_request(self, runner: CliRunner):
    record_result = runner.invoke(record, [DETERMINISTIC_GET_REQUEST_URL])
    assert record_result.exit_code == 0
    return Request.last()

  @pytest.fixture(autouse=True, scope='class')
  def update_result(self, runner: CliRunner, recorded_request: Request):
    result = runner.invoke(
      request,
      ['response', 'update', recorded_request.key(), '--latency', '500'],
    )
    assert result.exit_code == 0
    return result

  def test_it_updates_latency(self, recorded_request: Request):
    refreshed = Request.find(recorded_request.id)
    control = ResponseStringControl(refreshed.response.control)
    assert control.latency == 500
