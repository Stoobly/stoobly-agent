import json
from unittest.mock import MagicMock

import pytest

from stoobly_agent.app.api.requests_controller import RequestsController
from stoobly_agent.app.models.adapters.orm import JoinedRequestStringAdapter
from stoobly_agent.app.models.factories.resource.local_db.helpers.request_builder import RequestBuilder
from stoobly_agent.app.settings import Settings
from stoobly_agent.lib.orm.request import Request
from stoobly_agent.lib.orm.scenario import Scenario
from stoobly_agent.test.test_helper import reset


@pytest.fixture(autouse=True, scope='module')
def settings():
  return reset()


@pytest.fixture
def controller():
  RequestsController._instance = None
  return RequestsController.instance()


@pytest.fixture
def mock_context():
  context = MagicMock()
  context.render = MagicMock()
  context.bad_request = MagicMock()
  context.filter_response = lambda res, status: status >= 400
  context.params = {}
  context.headers = {}
  return context


def _minimal_har(url='https://example.com/api/pets'):
  return {
    'log': {
      'entries': [
        {
          '_resourceType': 'xhr',
          'request': {
            'method': 'GET',
            'url': url,
            'headers': [],
            'httpVersion': 'HTTP/1.1',
          },
          'response': {
            'status': 200,
            'headers': [],
            'content': {'text': '{}', 'size': 2},
          },
        }
      ]
    }
  }


class TestRequestsControllerCreate:

  def test_it_defaults_to_gor(self, controller, mock_context, settings: Settings):
    status = RequestBuilder(
      method='GET',
      url='https://example.com/default-gor',
      request_body=b'',
      request_headers={},
      response_body=b'{}',
      response_headers={},
      status_code=200,
    ).with_settings(settings).build()[1]
    assert status == 200
    gor = JoinedRequestStringAdapter(Request.last()).adapt()
    before = Request.count()

    mock_context.params = {'requests': gor}
    controller.create(mock_context)

    mock_context.render.assert_called_once()
    _, kwargs = mock_context.render.call_args
    assert kwargs['status'] == 200
    assert kwargs['json']['total'] == 1
    assert Request.count() == before + 1

  def test_it_imports_har_format(self, controller, mock_context):
    before = Request.count()
    mock_context.params = {
      'requests': json.dumps(_minimal_har()),
      'format': 'har',
    }

    controller.create(mock_context)

    mock_context.render.assert_called_once()
    _, kwargs = mock_context.render.call_args
    assert kwargs['status'] == 200
    assert kwargs['json']['total'] == 1
    assert Request.count() == before + 1
    assert Request.last().path == '/api/pets'

  def test_it_imports_gor_format_explicitly(self, controller, mock_context, settings: Settings):
    status = RequestBuilder(
      method='GET',
      url='https://example.com/explicit-gor',
      request_body=b'',
      request_headers={},
      response_body=b'{}',
      response_headers={},
      status_code=200,
    ).with_settings(settings).build()[1]
    assert status == 200
    gor = JoinedRequestStringAdapter(Request.last()).adapt()

    mock_context.params = {
      'requests': gor,
      'format': 'gor',
    }
    controller.create(mock_context)

    mock_context.render.assert_called_once()
    _, kwargs = mock_context.render.call_args
    assert kwargs['status'] == 200
    assert kwargs['json']['total'] == 1

  def test_it_assigns_scenario_id(self, controller, mock_context):
    scenario = Scenario.create(name='request-create-har-scenario')
    mock_context.params = {
      'requests': json.dumps(_minimal_har('https://example.com/assigned')),
      'format': 'har',
      'scenario_id': scenario.id,
    }

    controller.create(mock_context)

    created = Request.last()
    assert created.scenario_id == scenario.id

  def test_it_rejects_invalid_format(self, controller, mock_context):
    mock_context.params = {
      'requests': b'{}',
      'format': 'xml',
    }

    controller.create(mock_context)

    mock_context.bad_request.assert_called_once()
    mock_context.render.assert_not_called()
