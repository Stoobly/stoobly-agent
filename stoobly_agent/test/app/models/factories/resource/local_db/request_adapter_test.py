import pdb
import pytest
import requests

from urllib.parse import urlparse

from stoobly_agent.app.models.adapters.python import PythonRequestAdapterFactory
from stoobly_agent.app.models.factories.resource.local_db.helpers.request_builder import RequestBuilder
from stoobly_agent.app.models.factories.resource.local_db.request_adapter import (
  LocalDBRequestAdapter,
)
from stoobly_agent.app.models.types.request import RequestIndexSimilarParams
from stoobly_agent.app.proxy.constants import custom_response_codes
from stoobly_agent.app.proxy.mock.hashed_request_decorator import HashedRequestDecorator
from stoobly_agent.lib.orm.request import Request
from stoobly_agent.lib.orm.response import Response
from stoobly_agent.app.settings import Settings
from stoobly_agent.config.constants import custom_headers, query_params as request_query_params
from stoobly_agent.lib.orm.scenario import Scenario
from stoobly_agent.test.test_helper import reset

class TestIndex():
  @pytest.fixture(autouse=True, scope='class')
  def settings(self):
    return reset()

  @pytest.fixture(scope='class')
  def adapter(self):
    return LocalDBRequestAdapter(request_orm=Request, response_orm=Response)

  @pytest.fixture(autouse=True, scope='class')
  def active_request(self, settings: Settings):
    status = RequestBuilder(
      method='GET',
      request_body='',
      request_headers={},
      response_body='',
      status_code=200,
      url='https://petstore.swagger.io/v2/pets',
    ).with_settings(settings).build()[1]
    assert status == 200
    record = Request.last()
    yield record
    record.delete()

  @pytest.fixture(autouse=True, scope='class')
  def trashed_request(self, settings: Settings, active_request: Request):
    status = RequestBuilder(
      method='GET',
      request_body='',
      request_headers={},
      response_body='',
      status_code=200,
      url='https://petstore.swagger.io/v2/trashed',
    ).with_settings(settings).build()[1]
    assert status == 200
    record = Request.last()
    record.update({'is_deleted': True})
    yield record
    record.delete()

  def test_it_excludes_trashed_by_default(self, adapter: LocalDBRequestAdapter, active_request: Request, trashed_request: Request):
    body, status = adapter.index()
    assert status == 200
    assert body['total'] == 1

  class TestWhenFilterIsDeleted():
    def test_it_returns_only_trashed(self, adapter: LocalDBRequestAdapter, active_request: Request, trashed_request: Request):
      body, status = adapter.index(filter='is_deleted')
      assert status == 200
      assert body['total'] == 1


class TestLocalDBRequestAdapter():
  @pytest.fixture(autouse=True, scope='class')
  def settings(self):
    return reset()

  @pytest.fixture(scope='class')
  def local_db_request_adapter(self):
    adapter = LocalDBRequestAdapter(request_orm=Request, response_orm=Response)
    return adapter

  class SimilarRequests():
    @pytest.fixture(scope='function')
    def get_v2_pets(self):
      record = Request.create(
        method='GET',
        scheme='https',
        host="petstore.swagger.io",
        port="443",
        path='/v2/pets',
        headers_hash='c079b917a5091fbcdea198bc96c87796',
        body_text_hash='',
        query_params_hash='90f45a51e497a899f995f5c913b805ba',
        body_params_hash='',
        control='1 oxsmp817uge 1684883577229000000',
        raw='GET https://petstore.swagger.io/v2/pets?limit=1 HTTP/1.1 Content-Length: 0',
        query='limit=1'
      )
      yield record
      record.delete()

    @pytest.fixture(scope='function')
    def get_v2_pet_1(self):
      record = Request.create(
        method='GET',
        scheme='https',
        host="petstore.swagger.io",
        port="443",
        path='/v2/pet/1',
        headers_hash='c079b917a5091fbcdea198bc96c87796',
        body_text_hash='',
        query_params_hash='',
        body_params_hash='',
        control='1 l9jiwridgk 1684883778859000000',
        raw='GET https://petstore.swagger.io/v2/pets/1 HTTP/1.1 Content-Length: 0',
      )
      yield record
      record.delete()

    @pytest.fixture(scope='function')
    def create_put_v3_pet(self):
      record = Request.create(
        method='PUT',
        scheme='http',
        host="swagger.io",
        port="80",
        path='/v3/pet',
        headers_hash='c079b917a5091fbcdea198bc96c87796',
        body_text_hash='',
        query_params_hash='',
        body_params_hash='',
        control='1 gocrqlad4ru 1690266880243000000',
        raw='PUT http://swagger.io/v3/pet HTTP/1.1 Content-Length: 0',
      )
      yield record
      record.delete()

    @pytest.fixture(scope='function')
    def created_scenario(self):
      record = Scenario.create(name="Pets scenario")
      yield record
      record.delete()

    @pytest.mark.openapi
    def test_finds_get_v2_pets(self, local_db_request_adapter: LocalDBRequestAdapter, get_v2_pets: Request, get_v2_pet_1: Request):
      assert get_v2_pets
      assert get_v2_pet_1

      params: RequestIndexSimilarParams = {
        'method': 'GET',
        'host' : "petstore.swagger.io",
        'port': "443",
        'pattern': '/v2/pets'
      }

      similar_requests = local_db_request_adapter.index_similar(params)

      assert len(similar_requests) == 1

      request = similar_requests[0]
      assert request.host == params['host']
      assert request.port == int(params['port'])
      assert request.method == params['method']
      assert request.path == params['pattern']

    @pytest.mark.openapi
    def test_finds_put_v3_pet(self, local_db_request_adapter: LocalDBRequestAdapter, create_put_v3_pet: Request):
      params: RequestIndexSimilarParams = {
        'host': '%',
        'port': '%',
        'method': 'PUT',
        'pattern': '/v3/pet',
        'scenario_id': 0
      }

      similar_requests = local_db_request_adapter.index_similar(params)

      assert len(similar_requests) == 1

      request = similar_requests[0]
      assert request.id == create_put_v3_pet.id
      assert request.method == params['method']
      assert request.path == params['pattern']

    class Scenario():
      @pytest.mark.openapi
      def test_finds_no_requests(
        self, local_db_request_adapter: LocalDBRequestAdapter, get_v2_pets: Request, get_v2_pet_1: Request, created_scenario: Scenario
      ):
        assert get_v2_pets
        assert get_v2_pet_1

        params: RequestIndexSimilarParams = {
          'method': 'GET',
          'host' : "petstore.swagger.io",
          'port': "443",
          'pattern': '/v2/pets',
          'scenario_id': created_scenario.id,
        }

        similar_requests = local_db_request_adapter.index_similar(params)

        assert len(similar_requests) == 0

      @pytest.mark.openapi
      def test_finds_requests(
        self, local_db_request_adapter: LocalDBRequestAdapter, get_v2_pets: Request, get_v2_pet_1: Request, created_scenario: Scenario
      ):
        assert get_v2_pets
        assert get_v2_pet_1

        Request.where('id', get_v2_pets.id).update(scenario_id=created_scenario.id)

        params: RequestIndexSimilarParams = {
          'method': 'GET',
          'host' : "petstore.swagger.io",
          'port': "443",
          'pattern': '/v2/pets',
          'scenario_id': created_scenario.id,
        }

        similar_requests = local_db_request_adapter.index_similar(params)

        assert len(similar_requests) == 1
        assert similar_requests[0].id == get_v2_pets.id

  class TestWhenResponse():
    class TestTiebreakScenarioRequest():
      @pytest.fixture(autouse=True, scope='class')
      def settings(self):
        return reset()

      @pytest.fixture(scope='class')
      def request_method(self):
        return 'POST'

      @pytest.fixture(scope='class')
      def request_url(self):
        return 'https://petstore.swagger.io/v2/pets'

      @pytest.fixture(scope='class')
      def created_scenario(self):
        return Scenario.create(name='test')

      @pytest.fixture(autouse=True, scope='class')
      def created_request_one(
        self, settings: Settings, 
        request_method: str, request_url: str, created_scenario: Scenario,
      ):
        status = RequestBuilder(
          method=request_method,
          request_body='',
          request_headers={},
          response_body='',
          status_code=201,
          url=request_url,
        ).with_settings(settings).build()[1]
        assert status == 200

        request = Request.last()
        request.update(scenario_id=created_scenario.id)

        return request

      @pytest.fixture(autouse=True, scope='class')
      def created_request_two(
        self, settings: Settings, 
        request_method: str, request_url: str, created_scenario: Scenario
      ):
        status = RequestBuilder(
          method=request_method,
          request_body='',
          request_headers={},
          response_body='2',
          status_code=202,
          url=request_url,
        ).with_settings(settings).build()[1]
        assert status == 200

        request = Request.last()
        request.update(scenario_id=created_scenario.id)
        return request

      @pytest.fixture(scope='class')
      def requests(self, created_request_one: Request, created_request_two: Request):
        return [created_request_one, created_request_two]

      def test_it_returns_request_one(self, request_url: str, created_scenario: Scenario, local_db_request_adapter: LocalDBRequestAdapter):
        uri = urlparse(request_url)
        response = local_db_request_adapter.response(
          host=uri.hostname, path=uri.path, scenario_id=created_scenario.id
        )
        assert response.status_code == 201

      def test_it_returns_request_two(self, request_url: str, created_scenario: Scenario, local_db_request_adapter: LocalDBRequestAdapter):
        uri = urlparse(request_url)
        response = local_db_request_adapter.response(
          host=uri.hostname, path=uri.path, scenario_id=created_scenario.id
        )
        assert response.status_code == 202

      def test_it_returns_request_one_again(self, request_url: str, created_scenario: Scenario, local_db_request_adapter: LocalDBRequestAdapter):
        uri = urlparse(request_url)
        response = local_db_request_adapter.response(
          host=uri.hostname, path=uri.path, scenario_id=created_scenario.id
        )
        assert response.status_code == 201

    class TestMostRecentWithoutScenario():
      @pytest.fixture(autouse=True, scope='class')
      def settings(self):
        return reset()

      @pytest.fixture(scope='class')
      def request_url(self):
        return 'https://example.com/v1/unordered'

      @pytest.fixture(autouse=True, scope='class')
      def created_request_one(self, settings: Settings, request_url: str):
        status = RequestBuilder(
          method='GET',
          request_body='',
          request_headers={},
          response_body='older',
          status_code=200,
          url=request_url,
        ).with_settings(settings).build()[1]
        assert status == 200
        return Request.last()

      @pytest.fixture(autouse=True, scope='class')
      def created_request_two(self, settings: Settings, request_url: str, created_request_one: Request):
        status = RequestBuilder(
          method='GET',
          request_body='',
          request_headers={},
          response_body='newer',
          status_code=201,
          url=request_url,
        ).with_settings(settings).build()[1]
        assert status == 200
        request = Request.last()
        assert request.id > created_request_one.id
        return request

      def test_it_returns_highest_id(
        self,
        request_url: str,
        created_request_one: Request,
        created_request_two: Request,
        local_db_request_adapter: LocalDBRequestAdapter,
      ):
        uri = urlparse(request_url)
        response = local_db_request_adapter.response(
          host=uri.hostname,
          path=uri.path,
          method='GET',
          port=443,
        )
        assert response.status_code == 201
        assert response.headers.get(custom_headers.MOCK_REQUEST_ID) == str(created_request_two.id)

    class TestHeuristicTiebreak():
      @pytest.fixture(autouse=True, scope='class')
      def settings(self):
        return reset()

      @pytest.fixture(scope='class')
      def created_scenario(self):
        return Scenario.create(name='heuristic-tiebreak')

      @pytest.fixture(autouse=True, scope='class')
      def created_request_admin(self, settings: Settings, created_scenario: Scenario):
        status = RequestBuilder(
          method='GET',
          request_body='',
          request_headers={},
          response_body='admin',
          status_code=200,
          url='https://example.com/v1/search?role=admin',
        ).with_settings(settings).build()[1]
        assert status == 200
        request = Request.last()
        request.update(scenario_id=created_scenario.id, sequence_id=1)
        return request

      @pytest.fixture(autouse=True, scope='class')
      def created_request_user(self, settings: Settings, created_scenario: Scenario):
        status = RequestBuilder(
          method='GET',
          request_body='',
          request_headers={},
          response_body='user',
          status_code=201,
          url='https://example.com/v1/search?role=user',
        ).with_settings(settings).build()[1]
        assert status == 200
        request = Request.last()
        request.update(scenario_id=created_scenario.id, sequence_id=3)
        return request

      def test_it_picks_by_query_params(
        self,
        created_scenario: Scenario,
        created_request_user: Request,
        local_db_request_adapter: LocalDBRequestAdapter,
      ):
        response = local_db_request_adapter.response(
          host='example.com',
          path='/v1/search',
          method='GET',
          port=443,
          scenario_id=created_scenario.id,
          **{request_query_params.QUERY_PARAMS: {'role': 'user'}},
        )
        assert response.status_code == 201
        assert response.headers.get(custom_headers.MOCK_REQUEST_ID) == str(created_request_user.id)

      def test_it_picks_by_sequence_id(
        self,
        created_scenario: Scenario,
        created_request_user: Request,
        local_db_request_adapter: LocalDBRequestAdapter,
      ):
        response = local_db_request_adapter.response(
          host='example.com',
          path='/v1/search',
          method='GET',
          port=443,
          scenario_id=created_scenario.id,
          **{request_query_params.SEQUENCE_ID: 3},
        )
        assert response.status_code == 201
        assert response.headers.get(custom_headers.MOCK_REQUEST_ID) == str(created_request_user.id)

    class TestNotFound():
      @pytest.fixture(autouse=True, scope='class')
      def settings(self):
        return reset()

      def test_it_returns_499_when_no_matching_row(self, local_db_request_adapter: LocalDBRequestAdapter):
        response = local_db_request_adapter.response(
          host='missing.example.com',
          path='/none',
          method='GET',
          port=443,
        )
        assert response.status_code == custom_response_codes.NOT_FOUND

      def test_it_returns_499_on_retry_even_with_endpoint_ignores(
        self, local_db_request_adapter: LocalDBRequestAdapter
      ):
        ignored_components = [{'type': 3, 'name': 'b'}]
        response = local_db_request_adapter.response(
          host='missing.example.com',
          path='/none',
          method='GET',
          port=443,
          query_params_hash='abc',
          retry=True,
          endpoint_promise=lambda: {'ignored_components': ignored_components},
        )
        assert response.status_code == custom_response_codes.NOT_FOUND

    class TestMockRequestEndpointIdHeader():
      @pytest.fixture(scope='function')
      def created_request(self, settings: Settings):
        status = RequestBuilder(
          method='GET',
          request_body='',
          request_headers={},
          response_body='ok',
          status_code=200,
          url='https://example.com/v1/items',
        ).with_settings(settings).build()[1]
        assert status == 200

        request = Request.last()
        yield request
        request.delete()

      def test_it_omits_endpoint_id_without_endpoint_promise(
        self, local_db_request_adapter: LocalDBRequestAdapter, created_request: Request
      ):
        response = local_db_request_adapter.response(request_id=created_request.id)

        assert response.status_code == 200
        assert custom_headers.MOCK_REQUEST_ENDPOINT_ID not in response.headers
        assert response.headers.get(custom_headers.MOCK_REQUEST_ID) == str(created_request.id)

      def test_it_includes_endpoint_id_when_endpoint_promise_provides_id(
        self, local_db_request_adapter: LocalDBRequestAdapter, created_request: Request
      ):
        endpoint_id = 'openapi-endpoint-abc'
        response = local_db_request_adapter.response(
          request_id=created_request.id,
          endpoint_promise=lambda: {'id': endpoint_id},
        )

        assert response.status_code == 200
        assert response.headers.get(custom_headers.MOCK_REQUEST_ENDPOINT_ID) == endpoint_id
        assert response.headers.get(custom_headers.MOCK_REQUEST_ID) == str(created_request.id)

    class TestComputeMode():
      @pytest.fixture(scope='function')
      def created_request(self, settings: Settings):
        status = RequestBuilder(
          method='GET',
          request_body='',
          request_headers={'x-token': 'abc'},
          response_body='ok',
          status_code=200,
          url='https://example.com/v1/search?a=1&b=2',
        ).with_settings(settings).build()[1]
        assert status == 200

        request = Request.last()
        yield request
        request.delete()

      def test_it_recomputes_hashes_when_compute_is_enabled(
        self, local_db_request_adapter: LocalDBRequestAdapter, created_request: Request
      ):
        ignored_components = [
          {'type': 3, 'name': 'b'},
        ]

        python_request = requests.Request(
          method='GET',
          url='https://example.com/v1/search?a=1&b=3',
          headers={'x-token': 'abc'},
        )
        mitmproxy_request = PythonRequestAdapterFactory(python_request).mitmproxy_request()
        hashed_request = HashedRequestDecorator(mitmproxy_request).with_ignored_components(ignored_components)

        response = local_db_request_adapter.response(
          host='example.com',
          method='GET',
          path='/v1/search',
          port=443,
          query_params_hash=hashed_request.query_params_hash(),
          compute=1,
          endpoint_promise=lambda: { 'ignored_components': ignored_components }
        )

        assert response.status_code == 200

      def test_it_does_not_recompute_hashes_when_compute_is_disabled(
        self, local_db_request_adapter: LocalDBRequestAdapter, created_request: Request
      ):
        ignored_components = [
          {'type': 3, 'name': 'b'},
        ]

        python_request = requests.Request(
          method='GET',
          url='https://example.com/v1/search?a=1&b=2',
          headers={'x-token': 'abc'},
        )
        mitmproxy_request = PythonRequestAdapterFactory(python_request).mitmproxy_request()
        hashed_request = HashedRequestDecorator(mitmproxy_request).with_ignored_components(ignored_components)

        response = local_db_request_adapter.response(
          host='example.com',
          method='GET',
          path='/v1/search',
          port=443,
          query_params_hash=hashed_request.query_params_hash(),
          endpoint_promise=lambda: { 'ignored_components': ignored_components }
        )

        assert response.status_code == 498
