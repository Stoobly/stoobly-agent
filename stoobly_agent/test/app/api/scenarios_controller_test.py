import json
from unittest.mock import MagicMock

import pytest

from stoobly_agent.app.api.scenarios_controller import ScenariosController
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
  ScenariosController._instance = None
  return ScenariosController.instance()


@pytest.fixture
def mock_context():
  context = MagicMock()
  context.render = MagicMock()
  context.bad_request = MagicMock()
  context.filter_response = lambda res, status: status >= 400
  context.params = {}
  context.headers = {}
  return context


def _minimal_har():
  return {
    'log': {
      'entries': [
        {
          '_resourceType': 'xhr',
          'request': {
            'method': 'GET',
            'url': 'https://example.com/api/pets',
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


class TestScenariosControllerCreate:

  def test_it_creates_without_file(self, controller, mock_context):
    mock_context.params = {'name': 'plain-scenario'}

    controller.create(mock_context)

    mock_context.render.assert_called_once()
    _, kwargs = mock_context.render.call_args
    assert kwargs['status'] == 200
    assert kwargs['json']['name'] == 'plain-scenario'
    assert Scenario.find_by(uuid=kwargs['json']['uuid']) is not None

  def test_it_imports_har_file(self, controller, mock_context):
    mock_context.params = {
      'name': 'har-scenario',
      'format': 'har',
      'file': json.dumps(_minimal_har()),
    }

    controller.create(mock_context)

    mock_context.render.assert_called_once()
    _, kwargs = mock_context.render.call_args
    assert kwargs['status'] == 200
    scenario = Scenario.find_by(uuid=kwargs['json']['uuid'])
    assert scenario.requests.count() == 1
    assert scenario.requests.first().path == '/api/pets'

  def test_it_imports_gor_file(self, controller, mock_context, settings: Settings):
    status = RequestBuilder(
      method='GET',
      url='https://example.com/gor-pet',
      request_body=b'',
      request_headers={},
      response_body=b'{}',
      response_headers={},
      status_code=200,
    ).with_settings(settings).build()[1]
    assert status == 200
    gor = JoinedRequestStringAdapter(Request.last()).adapt()

    mock_context.params = {
      'name': 'gor-scenario',
      'format': 'gor',
      'file': gor,
    }

    controller.create(mock_context)

    mock_context.render.assert_called_once()
    _, kwargs = mock_context.render.call_args
    assert kwargs['status'] == 200
    scenario = Scenario.find_by(uuid=kwargs['json']['uuid'])
    assert scenario.requests.count() == 1
    assert scenario.requests.first().path == '/gor-pet'

  def test_it_rejects_invalid_format(self, controller, mock_context):
    mock_context.params = {
      'name': 'bad-format',
      'format': 'xml',
      'file': b'{}',
    }

    controller.create(mock_context)

    mock_context.bad_request.assert_called_once()
    mock_context.render.assert_not_called()

  def test_it_rejects_format_without_file(self, controller, mock_context):
    mock_context.params = {
      'name': 'missing-file',
      'format': 'har',
    }

    controller.create(mock_context)

    mock_context.bad_request.assert_called_once()
    mock_context.render.assert_not_called()

  def test_it_destroys_scenario_when_import_fails(self, controller, mock_context):
    before = Scenario.count()
    mock_context.params = {
      'name': 'orphan-scenario',
      'format': 'har',
      'file': '{"log": null}',
    }

    controller.create(mock_context)

    mock_context.bad_request.assert_called_once()
    mock_context.render.assert_not_called()
    assert Scenario.count() == before
    assert Scenario.find_by(name='orphan-scenario') is None
