import pdb
import pytest

from stoobly_agent.app.proxy.test.iterable_matches import dict_fuzzy_matches, list_fuzzy_matches, list_matches
from stoobly_agent.app.proxy.test.response_param_names_facade import ResponseParamNamesFacade
from stoobly_agent.test.mock_data.endpoint_show_response import endpoint_show_response

@pytest.fixture
def endpoints_list_response_param_names_facade():
  response_param_names = endpoint_show_response['response_param_names']
  return ResponseParamNamesFacade(response_param_names)

@pytest.fixture
def empty_response_param_names_facade():
  response_param_names = endpoint_show_response['response_param_names']
  return ResponseParamNamesFacade(response_param_names)

class TestListMatchesList():

  def test_matches_list_of_numbers(self, empty_response_param_names_facade):
    matches, log = list_matches([1], [1], empty_response_param_names_facade)
    assert matches, log

  def test_not_matches_list_of_numbers(self, empty_response_param_names_facade):
    matches, log = list_matches([1], [2], empty_response_param_names_facade)
    assert not matches, log

  def test_not_matches_different_length(self, empty_response_param_names_facade):
    matches, log = list_matches([1], [1, 2], empty_response_param_names_facade)
    assert not matches, log

class TestListFuzzyMatchesListOfDicts():

  def test_matches_empty_response(self, endpoints_list_response_param_names_facade):
    matches, log = list_fuzzy_matches([], [], endpoints_list_response_param_names_facade)
    assert matches, log

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

    matches, log = list_fuzzy_matches(expected, actual, endpoints_list_response_param_names_facade)
    assert matches, log

class TestListMatchesListOfDicts():
  def test_matches_empty_response(self, endpoints_list_response_param_names_facade):
    matches, log = list_matches([], [], endpoints_list_response_param_names_facade)
    assert matches, log

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

    matches, log = list_matches(expected, actual, endpoints_list_response_param_names_facade)
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

    matches, log = list_matches(expected, actual, endpoints_list_response_param_names_facade)
    assert not matches, log