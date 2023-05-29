import pytest

from stoobly_agent.app.models.factories.resource.local_db.request_adapter import (
  LocalDBRequestAdapter,
)
from stoobly_agent.app.models.types.request import RequestFindParams
from stoobly_agent.lib.orm.request import Request
from stoobly_agent.test.test_helper import reset

class TestLocalDBRequestAdapter():
  @pytest.fixture(autouse=True)
  def settings(self):
    return reset()

  @pytest.fixture(scope='function')
  def local_db_request_adapter(self):
    self.__request_orm = Request
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

