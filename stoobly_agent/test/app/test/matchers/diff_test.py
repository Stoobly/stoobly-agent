import pdb
import pytest

from stoobly_agent.app.proxy.test.helpers.request_component_names_facade import RequestComponentNamesFacade
from stoobly_agent.app.proxy.test.matchers.context import MatchContext
from stoobly_agent.app.proxy.test.matchers.diff import list_matches
from stoobly_agent.config.constants import test_filter
from stoobly_agent.lib.orm.trace import Trace
from stoobly_agent.lib.orm.trace_alias import TraceAlias
from stoobly_agent.test.mock_data.endpoint_show_response import endpoint_show_response

@pytest.fixture
def endpoints_list_response_param_names_facade():
  response_param_names = endpoint_show_response['response_param_names']
  aliases = endpoint_show_response['aliases']
  return RequestComponentNamesFacade(response_param_names).with_aliases(aliases)

@pytest.fixture
def empty_response_param_names_facade():
  response_param_names = []
  return RequestComponentNamesFacade(response_param_names)

class TestMatchesDiffSanity():
  def test_matches_empty_response(self, endpoints_list_response_param_names_facade):
    matches, log = list_matches(
      MatchContext({
        'path_key': '', 'query': '', 'request_component_names_facade': endpoints_list_response_param_names_facade
      }),
      [], [], 
    )
    assert matches, log
  
  def test_matches_list_of_numbers(self, empty_response_param_names_facade):
    matches, log = list_matches(
      MatchContext({
        'path_key': '', 'query': '', 'request_component_names_facade': empty_response_param_names_facade
      }),
      [1], [1]
    )
    assert matches, log

  def test_not_matches(self, endpoints_list_response_param_names_facade):
    matches, log = list_matches(
      MatchContext({
        'path_key': '', 'query': '', 'request_component_names_facade': endpoints_list_response_param_names_facade
      }),
      [], {}
    )
    assert log == "Key '' type did not match: got <class 'dict'>, expected <class 'list'>", log

  def test_not_matches_list_of_numbers(self, empty_response_param_names_facade):
    matches, log = list_matches(
      MatchContext({
        'path_key': '', 'query': '', 'request_component_names_facade': empty_response_param_names_facade
      }),
      [1], [2]
    )

    assert log == "Key '[0]' did not match: got 2, expected 1", log

  def test_not_matches_different_length(self, empty_response_param_names_facade):
    matches, log = list_matches(
      MatchContext({
        'path_key': '', 'query': '', 'request_component_names_facade': empty_response_param_names_facade
      }),
      [1], [1, 2]
    )

    assert log == "Key '' length did not match: got 2, expected 1", log

class TestMatchesListOfDicts():
  def test_matches_id_not_deterministic(self, endpoints_list_response_param_names_facade):
    actual = [
      {
        "id": 1000,
        "requests_count": 6,
        "category": 1,
        "path": "/abc",
        "method": "GET",
        "created_at": "2022-05-26T23:46:49.968Z",
        "updated_at": "2022-05-26T23:46:49.968Z",
        "components": [],
        "url": "https://alpha.api.stoobly.com/endpoints/930"
      },
    ]

    expected = [
      {
        "id": 930,
        "requests_count": 6,
        "category": 1,
        "path": "/abc",
        "method": "GET",
        "created_at": "2022-05-26T23:46:49.968Z",
        "updated_at": "2022-05-26T23:46:49.968Z",
        "components": [],
        "url": "https://alpha.api.stoobly.com/endpoints/930"
      },
    ] 

    matches, log = list_matches(
      MatchContext({
        'path_key': '', 'query': '', 'request_component_names_facade': endpoints_list_response_param_names_facade
      }),
      expected, actual
    )
    assert matches, log

  def test_not_matches_requests_count(self, endpoints_list_response_param_names_facade):
    actual = [
      {
        "id": 1000,
        "requests_count": 8,
        "category": 2,
        "path": "/abc",
        "method": "POST",
        "created_at": "2022-05-26T23:46:49.968Z",
        "updated_at": "2022-05-26T23:46:49.968Z",
        "components": [],
        "url": "https://alpha.api.stoobly.com/endpoints/930"
      },
    ]

    expected = [
      {
        "id": 1000,
        "requests_count": 6,
        "category": 2,
        "path": "/abc",
        "method": "POST",
        "created_at": "2022-05-26T23:46:49.968Z",
        "updated_at": "2022-05-26T23:46:49.968Z",
        "components": [],
        "url": "https://alpha.api.stoobly.com/endpoints/930"
      },
    ] 

    matches, log = list_matches(
      MatchContext({
        'path_key': '', 'query': '', 'request_component_names_facade': endpoints_list_response_param_names_facade
      }),
      expected, actual
    )

    assert log == "Key '[0].requests_count' did not match: got 8, expected 6", log

class TestAliasFilterMatchesListOfDicts():
  def test_matches_id_aliased(self, endpoints_list_response_param_names_facade: RequestComponentNamesFacade):
    endpoints_list_response_param_names_facade.with_filter(test_filter.ALIAS)

    actual = [
      {
        "id": 1000,
        "requests_count": 6,
        "category": 1,
        "path": "/abc",
        "method": "GET",
        "created_at": "2022-05-26T23:46:49.968Z",
        "updated_at": "2022-05-26T23:46:49.968Z",
        "components": [],
        "url": "https://alpha.api.stoobly.com/endpoints/930"
      },
    ]

    expected = [
      {
        "id": 1000,
        "requests_count": 6,
        "category": 2,
        "path": "/abcdef",
        "method": "POST",
        "created_at": "2022-05-26T23:46:49.968Z",
        "updated_at": "2022-05-26T23:46:49.968Z",
        "components": None,
        "url": "https://alpha.api.stoobly.com/endpoints/931"
      },
    ] 

    matches, log = list_matches(
      MatchContext({
        'path_key': '', 'query': '', 'request_component_names_facade': endpoints_list_response_param_names_facade
      }),
      expected, actual
    )
    assert matches, log

  def test_not_matches_id_aliased(self, endpoints_list_response_param_names_facade: RequestComponentNamesFacade):
    endpoints_list_response_param_names_facade.with_filter(test_filter.ALIAS)

    # Set aliased params as deterministic to prevent ignore due to not deterministic
    for response_param_name in endpoints_list_response_param_names_facade.aliased:
      response_param_name['is_deterministic'] = True

    actual = [
      {
        "id": 1000,
        "requests_count": 6,
        "category": 1,
        "path": "/abc",
        "method": "GET",
        "created_at": "2022-05-26T23:46:49.968Z",
        "updated_at": "2022-05-26T23:46:49.968Z",
        "components": [],
        "url": "https://alpha.api.stoobly.com/endpoints/930"
      },
    ]

    expected = [
      {
        "id": 1001,
        "requests_count": 6,
        "category": 2,
        "path": "/abcdef",
        "method": "POST",
        "created_at": "2022-05-26T23:46:49.968Z",
        "updated_at": "2022-05-26T23:46:49.968Z",
        "components": None,
        "url": "https://alpha.api.stoobly.com/endpoints/931"
      },
    ] 

    matches, log = list_matches(
      MatchContext({
        'path_key': '', 'query': '', 'request_component_names_facade': endpoints_list_response_param_names_facade
      }),
      expected, actual
    )

    assert log == "Key '[0].id' did not match: got 1000, expected 1001", log

  class TestLinkFilterMatchesListOfDicts():
    def test_matches_id_aliased(self, endpoints_list_response_param_names_facade: RequestComponentNamesFacade):
      trace = Trace.create()

      TraceAlias.create(trace_id=trace.id, name=':endpointId', value=1001)
      TraceAlias.create(trace_id=trace.id, name=':endpointRequestCounts', value=2)

      endpoints_list_response_param_names_facade.with_filter(test_filter.LINK).with_trace(trace)

      actual = [
        {
          "id": 1000, # Aliased as :endpointId
          "requests_count": 7, # Aliased as :endpointRequestsCount
          "category": 1,
          "path": "/abc",
          "method": "GET",
          "created_at": "2022-05-26T23:46:49.968Z",
          "updated_at": "2022-05-26T23:46:49.968Z",
          "components": [],
          "url": "https://alpha.api.stoobly.com/endpoints/930"
        },
      ]

      expected = [
        {
          "id": 1000,
          "requests_count": 7,
          "category": 2,
          "path": "/abcdef",
          "method": "POST",
          "created_at": "2022-05-26T23:46:49.968Z",
          "updated_at": "2022-05-26T23:46:49.968Z",
          "components": None,
          "url": "https://alpha.api.stoobly.com/endpoints/931"
        },
      ] 

      matches, log = list_matches(
        MatchContext({
          'path_key': '', 'query': '', 'request_component_names_facade': endpoints_list_response_param_names_facade
        }),
        expected, actual
      )
      assert matches, log

    def test_not_matches_id_aliased(self, endpoints_list_response_param_names_facade: RequestComponentNamesFacade):
      trace = Trace.create()

      TraceAlias.create(trace_id=trace.id, name=':endpointId', value=1001)

      endpoints_list_response_param_names_facade.with_filter(test_filter.LINK).with_trace(trace)

      actual = [
        {
          "id": 1001, # Aliased as :endpointId
          "requests_count": 8, # Aliased as :endpointRequestsCount
          "category": 1,
          "path": "/abc",
          "method": "GET",
          "created_at": "2022-05-26T23:46:49.968Z",
          "updated_at": "2022-05-26T23:46:49.968Z",
          "components": [],
          "url": "https://alpha.api.stoobly.com/endpoints/930"
        },
      ]

      expected = [
        {
          "id": 1000,
          "requests_count": 7,
          "category": 2,
          "path": "/abcdef",
          "method": "POST",
          "created_at": "2022-05-26T23:46:49.968Z",
          "updated_at": "2022-05-26T23:46:49.968Z",
          "components": None,
          "url": "https://alpha.api.stoobly.com/endpoints/931"
        },
      ] 

      matches, log = list_matches(
        MatchContext({
          'path_key': '', 'query': '', 'request_component_names_facade': endpoints_list_response_param_names_facade
        }), 
        expected, actual, 
      )

      assert log == "Key '[0].id' did not match: got 1001, expected 1000", log