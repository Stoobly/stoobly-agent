import json

import pytest

from stoobly_agent.app.models.adapters.orm import JoinedRequestStringAdapter
from stoobly_agent.app.models.factories.resource.local_db.helpers.request_builder import RequestBuilder
from stoobly_agent.app.models.import_.har_importer import HarImporter, looks_like_gor
from stoobly_agent.app.proxy.record import REQUEST_DELIMITTER
from stoobly_agent.app.settings import Settings
from stoobly_agent.lib.orm.request import Request
from stoobly_agent.test.test_helper import reset


@pytest.fixture(autouse=True, scope='module')
def settings():
  return reset()


class TestLooksLikeGor:

  def test_it_detects_monkey_delimiter(self):
    assert looks_like_gor(b'1 abc' + REQUEST_DELIMITTER + b'2 abc')

  def test_it_detects_control_line(self):
    assert looks_like_gor(b'1 550e8400-e29b-41d4-a716-446655440000 1234567890\nGET / HTTP/1.1\r\n')

  def test_it_does_not_flag_har(self):
    har = json.dumps({'log': {'entries': []}})
    assert not looks_like_gor(har)


class TestHarImporterWrongFormat:

  def test_it_returns_clear_error_for_gor_content(self, settings: Settings):
    status = RequestBuilder(
      method='GET',
      url='https://example.com/pets',
      request_body=b'',
      request_headers={},
      response_body=b'{}',
      response_headers={},
      status_code=200,
    ).with_settings(settings).build()[1]
    assert status == 200

    gor = JoinedRequestStringAdapter(Request.last()).adapt()
    res, status = HarImporter().import_file(gor, scenario_id=None, settings=settings)

    assert status == 400
    assert 'GOR' in res['error']
    assert 'format GOR' in res['error']
    assert 'Extra data' not in res['error']
    assert 'Invalid JSON' not in res['error']


class TestGorImporterWrongFormat:

  def test_it_returns_clear_error_for_har_content(self, settings: Settings):
    from stoobly_agent.app.models.import_.gor_importer import GorImporter, looks_like_har

    har = json.dumps({
      'log': {
        'entries': [
          {
            '_resourceType': 'xhr',
            'request': {'method': 'GET', 'url': 'https://example.com/x', 'headers': []},
            'response': {'status': 200, 'headers': [], 'content': {'text': '{}'}},
          }
        ]
      }
    })
    assert looks_like_har(har)

    res, status = GorImporter().import_file(har, scenario_id=None, settings=settings)
    assert status == 400
    assert 'HAR' in res['error']
    assert 'format HAR' in res['error']
