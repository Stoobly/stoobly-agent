import pytest

from stoobly_agent.app.cli.helpers.schema_builder import SchemaBuilder

@pytest.mark.openapi
class TestSchemaBuilder():

  def test_it_builds_single_level_dict(self):
    builder = SchemaBuilder(-1, 'query_param_name')
    param_names = builder.build([
      {'name': 'id', 'value': 0, 'query': 'id', 'required': False, 'id': 1, "parent_id": None},
      {'name': 'name', 'value': '', 'query': 'name', 'required': False, 'id': 2, "parent_id": None}
    ])

    param_names_index = self.__index(param_names)
    expected_queries = ['id.Integer', 'name.String']

    for query in expected_queries:
      assert param_names_index.get(query), query

  def test_it_builds_two_level_dict(self):
    builder = SchemaBuilder(-1, 'query_param_name')
    param_names = builder.build([
      {'name': 'list', 'value': [], 'query': 'list', 'required': False, 'id': 1, "parent_id": None},
      {'name': 'ListElement', 'value': {}, 'query': 'list[*]', 'required': False, 'id': 2, "parent_id": 1},
      {'name': 'id', 'value': 0, 'query': 'list[*].id', 'required': False, 'id': 3, "parent_id": 2},
      {'name': 'name', 'value': '', 'query': 'list[*].name', 'required': False, 'id': 4, "parent_id": 2},
      {'name': 'total', 'value': 0, 'query': 'total', 'required': False, 'id': 5, "parent_id": None}
    ])

    param_names_index = self.__index(param_names)
    expected_queries = [
      'list.Array', 'list[*].Hash', 'list[*].id.Integer', 'list[*].name.String', 'total.Integer'
    ]

    for query in expected_queries:
      assert param_names_index.get(query), query

  def test_it_builds_single_level_array(self):
    builder = SchemaBuilder(-1, 'body_param_name')
    param_names = builder.build([
      {'name': 'Element', 'value': 0, 'query': '[*]', 'required': False, 'id': 1, "parent_id": None},
    ])

    param_names_index = self.__index(param_names)
    expected_queries = [
      '[*].Integer'
    ]

    for query in expected_queries:
      assert param_names_index.get(query), query

  def test_it_builds_item_and_single_level_array(self):
    builder = SchemaBuilder(-1, 'query_param_name')
    param_names = builder.build([
      {'name': 'tags', 'value': [], 'query': 'tags', 'required': False, 'id': 1, "parent_id": None},
      {'name': 'TagsElement', 'value': '', 'query': 'tags[*]', 'required': False, 'id': 2, "parent_id": 1},
      {'name': 'limit', 'value': 0, 'query': 'limit', 'required': False, 'id': 3, "parent_id": None}
    ])

    param_names_index = self.__index(param_names)
    expected_queries = [
      'tags.Array', 'tags[*].String', 'limit.Integer' 
    ]

    for query in expected_queries:
      assert param_names_index.get(query), query

  def __index(self, param_names):
    param_names_index = {}
    for param_name in param_names:
      param_names_index[f"{param_name['query']}.{param_name['inferred_type']}"] = param_name
    return param_names_index
