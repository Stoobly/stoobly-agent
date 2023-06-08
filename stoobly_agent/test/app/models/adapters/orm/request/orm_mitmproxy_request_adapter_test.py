import json
import pdb
import pytest
import requests

from click.testing import CliRunner
from mitmproxy.http import Request as MitmproxyRequest

from stoobly_agent.test.test_helper import reset

from stoobly_agent.app.models.adapters.orm.request.mitmproxy_adapter import MitmproxyRequestAdapter
from stoobly_agent.app.settings import Settings
from stoobly_agent.lib.orm.request import Request

from stoobly_agent.app.models.factories.resource.local_db.helpers.request_builder import RequestBuilder

@pytest.fixture(scope='module')
def runner():
    return CliRunner()

class TestOrmPythonRequestAdapter():
  @pytest.fixture(scope='class')
  def settings(self):
    return reset()

  @pytest.fixture(scope='class')
  def request_method(self):
    return 'POST'

  @pytest.fixture(scope='class')
  def request_url(self):
    return 'https://petstore.swagger.io/v2/pets'

  @pytest.fixture(scope='class')
  def request_body(self):
    return {
      'first_name': 'John',
      'last_name': 'Smith',
    }

  @pytest.fixture(scope='class')
  def request_headers(self):
    return {
      'Content-Type': 'application/json'
    }

  @pytest.fixture(scope='class')
  def created_request(
    self, settings: Settings, 
    request_method: str, request_url: str, request_headers: dict, request_body: dict
  ):
    status = RequestBuilder(
      method=request_method,
      request_body=request_body,
      request_headers=request_headers,
      response_body='',
      status_code=200,
      url=request_url,
    ).with_settings(settings).build()[1]
    assert status == 200

    return Request.last()

  @pytest.fixture()
  def mitmproxy_request(self, created_request: Request):
    return MitmproxyRequestAdapter(created_request).adapt()

  def test_it_sets_method(self, mitmproxy_request: MitmproxyRequest, request_method: str):
    assert mitmproxy_request.method == request_method

  def test_it_sets_url(self, mitmproxy_request: MitmproxyRequest, request_url: str):
    assert mitmproxy_request.url == request_url

  def test_it_sets_headers(self, mitmproxy_request: MitmproxyRequest, request_headers: dict):
    data = mitmproxy_request.content
    headers = dict(mitmproxy_request.headers)
    assert headers == {
      **request_headers,
      'Content-Length': str(len(data))
    }

  def test_it_returns_content_as_bytes(self, mitmproxy_request: MitmproxyRequest):
    assert isinstance(mitmproxy_request.content, bytes)

  def test_it_returns_raw_content_as_bytes(self, mitmproxy_request: MitmproxyRequest):
    assert isinstance(mitmproxy_request.raw_content, bytes)

  def test_it_sets_content(self, mitmproxy_request: MitmproxyRequest, request_body: dict):
    content = mitmproxy_request.content
    assert json.dumps(request_body) == content.decode()