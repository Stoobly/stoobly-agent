import pdb
import pytest

from stoobly_agent.app.proxy.test.helpers.request_component_names_facade import RequestComponentNamesFacade
from stoobly_agent.app.proxy.test.matchers.context import MatchContext
from stoobly_agent.app.proxy.test.matchers.contract import list_matches
from stoobly_agent.config.constants.lifecycle_hooks import ON_PARAM_NAME_MISSING_ERROR
from stoobly_agent.test.mock_data.endpoint_show_response import endpoint_show_response

@pytest.fixture
def endpoints_list_response_param_names_facade():
  response_param_names = endpoint_show_response['response_param_names']
  aliases = endpoint_show_response['aliases']
  return RequestComponentNamesFacade(response_param_names).with_aliases(aliases)

class TestListMatchesList():

  def test_matches(self, endpoints_list_response_param_names_facade: RequestComponentNamesFacade):
    matches, log = list_matches(
      MatchContext({
        'path_key': '', 'query': '', 'request_component_names_facade': endpoints_list_response_param_names_facade
      }),
      [{
        "id": 934,
        "requests_count": 2,
        "category": 2,
        "path": "/users/:userId",
        "method": "GET",
        "created_at": "2022-05-31T06:00:10.663Z",
        "updated_at": "2022-05-31T06:00:10.663Z",
        "components": [],
        "url": "https://alpha.api.stoobly.com/endpoints/934"
      }]
    )
    assert matches, log

  def test_not_matches_list_type(self, endpoints_list_response_param_names_facade: RequestComponentNamesFacade):
    matches, log = list_matches(
      MatchContext({
        'path_key': '', 'query': '', 'request_component_names_facade': endpoints_list_response_param_names_facade
      }),
      [1], strict=True
    )

    assert not matches
    assert log == "Key '[0]' type did not match: got <class 'int'>, expected valid types Hash", log

  def test_not_matches_list_element_type(self, endpoints_list_response_param_names_facade: RequestComponentNamesFacade):
    lifecycle_hooks = {}
    lifecycle_hooks[ON_PARAM_NAME_MISSING_ERROR] = lambda context, actual: True # Ignore this error

    match_context = MatchContext({
      'lifecycle_hooks': lifecycle_hooks, 'path_key': '', 'query': '', 'request_component_names_facade': endpoints_list_response_param_names_facade 
    })

    matches, log = list_matches(
      match_context, [{ "id": "934" }], strict=True
    )

    assert not matches
    assert log == "Key '[0].id' type did not match: got <class 'str'>, expected valid types Integer", log

  def test_not_matches_list_element_missing_properties(self, endpoints_list_response_param_names_facade: RequestComponentNamesFacade):  
    match_context = MatchContext({
      'path_key': '', 'query': '', 'request_component_names_facade': endpoints_list_response_param_names_facade
    })

    matches, log = list_matches(
      match_context, [{ "id": 934 }], strict=True
    )

    assert not matches
    assert log == "Missing key: expected [0].requests_count to exist", log

  def test_not_matches_list_element_properties(self, endpoints_list_response_param_names_facade: RequestComponentNamesFacade):
    lifecycle_hooks = {}
    lifecycle_hooks[ON_PARAM_NAME_MISSING_ERROR] = lambda context, actual: True # Ignore this error
    match_context = MatchContext({
      'lifecycle_hooks': lifecycle_hooks, 'path_key': '', 'query': '', 'request_component_names_facade': endpoints_list_response_param_names_facade
    })

    matches, log = list_matches(
      match_context, [{ "random_property": 934 }], strict=True
    )

    assert not matches
    assert log == "Extra key: expected [0].random_property to not exist", log

  def test_not_matches_list_length(self, endpoints_list_response_param_names_facade: RequestComponentNamesFacade):
    match_context = MatchContext({
      'path_key': '', 'query': '', 'request_component_names_facade': endpoints_list_response_param_names_facade
    })

    matches, log = list_matches(
      match_context, [], strict=True
    )

    assert not matches
    assert log == "Key '[*]' length did not match: got 0", log

  def test_not_matches_list(self, endpoints_list_response_param_names_facade: RequestComponentNamesFacade):
    match_context = MatchContext({
      'path_key': '', 'query': '', 'request_component_names_facade': endpoints_list_response_param_names_facade
    })

    matches, log = list_matches(
      match_context, {}, strict=True
    )
    
    assert not matches
    assert log == "Key '[*]' type did not match: got <class 'dict'>, expected <class 'list'>", log