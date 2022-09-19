import pdb
import pytest

from stoobly_agent.app.proxy.test.helpers.request_component_names_facade import RequestComponentNamesFacade
from stoobly_agent.app.proxy.test.matchers.context import MatchContext
from stoobly_agent.app.proxy.test.matchers.fuzzy import list_matches
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

class TestMatchesFuzzySanity():
  def test_matches_empty_response(self, endpoints_list_response_param_names_facade):
    matches, log = list_matches(
      MatchContext({
        'path_key': '', 'query': '', 'request_component_names_facade': endpoints_list_response_param_names_facade
      }),
      [], []
    )
    assert matches, log

  def test_matches_list_of_numbers(self, empty_response_param_names_facade):
    matches, log = list_matches(
      MatchContext({
        'path_key': '', 'query': '', 'request_component_names_facade': empty_response_param_names_facade
      }),
      [1], [2]
    )
    assert matches, log

  def test_not_matches_mixed(self, endpoints_list_response_param_names_facade):
    matches, log = list_matches(
      MatchContext({
        'path_key': '', 'query': '', 'request_component_names_facade': endpoints_list_response_param_names_facade
      }),
      [{}], [{}, 1]
    )
    
    assert log == "Key '[1]' type did not match: got <class 'int'>, expected valid types <class 'dict'>", log 

  def test_not_matches(self, endpoints_list_response_param_names_facade):
    matches, log = list_matches(
      MatchContext({
        'path_key': '', 'query': '', 'request_component_names_facade': endpoints_list_response_param_names_facade
      }),
      [], {}
    )
    assert log == "Key '' type did not match: got <class 'dict'>, expected <class 'list'>", log 

class TestFuzzyMatchesListOfDicts():

  def test_matches_response_one_object(self, endpoints_list_response_param_names_facade):
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