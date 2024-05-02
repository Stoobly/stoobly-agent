import json
import pdb
import pytest

from mitmproxy.http import Headers, Request as MitmproxyRequest
from time import time

from stoobly_agent.app.settings.constants import intercept_mode, request_component
from stoobly_agent.app.proxy.mitmproxy.request_facade import MitmproxyRequestFacade
from stoobly_agent.app.settings.rewrite_rule import RewriteRule

@pytest.fixture
def mitmproxy_get_request():
  now = time()
  return MitmproxyRequest(
    'stoobly.com',
    443,
    b'GET',
    b'https',
    b'stoobly.com:443',
    b'/requests?project_id=1',
    b'HTTP/1.1',
    Headers(**{'access-token': b'123'}),
    b'',
    Headers(), # Trailers
    now,
    now + 1,
  )

@pytest.fixture
def mitmproxy_post_request():
  now = time()
  return MitmproxyRequest(
    'stoobly.com',
    443,
    b'POST',
    b'https',
    b'stoobly.com:443',
    b'/users?project_id=1',
    b'HTTP/1.1',
    Headers(**{'content-type': b'application/json'}),
    json.dumps({'name': 'Alice', 'age': 20}).encode(),
    Headers(), # Trailers
    now,
    now + 1,
  )

class TestRewriteParams():

  def test_rewrites_header(self, mitmproxy_get_request: MitmproxyRequest):
    parameter_rule = {
      'modes': [intercept_mode.RECORD],
      'name': 'access-token',
      'type': request_component.HEADER,
      'value': '',
    }
    rewrite_rule = RewriteRule({
      'methods': ['GET'],
      'pattern': '.*?/requests',
      'parameter_rules': [parameter_rule]
    })

    facade = MitmproxyRequestFacade(mitmproxy_get_request)
    facade.with_parameter_rules([rewrite_rule])
    facade.rewrite()

    headers = facade.headers
    assert headers['access-token'] == ''

  def test_rewrites_query_param(self, mitmproxy_get_request: MitmproxyRequest):
    parameter_rule = {
      'modes': [intercept_mode.RECORD],
      'name': 'project_id',
      'type': request_component.QUERY_PARAM,
      'value': '',
    }
    rewrite_rule = RewriteRule({
      'methods': ['GET'],
      'pattern': '.*?/requests',
      'parameter_rules': [parameter_rule]
    })

    facade = MitmproxyRequestFacade(mitmproxy_get_request)
    facade.with_parameter_rules([rewrite_rule])
    facade.rewrite()

    query_params = facade.query
    assert query_params['project_id'] == ''
 
  def test_rewrites_body_param(self, mitmproxy_post_request: MitmproxyRequest):
    parameter_rule = {
      'modes': [intercept_mode.RECORD],
      'name': 'age',
      'type': request_component.BODY_PARAM,
      'value': '',
    }
    rewrite_rule = RewriteRule({
      'methods': ['POST'],
      'pattern': '.*?/users',
      'parameter_rules': [parameter_rule]
    })

    facade = MitmproxyRequestFacade(mitmproxy_post_request)
    facade.with_parameter_rules([rewrite_rule])
    facade.rewrite()

    body = facade.body
    body_params = json.loads(body)
    assert body_params['age'] == '' 

class TestRewriteUrl():

  def test_rewrites_hostname(self, mitmproxy_get_request: MitmproxyRequest):
    hostname = 'test'
    url_rule = {
      'modes': [intercept_mode.RECORD],
      'hostname': hostname,
    }
    rewrite_rule = RewriteRule({
      'methods': ['GET'],
      'pattern': '.*?/requests',
      'url_rules': [url_rule]
    })

    facade = MitmproxyRequestFacade(mitmproxy_get_request)
    facade.with_url_rules([rewrite_rule])

    assert facade.host != hostname

    facade.rewrite()

    assert facade.host == hostname

  def test_rewrites_port(self, mitmproxy_get_request: MitmproxyRequest):
    port = '8000'
    url_rule = {
      'modes': [intercept_mode.RECORD],
      'port': port,
    }
    rewrite_rule = RewriteRule({
      'methods': ['GET'],
      'pattern': '.*?/requests',
      'url_rules': [url_rule]
    })

    facade = MitmproxyRequestFacade(mitmproxy_get_request)
    facade.with_url_rules([rewrite_rule])

    assert facade.port != int(port)

    url_before = facade.url
    facade.rewrite()

    assert facade.port == int(port)
    assert url_before != facade.url

  def test_rewrites_scheme(self, mitmproxy_get_request: MitmproxyRequest):
    scheme = 'http'
    url_rule = {
      'modes': [intercept_mode.RECORD],
      'scheme': scheme,
    }
    rewrite_rule = RewriteRule({
      'methods': ['GET'],
      'pattern': '.*?/requests',
      'url_rules': [url_rule]
    })

    facade = MitmproxyRequestFacade(mitmproxy_get_request)
    facade.with_url_rules([rewrite_rule])

    assert facade.scheme != scheme

    url_before = facade.url
    facade.rewrite()

    assert facade.scheme == scheme
    assert url_before != facade.url

  def test_rewrites_path(self, mitmproxy_get_request: MitmproxyRequest):
    path = '/index.html'
    url_rule = {
      'modes': [intercept_mode.RECORD],
      'path': path
    }
    rewrite_rule = RewriteRule({
      'methods': ['GET'],
      'pattern': '.*?/requests',
      'url_rules': [url_rule]
    })

    facade = MitmproxyRequestFacade(mitmproxy_get_request)
    facade.with_url_rules([rewrite_rule])

    assert facade.path != path

    url_before = facade.url
    facade.rewrite()

    assert facade.path == path
    assert url_before != facade.url

  class TestWhenMultipleRules():

    def test_rewrites_hostname(self, mitmproxy_get_request: MitmproxyRequest):
      hostname1 = 'test1'
      url_rule1 = {
        'modes': [intercept_mode.RECORD],
        'hostname': hostname1,
      }
      hostname2 = 'test2'
      url_rule2 = {
        'modes': [intercept_mode.RECORD],
        'hostname': hostname2,
      }
      rewrite_rule = RewriteRule({
        'methods': ['GET'],
        'pattern': '.*?/requests',
        'url_rules': [url_rule1, url_rule2]
      })

      facade = MitmproxyRequestFacade(mitmproxy_get_request)
      facade.with_url_rules([rewrite_rule])
      facade.rewrite()

      assert facade.host == hostname2