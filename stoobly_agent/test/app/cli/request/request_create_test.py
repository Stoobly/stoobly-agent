import pytest

from click.testing import CliRunner

from stoobly_agent.app.cli.request_cli import request
from stoobly_agent.app.cli.scenario_cli import scenario
from stoobly_agent.app.models.adapters.raw_http_request_adapter import RawHttpRequestAdapter
from stoobly_agent.app.models.adapters.raw_http_response_adapter import RawHttpResponseAdapter
from stoobly_agent.lib.orm.request import Request
from stoobly_agent.lib.orm.scenario import Scenario
from stoobly_agent.lib.utils.decode import decode
from stoobly_agent.test.test_helper import reset


@pytest.fixture(scope='module')
def runner():
  return CliRunner()


@pytest.fixture(autouse=True, scope='module')
def settings():
  return reset()


class TestCreate:

  def test_it_creates_a_request(self, runner: CliRunner):
    result = runner.invoke(request, ['create', 'https://example.com/api/pets'])
    assert result.exit_code == 0

    created = Request.last()
    assert created is not None
    assert created.method == 'GET'
    assert created.host == 'example.com'
    assert created.path == '/api/pets'
    assert created.status == 200


class TestCreateMethod:

  @pytest.fixture(autouse=True, scope='class')
  def create_result(self, runner: CliRunner):
    result = runner.invoke(
      request,
      ['create', 'https://example.com/api/pets', '--method', 'POST'],
    )
    assert result.exit_code == 0
    return result

  def test_it_sets_method(self):
    created = Request.last()
    assert created.method == 'POST'


class TestCreateBodyAndHeaders:

  @pytest.fixture(autouse=True, scope='class')
  def create_result(self, runner: CliRunner):
    result = runner.invoke(
      request,
      [
        'create',
        'https://example.com/api/pets',
        '--method', 'POST',
        '--body', '{"name":"fido"}',
        '--header', 'Content-Type:application/json',
        '--header', 'X-Test:1',
      ],
    )
    assert result.exit_code == 0
    return result

  def test_it_sets_body(self):
    created = Request.last()
    python_request = RawHttpRequestAdapter(created.raw).to_request()
    assert python_request.data == b'{"name":"fido"}'

  def test_it_sets_headers(self):
    created = Request.last()
    headers = RawHttpRequestAdapter(created.raw).headers
    assert headers.get('Content-Type') == 'application/json'
    assert headers.get('X-Test') == '1'


class TestCreateResponse:

  @pytest.fixture(autouse=True, scope='class')
  def create_result(self, runner: CliRunner):
    result = runner.invoke(
      request,
      [
        'create',
        'https://example.com/api/pets',
        '--status', '201',
        '--response-body', '{"id":1}',
        '--response-header', 'Content-Type:application/json',
        '--latency', '25',
      ],
    )
    assert result.exit_code == 0
    return result

  def test_it_sets_status(self):
    created = Request.last()
    assert created.status == 201

  def test_it_sets_response_body(self):
    created = Request.last()
    python_response = RawHttpResponseAdapter(created.response.raw).to_response()
    assert decode(python_response.content) == '{"id":1}'

  def test_it_sets_response_headers(self):
    created = Request.last()
    headers = RawHttpResponseAdapter(created.response.raw).headers
    assert headers.get('Content-Type') == 'application/json'

  def test_it_sets_latency(self):
    created = Request.last()
    assert created.latency == 25


class TestCreateScenarioKey:

  @pytest.fixture(autouse=True, scope='class')
  def created_scenario(self, runner: CliRunner):
    result = runner.invoke(scenario, ['create', 'request-create-scenario'])
    assert result.exit_code == 0
    return Scenario.last()

  @pytest.fixture(autouse=True, scope='class')
  def create_result(self, runner: CliRunner, created_scenario: Scenario):
    result = runner.invoke(
      request,
      [
        'create',
        'https://example.com/api/pets',
        '--scenario-key', created_scenario.key(),
      ],
    )
    assert result.exit_code == 0
    return result

  def test_it_assigns_scenario(self, created_scenario: Scenario):
    created = Request.last()
    assert created.scenario_id == created_scenario.id


class TestCreateInvalidHeader:

  def test_it_rejects_invalid_header_format(self, runner: CliRunner):
    result = runner.invoke(
      request,
      ['create', 'https://example.com/api/pets', '--header', 'Invalid'],
    )
    assert result.exit_code == 1
    assert 'Invalid header format' in result.output
