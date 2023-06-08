import json
import pdb
import pytest

from click.testing import CliRunner
from mitmproxy.http import Response as MitmproxyResponse

from stoobly_agent.test.test_helper import reset

from stoobly_agent.app.models.adapters.orm.response.mitmproxy_adapter import MitmproxyResponseAdapter
from stoobly_agent.app.settings import Settings
from stoobly_agent.lib.orm.response import Response

from stoobly_agent.app.models.factories.resource.local_db.helpers.request_builder import RequestBuilder

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
  def created_response(
    self, settings: Settings, 
    response_headers: dict, response_body: dict
  ):
    status = RequestBuilder(
      method='POST',
      request_body='',
      response_headers=response_headers,
      response_body=response_body,
      status_code=200,
      url='https://petstore.swagger.io/v2/pets',
    ).with_settings(settings).build()[1]
    assert status == 200

    return Response.last()

  @pytest.fixture()
  def mitmproxy_response(self, created_response: Response):
    return MitmproxyResponseAdapter(created_response).adapt()

  def test_it_sets_headers(self, mitmproxy_response: MitmproxyResponse, response_headers: dict):
    data = mitmproxy_response.content
    headers = dict(mitmproxy_response.headers)
    assert headers == {
      **response_headers,
      'Content-Length': str(len(data))
    }

  def test_it_returns_content_as_bytes(self, mitmproxy_response: MitmproxyResponse):
    assert isinstance(mitmproxy_response.content, bytes)

  def test_it_returns_raw_content_as_bytes(self, mitmproxy_response: MitmproxyResponse):
    assert isinstance(mitmproxy_response.raw_content, bytes)

  def test_it_sets_content(self, mitmproxy_response: MitmproxyResponse, response_body: dict):
    content = mitmproxy_response.content
    assert json.dumps(response_body) == content.decode()