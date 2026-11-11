import pdb
import pytest

from stoobly_agent.app.proxy.test.helpers.request_component_names_facade import RequestComponentNamesFacade
from stoobly_agent.app.proxy.test.matchers.context import MatchContext
from stoobly_agent.app.proxy.test.matchers.contract import dict_matches, list_matches
from stoobly_agent.config.constants.lifecycle_hooks import ON_PARAM_NAME_MISSING_ERROR
from stoobly_agent.test.mock_data.endpoint_show_response import endpoint_show_response

@pytest.fixture
def endpoints_list_response_param_names_facade():
  response_param_names = endpoint_show_response['response_param_names']
  aliases = endpoint_show_response['aliases']
  return RequestComponentNamesFacade(response_param_names).with_aliases(aliases)

def _param(id, name, query, inferred_type, parent_id=None, required=False, allows_additional=None):
  param = {
    'id': id,
    'name': name,
    'query': query,
    'inferred_type': inferred_type,
    'is_required': required,
    'is_deterministic': True,
    'response_param_name_id': parent_id,
  }
  if allows_additional is not None:
    param['allows_additional_properties'] = allows_additional
  return param

def _facade(response_param_names):
  return RequestComponentNamesFacade(response_param_names)

def _context(facade):
  return MatchContext({
    'path_key': '',
    'query': '',
    'request_component_names_facade': facade,
  })

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


class TestDictMatchesAdditionalProperties():

  def test_matches_dynamic_keys_against_additional_properties_schema(self):
    # Shape: { message: { [breed: string]: string[] } }
    # Open map of string arrays under a named field (dogs.ceo-style success path).
    facade = _facade([
      _param(1, 'message', 'message', 'Hash', required=True),
      _param(2, 'AdditionalProperty', 'message.*', 'Array', 1),
      _param(3, 'AdditionalPropertyElement', 'message.*[*]', 'String', 2),
    ])

    matches, log = dict_matches(
      _context(facade),
      {'message': {'terrier': ['american', 'border'], 'boxer': []}},
    )
    assert matches, log

  def test_fails_when_dynamic_value_type_does_not_match(self):
    # Shape: { message: { [breed: string]: string } }
    # Same map path, but values must be strings — arrays should fail.
    facade = _facade([
      _param(1, 'message', 'message', 'Hash', required=True),
      _param(2, 'AdditionalProperty', 'message.*', 'String', 1),
    ])

    matches, log = dict_matches(
      _context(facade),
      {'message': {'terrier': ['american']}},
    )
    assert not matches
    assert 'type did not match' in log

  def test_forbids_extra_keys_when_additional_properties_false(self):
    # Shape: { pet: { name: string } } with pet closed (additionalProperties: false)
    # Unknown fields on a closed named object are rejected.
    facade = _facade([
      _param(1, 'pet', 'pet', 'Hash', required=True, allows_additional=False),
      _param(2, 'name', 'pet.name', 'String', 1, required=True),
    ])

    matches, log = dict_matches(
      _context(facade),
      {'pet': {'name': 'Buddy', 'extra': 1}},
    )
    assert not matches
    assert 'Extra key' in log

  def test_matches_map_of_objects_with_named_fields(self):
    # Shape: { users: { [id: string]: { name: string, age?: integer } } }
    # Dynamic keys whose values are objects with fixed fields.
    facade = _facade([
      _param(1, 'users', 'users', 'Hash', required=True),
      _param(2, 'AdditionalProperty', 'users.*', 'Hash', 1),
      _param(3, 'name', 'users.*.name', 'String', 2, required=True),
      _param(4, 'age', 'users.*.age', 'Integer', 2),
    ])

    matches, log = dict_matches(
      _context(facade),
      {'users': {'u1': {'name': 'Ada', 'age': 36}, 'u2': {'name': 'Grace'}}},
    )
    assert matches, log

  def test_fails_when_named_field_under_additional_property_missing(self):
    # Shape: { users: { [id: string]: { name: string } } }
    # Required named field missing under a dynamic key.
    facade = _facade([
      _param(1, 'users', 'users', 'Hash', required=True),
      _param(2, 'AdditionalProperty', 'users.*', 'Hash', 1),
      _param(3, 'name', 'users.*.name', 'String', 2, required=True),
    ])

    matches, log = dict_matches(
      _context(facade),
      {'users': {'u1': {'age': 36}}},
    )
    assert not matches
    assert 'Missing key' in log

  def test_fails_when_named_field_under_additional_property_has_wrong_type(self):
    # Shape: { users: { [id: string]: { age: integer } } }
    # Named field present under a dynamic key, but wrong type.
    facade = _facade([
      _param(1, 'users', 'users', 'Hash', required=True),
      _param(2, 'AdditionalProperty', 'users.*', 'Hash', 1),
      _param(3, 'age', 'users.*.age', 'Integer', 2, required=True),
    ])

    matches, log = dict_matches(
      _context(facade),
      {'users': {'u1': {'age': '36'}}},
    )
    assert not matches
    assert 'type did not match' in log

  def test_matches_map_of_maps(self):
    # Shape: { [group: string]: { [name: string]: string[] } }
    # Two levels of dynamic keys; inner values are string arrays.
    facade = _facade([
      _param(1, 'AdditionalProperty', '*', 'Hash'),
      _param(2, 'AdditionalProperty', '*.*', 'Array', 1),
      _param(3, 'AdditionalPropertyElement', '*.*[*]', 'String', 2),
    ])

    matches, log = dict_matches(
      _context(facade),
      {'groupA': {'a': ['x'], 'b': []}, 'groupB': {'c': ['y', 'z']}},
    )
    assert matches, log

  def test_fails_when_nested_map_value_type_does_not_match(self):
    # Shape: { [group: string]: { [name: string]: string[] } }
    # Inner map value must be an array — a string fails.
    facade = _facade([
      _param(1, 'AdditionalProperty', '*', 'Hash'),
      _param(2, 'AdditionalProperty', '*.*', 'Array', 1),
      _param(3, 'AdditionalPropertyElement', '*.*[*]', 'String', 2),
    ])

    matches, log = dict_matches(
      _context(facade),
      {'groupA': {'a': 'not-an-array'}},
    )
    assert not matches
    assert 'type did not match' in log

  def test_matches_array_of_objects_with_additional_properties(self):
    # Shape: Array<{ [k: string]: integer }>
    # List elements are open maps of integers.
    facade = _facade([
      _param(1, 'Element', '[*]', 'Hash', required=True),
      _param(2, 'AdditionalProperty', '[*].*', 'Integer', 1),
    ])

    matches, log = list_matches(
      _context(facade),
      [{'a': 1, 'b': 2}, {'c': 3}],
    )
    assert matches, log

  def test_fails_array_element_additional_property_type(self):
    # Shape: Array<{ [k: string]: integer }>
    # Dynamic value under a list element has the wrong type.
    facade = _facade([
      _param(1, 'Element', '[*]', 'Hash', required=True),
      _param(2, 'AdditionalProperty', '[*].*', 'Integer', 1),
    ])

    matches, log = list_matches(
      _context(facade),
      [{'a': '1'}],
    )
    assert not matches
    assert 'type did not match' in log

  def test_matches_mixed_named_and_additional_properties(self):
    # Shape: { id: integer, [k: string]: string }
    # Required named field plus an open string map for everything else.
    facade = _facade([
      _param(1, 'id', 'id', 'Integer', required=True),
      _param(2, 'AdditionalProperty', '*', 'String'),
    ])

    matches, log = dict_matches(
      _context(facade),
      {'id': 7, 'label': 'ok', 'note': 'x'},
    )
    assert matches, log

  def test_named_property_takes_precedence_over_additional_properties(self):
    # Shape: { id: integer, [k: string]: string }
    # Named contract for `id` wins over the `*` string wildcard.
    facade = _facade([
      _param(1, 'id', 'id', 'Integer', required=True),
      _param(2, 'AdditionalProperty', '*', 'String'),
    ])

    matches, log = dict_matches(
      _context(facade),
      {'id': 7, 'label': 'ok'},
    )
    assert matches, log

    matches, log = dict_matches(
      _context(facade),
      {'id': '7', 'label': 'ok'},
    )
    assert not matches
    assert 'type did not match' in log

  def test_deeply_nested_wildcard_path(self):
    # Shape: { data: { meta: { [k: string]: { [k: string]: boolean } } } }
    # Named path down to a map-of-maps of booleans.
    facade = _facade([
      _param(1, 'data', 'data', 'Hash', required=True),
      _param(2, 'meta', 'data.meta', 'Hash', 1, required=True),
      _param(3, 'AdditionalProperty', 'data.meta.*', 'Hash', 2),
      _param(4, 'AdditionalProperty', 'data.meta.*.*', 'Boolean', 3),
    ])

    matches, log = dict_matches(
      _context(facade),
      {'data': {'meta': {'region': {'enabled': True, 'beta': False}}}},
    )
    assert matches, log

    matches, log = dict_matches(
      _context(facade),
      {'data': {'meta': {'region': {'enabled': 'yes'}}}},
    )
    assert not matches
    assert 'type did not match' in log

  def test_closed_object_under_additional_properties(self):
    # Shape: { [k: string]: { name: string } } with each value object closed
    # Dynamic keys whose values reject unknown fields.
    facade = _facade([
      _param(1, 'AdditionalProperty', '*', 'Hash', allows_additional=False),
      _param(2, 'name', '*.name', 'String', 1, required=True),
    ])

    matches, log = dict_matches(
      _context(facade),
      {'p1': {'name': 'Ada'}},
    )
    assert matches, log

    matches, log = dict_matches(
      _context(facade),
      {'p1': {'name': 'Ada', 'extra': True}},
    )
    assert not matches
    assert 'Extra key' in log
