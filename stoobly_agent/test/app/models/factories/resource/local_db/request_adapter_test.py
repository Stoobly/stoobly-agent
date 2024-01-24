import pdb
import pytest

from urllib.parse import urlparse

from stoobly_agent.app.models.factories.resource.local_db.helpers.request_builder import RequestBuilder
from stoobly_agent.app.models.factories.resource.local_db.request_adapter import (
  LocalDBRequestAdapter,
)
from stoobly_agent.app.models.types.request import RequestIndexSimilarParams
from stoobly_agent.lib.orm.request import Request
from stoobly_agent.lib.orm.response import Response
from stoobly_agent.app.settings import Settings
from stoobly_agent.lib.orm.scenario import Scenario
from stoobly_agent.test.test_helper import reset

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
