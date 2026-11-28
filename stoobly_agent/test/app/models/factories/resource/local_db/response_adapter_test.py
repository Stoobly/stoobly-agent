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
  @classmethod
  def settings(cls):
    return reset()

  @pytest.fixture(scope='class')
  @classmethod
  def response_body(cls):
    return {
      'first_name': 'John',
      'last_name': 'Smith',
    }

  @pytest.fixture(scope='class')
  @classmethod
  def response_headers(cls):
    return {
      'Content-Type': 'application/json'
    }

  @pytest.fixture(scope='class')
  @classmethod
  def local_db_request_adapter(cls):
    adapter = LocalDBRequestAdapter(request_orm=Request, response_orm=Response)
    return adapter

  @pytest.fixture(scope='class')
  @classmethod
  def local_db_response_adapter(cls):
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

  def test_it_rejects_adding_content_encoding(
    self, created_response: Response, local_db_response_adapter: LocalDBResponseAdapter
  ):
    from stoobly_agent.app.models.adapters.raw_http_response_adapter import RawHttpResponseAdapter

    headers = dict(RawHttpResponseAdapter(created_response.raw).headers)
    headers['Content-Encoding'] = 'gzip'

    res, status = local_db_response_adapter.update(created_response.id, headers=headers)

    assert status == 400
    assert res == 'Changing Content-Encoding is not allowed'

  def test_it_rejects_removing_content_encoding(
    self, settings: Settings, local_db_response_adapter: LocalDBResponseAdapter
  ):
    from mitmproxy.net import encoding
    from stoobly_agent.app.models.adapters.raw_http_response_adapter import RawHttpResponseAdapter

    plain = b'{"hello":"world"}'
    gzipped = encoding.encode(plain, 'gzip')
    status = RequestBuilder(
      method='GET',
      request_body='',
      response_body=gzipped,
      response_headers={
        'Content-Type': 'application/json',
        'Content-Encoding': 'gzip',
        'Content-Length': str(len(gzipped)),
      },
      status_code=200,
      url='https://example.com/encoded',
    ).with_settings(settings).build()[1]
    assert status == 200

    response = Response.last()
    headers = dict(RawHttpResponseAdapter(response.raw).headers)
    headers.pop('Content-Encoding', None)
    headers.pop('content-encoding', None)

    res, update_status = local_db_response_adapter.update(response.id, headers=headers)

    assert update_status == 400
    assert res == 'Changing Content-Encoding is not allowed'

    raw_after = RawHttpResponseAdapter(Response.find(response.id).raw)
    assert raw_after.headers.get('Content-Encoding') == 'gzip'
    assert raw_after.body[:2] == b'\x1f\x8b'

  def test_it_allows_other_header_updates_with_content_encoding(
    self, settings: Settings, local_db_response_adapter: LocalDBResponseAdapter
  ):
    from mitmproxy.net import encoding
    from stoobly_agent.app.models.adapters.raw_http_response_adapter import RawHttpResponseAdapter

    plain = b'{"hello":"world"}'
    gzipped = encoding.encode(plain, 'gzip')
    status = RequestBuilder(
      method='GET',
      request_body='',
      response_body=gzipped,
      response_headers={
        'Content-Type': 'application/json',
        'Content-Encoding': 'gzip',
        'Content-Length': str(len(gzipped)),
      },
      status_code=200,
      url='https://example.com/encoded-headers',
    ).with_settings(settings).build()[1]
    assert status == 200

    response = Response.last()
    headers = dict(RawHttpResponseAdapter(response.raw).headers)
    headers['X-Custom'] = '1'

    _res, update_status = local_db_response_adapter.update(response.id, headers=headers)

    assert update_status == 200
    raw_after = RawHttpResponseAdapter(Response.find(response.id).raw)
    assert raw_after.headers.get('Content-Encoding') == 'gzip'
    assert raw_after.headers.get('X-Custom') == '1'

  def test_it_rejects_adding_transfer_encoding(
    self, created_response: Response, local_db_response_adapter: LocalDBResponseAdapter
  ):
    from stoobly_agent.app.models.adapters.raw_http_response_adapter import RawHttpResponseAdapter

    headers = dict(RawHttpResponseAdapter(created_response.raw).headers)
    headers['Transfer-Encoding'] = 'chunked'

    res, status = local_db_response_adapter.update(created_response.id, headers=headers)

    assert status == 400
    assert res == 'Changing Transfer-Encoding is not allowed'

  def test_it_rejects_removing_transfer_encoding(
    self, settings: Settings, local_db_response_adapter: LocalDBResponseAdapter
  ):
    from stoobly_agent.app.models.adapters.raw_http_response_adapter import RawHttpResponseAdapter

    body = b'ok'
    status = RequestBuilder(
      method='GET',
      request_body='',
      response_body=body,
      response_headers={
        'Content-Type': 'text/plain',
        'Transfer-Encoding': 'chunked',
      },
      status_code=200,
      url='https://example.com/chunked',
    ).with_settings(settings).build()[1]
    assert status == 200

    response = Response.last()
    headers = dict(RawHttpResponseAdapter(response.raw).headers)
    headers.pop('Transfer-Encoding', None)
    headers.pop('transfer-encoding', None)

    res, update_status = local_db_response_adapter.update(response.id, headers=headers)

    assert update_status == 400
    assert res == 'Changing Transfer-Encoding is not allowed'

    raw_after = RawHttpResponseAdapter(Response.find(response.id).raw)
    assert raw_after.headers.get('Transfer-Encoding') == 'chunked'
