import json
import pdb
import pytest
import requests

from click.testing import CliRunner

from stoobly_agent.test.test_helper import reset

from stoobly_agent.app.settings import Settings
from stoobly_agent.lib.orm.request import Request
from stoobly_agent.lib.orm.response import Response

from stoobly_agent.app.models.factories.resource.local_db.helpers.request_builder import RequestBuilder
from stoobly_agent.app.models.factories.resource.local_db.request_adapter import LocalDBRequestAdapter
from stoobly_agent.app.models.factories.resource.local_db.request_adapter import LocalDBResponseAdapter

@pytest.fixture(scope='module')
def runner():
    return CliRunner()

class TestOrmPythonResponseAdapter():
  @pytest.fixture(scope='class')
  def settings(self):
    return reset()

  @pytest.fixture(scope='class')
  def response_body(self):
    return {
      'first_name': 'John',
      'last_name': 'Smith',
    }

  @pytest.fixture(scope='class')
  def response_headers(self):
    return {
      'Content-Type': 'application/json'
    }

  @pytest.fixture(scope='class')
  def local_db_request_adapter(self):
    adapter = LocalDBRequestAdapter(request_orm=Request, response_orm=Response)
    return adapter

  @pytest.fixture(scope='class')
  def local_db_response_adapter(self):
    adapter = LocalDBResponseAdapter(request_orm=Request)
    return adapter

  @pytest.fixture(scope='function')
  def created_response(
    self, settings: Settings, 
    response_headers: dict, response_body: dict
  ):
    status = RequestBuilder(
      method='POST',
      request_body='',
      response_body=response_body,
      response_headers=response_headers,
      status_code=200,
      url='https://petstore.swagger.io/v2/pets',
    ).with_settings(settings).build()[1]
    assert status == 200

    return Response.last()

  def test_it_updates_response(self, created_response: Response, local_db_response_adapter: LocalDBResponseAdapter):
    new_body = '123'
    local_db_response_adapter.update(created_response.id, text=new_body)

    updated_response, status = local_db_response_adapter.show(created_response.id)

    assert status == 200
    assert updated_response[0]['text'] == new_body
    