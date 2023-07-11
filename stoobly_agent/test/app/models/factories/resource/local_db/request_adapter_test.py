import pdb
import pytest

from typing import List
from urllib.parse import urlparse

from stoobly_agent.app.models.factories.resource.local_db.helpers.request_builder import RequestBuilder
from stoobly_agent.app.models.factories.resource.local_db.helpers.tiebreak_scenario_request import (
  access_request, generate_session_id, tiebreak_scenario_request
)
from stoobly_agent.app.models.factories.resource.local_db.request_adapter import (
  LocalDBRequestAdapter,
)
from stoobly_agent.app.models.types.request import RequestFindParams
from stoobly_agent.lib.orm.request import Request
from stoobly_agent.app.settings import Settings
from stoobly_agent.lib.orm.scenario import Scenario
from stoobly_agent.test.test_helper import reset

class TestLocalDBRequestAdapter():
  @pytest.fixture(autouse=True)
  def settings(self):
    return reset()

  @pytest.fixture(scope='function')
  def local_db_request_adapter(self):
    self.__request_orm = Request
    self.__scenario_orm = Scenario
    adapter = LocalDBRequestAdapter(request_orm=self.__request_orm)
    return adapter

  @pytest.fixture(scope='function')
  def create_get_pets(self):
    record = self.__request_orm.create(
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
  def create_get_pet(self):
    record = self.__request_orm.create(
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
  def create_scenario(self):
    record = self.__scenario_orm.create(
      name="Pets scenario",
    )
    yield record
    record.delete()

  @pytest.mark.openapi
  def test_find_similar_requests(self, local_db_request_adapter: LocalDBRequestAdapter, create_get_pets, create_get_pet):
    params: RequestFindParams = {
      'method': 'GET',
      'host' : "petstore.swagger.io",
      'port': "443",
      'pattern': '/v2/pets'
    }

    similar_requests = local_db_request_adapter.find_similar_requests(params)

    assert len(similar_requests) == 1
    for request in similar_requests:
      assert request.host == params['host']
      assert request.port == int(params['port'])
      assert request.method == params['method']
      assert request.path == params['pattern']

  @pytest.mark.openapi
  def test_find_similar_requests_given_scenario_with_no_requests(self, local_db_request_adapter: LocalDBRequestAdapter, create_get_pets, create_get_pet, create_scenario):
    params: RequestFindParams = {
      'method': 'GET',
      'host' : "petstore.swagger.io",
      'port': "443",
      'pattern': '/v2/pets',
      'scenario_id': create_scenario.id,
    }

    similar_requests = local_db_request_adapter.find_similar_requests(params)

    assert len(similar_requests) == 0

  @pytest.mark.openapi
  def test_find_similar_requests_given_scenario_with_requests(self, local_db_request_adapter: LocalDBRequestAdapter, create_get_pets, create_get_pet, create_scenario):

    self.__request_orm.where('id', create_get_pets.id).update(scenario_id=create_scenario.id)

    params: RequestFindParams = {
      'method': 'GET',
      'host' : "petstore.swagger.io",
      'port': "443",
      'pattern': '/v2/pets',
      'scenario_id': create_scenario.id,
    }

    similar_requests = local_db_request_adapter.find_similar_requests(params)

    assert len(similar_requests) == 1
    assert similar_requests[0].id == create_get_pets.id

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