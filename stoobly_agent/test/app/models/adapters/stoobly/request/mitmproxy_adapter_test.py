import base64
import json
import pdb

from mitmproxy.http import Request as MitmproxyRequest

from stoobly_agent.app.models.adapters.stoobly.request.mitmproxy_adapter import MitmproxyRequestAdapter
from stoobly_agent.app.models.schemas.request import Request
from stoobly_agent.lib.api.interfaces import RequestShowResponse

class TestMitmproxyRequestAdapter():

  def test_www_google_com(self):
    request = Request(RequestShowResponse(
      body='',
      components=[],
      created_at='',
      endpoint_id=0,
      headers=[
        {
          'name': 'Host',
          'value': 'www.google.com',
        },
        {
          'name': 'Content-Length',
          'value': '0',
        },
      ],
      host='www.google.com',
      http_version='HTTP/2.0',
      id='1',
      is_deleted=False,
      key='',
      latency=0,
      method='GET',
      path='/',
      port='443',
      query='',
      query_params=[],
      scheme='https',
      scenario='',
      scenario_id=0,
      sequence_id=None,
      starred=False,
      status=200,
      uuid='',
      url='https://www.google.com/',
    ))

    mitmproxy_request = MitmproxyRequestAdapter(request).adapt()

    assert isinstance(mitmproxy_request, MitmproxyRequest)
    assert mitmproxy_request.method == 'GET'
    assert mitmproxy_request.url == 'https://www.google.com/'
    assert mitmproxy_request.content == b''
    assert mitmproxy_request.http_version == 'HTTP/2.0'
    assert mitmproxy_request.headers.get('Host') == 'www.google.com'
    assert mitmproxy_request.headers.get('Content-Length') == '0'

  def test_stoobly_com(self):
    body = b'{"name": "test", "description": "test"}'

    request = Request(RequestShowResponse(
      body=base64.b64encode(body).decode(),
      components=[],
      created_at='',
      endpoint_id=0,
      headers=[
        {
          'name': 'Host',
          'value': 'stoobly.com',
        },
        {
          'name': 'Content-Type',
          'value': 'application/json',
        },
        {
          'name': 'Content-Length',
          'value': str(len(body)),
        },
      ],
      host='stoobly.com',
      http_version='HTTP/1.1',
      id='2',
      is_deleted=False,
      key='',
      latency=0,
      method='POST',
      path='/scenarios',
      port='443',
      query='',
      query_params=[],
      scheme='https',
      scenario='',
      scenario_id=0,
      sequence_id=None,
      starred=False,
      status=201,
      uuid='',
      url='https://stoobly.com/scenarios',
    ))

    mitmproxy_request = MitmproxyRequestAdapter(request).adapt()

    assert isinstance(mitmproxy_request, MitmproxyRequest)
    assert mitmproxy_request.method == 'POST'
    assert mitmproxy_request.url == 'https://stoobly.com/scenarios'
    assert mitmproxy_request.content == body
    assert mitmproxy_request.http_version == 'HTTP/1.1'
    assert mitmproxy_request.headers.get('Host') == 'stoobly.com'
    assert mitmproxy_request.headers.get('Content-Type') == 'application/json'
    assert mitmproxy_request.headers.get('Content-Length') == str(len(body))

  def test_query_params(self):
    request = Request(RequestShowResponse(
      body='',
      components=[],
      created_at='',
      endpoint_id=0,
      headers=[
        {
          'name': 'Host',
          'value': 'stoobly.com',
        },
      ],
      host='stoobly.com',
      http_version='HTTP/1.1',
      id='3',
      is_deleted=False,
      key='',
      latency=0,
      method='GET',
      path='/pets',
      port='443',
      query='name=test',
      query_params=[
        {
          'name': 'name',
          'value': 'test',
        },
      ],
      scheme='https',
      scenario='',
      scenario_id=0,
      sequence_id=None,
      starred=False,
      status=200,
      uuid='',
      url='https://stoobly.com/pets',
    ))

    mitmproxy_request = MitmproxyRequestAdapter(request).adapt()

    assert mitmproxy_request.url == 'https://stoobly.com/pets?name=test'
