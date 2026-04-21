import json

import pytest
import requests

from stoobly_agent.app.models.adapters.python import PythonRequestAdapterFactory
from stoobly_agent.app.models.factories.resource.local_db.helpers.filter_requests_by_hashes_service import (
  component_hashes,
  filter_requests_by_hashes,
)
from stoobly_agent.app.models.factories.resource.local_db.helpers.request_builder import RequestBuilder
from stoobly_agent.app.proxy.mitmproxy.request_facade import MitmproxyRequestFacade
from stoobly_agent.app.proxy.mock.hashed_request_decorator import COMPONENT_TYPES, HashedRequestDecorator
from stoobly_agent.app.settings import Settings
from stoobly_agent.lib.orm.request import Request
from stoobly_agent.test.test_helper import reset

class TestComponentHashes():
  def test_it_selects_supported_hash_keys(self):
    hashes = component_hashes({
      'host': 'example.com',
      'query_params_hash': 'a',
      'headers_hash': 'b',
      'compute': 1,
      'retry': 1,
    })

    assert hashes == {
      'query_params_hash': 'a',
      'headers_hash': 'b',
    }

class TestFilterRequestsByHashes():
  @pytest.fixture(autouse=True, scope='class')
  def settings(self):
    return reset()

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

  def test_it_filters_using_ignored_query_param_hash(self, created_request: Request):
    ignored_components = [
      {'type': 3, 'name': 'b'},
    ]

    python_request = requests.Request(
      method='GET',
      url='https://example.com/v1/search?a=1&b=3',
      headers={'x-token': 'abc'},
    )
    mitmproxy_request = PythonRequestAdapterFactory(python_request).mitmproxy_request()
    hashed_request = HashedRequestDecorator(MitmproxyRequestFacade(mitmproxy_request)).with_ignored_components(ignored_components)

    matches = filter_requests_by_hashes(
      [created_request],
      { 'query_params_hash': hashed_request.query_params_hash() },
      ignored_components
    )

    assert len(matches) == 1
    assert matches[0].id == created_request.id

  def test_it_requires_all_provided_hashes_to_match(self, created_request: Request):
    ignored_components = [
      {'type': 3, 'name': 'b'},
    ]

    python_request = requests.Request(
      method='GET',
      url='https://example.com/v1/search?a=1&b=3',
      headers={'x-token': 'abc'},
    )
    mitmproxy_request = PythonRequestAdapterFactory(python_request).mitmproxy_request()
    hashed_request = HashedRequestDecorator(MitmproxyRequestFacade(mitmproxy_request)).with_ignored_components(ignored_components)

    matches = filter_requests_by_hashes(
      [created_request],
      {
        'query_params_hash': hashed_request.query_params_hash(),
        'body_text_hash': 'not-a-match',
      },
      ignored_components
    )

    assert len(matches) == 0

  def test_it_filters_using_ignored_body_param(self, settings: Settings):
    status = RequestBuilder(
      method='POST',
      request_body={'a': 1, 'b': 2},
      request_headers={'Content-Type': 'application/json'},
      response_body='ok',
      status_code=200,
      url='https://example.com/v1/resource',
    ).with_settings(settings).build()[1]
    assert status == 200

    created_request = Request.last()

    try:
      ignored_components = [
        {'type': COMPONENT_TYPES['BODY_PARAM'], 'name': 'b', 'query': 'b'},
      ]

      python_request = requests.Request(
        method='POST',
        url='https://example.com/v1/resource',
        headers={'Content-Type': 'application/json'},
        data=json.dumps({'a': 1, 'b': 99}),
      )
      mitmproxy_request = PythonRequestAdapterFactory(python_request).mitmproxy_request()
      hashed_request = HashedRequestDecorator(MitmproxyRequestFacade(mitmproxy_request)).with_ignored_components(ignored_components)

      matches = filter_requests_by_hashes(
        [created_request],
        {'body_params_hash': hashed_request.body_params_hash()},
        ignored_components,
      )

      assert len(matches) == 1
      assert matches[0].id == created_request.id
    finally:
      created_request.delete()

  def test_it_filters_using_ignored_nested_body_param(self, settings: Settings):
    status = RequestBuilder(
      method='POST',
      request_body={'user': {'id': 1, 'name': 'alice'}, 'meta': {'version': 1}},
      request_headers={'Content-Type': 'application/json'},
      response_body='ok',
      status_code=200,
      url='https://example.com/v1/resource',
    ).with_settings(settings).build()[1]
    assert status == 200

    created_request = Request.last()

    try:
      ignored_components = [
        {'type': COMPONENT_TYPES['BODY_PARAM'], 'name': 'name', 'query': 'user.name'},
      ]

      python_request = requests.Request(
        method='POST',
        url='https://example.com/v1/resource',
        headers={'Content-Type': 'application/json'},
        data=json.dumps({'user': {'id': 1, 'name': 'bob'}, 'meta': {'version': 1}}),
      )
      mitmproxy_request = PythonRequestAdapterFactory(python_request).mitmproxy_request()
      hashed_request = HashedRequestDecorator(MitmproxyRequestFacade(mitmproxy_request)).with_ignored_components(ignored_components)

      matches = filter_requests_by_hashes(
        [created_request],
        {'body_params_hash': hashed_request.body_params_hash()},
        ignored_components,
      )

      assert len(matches) == 1
      assert matches[0].id == created_request.id
    finally:
      created_request.delete()
