import pdb
import pytest

from stoobly_agent.app.cli.helpers.schema_builder import SchemaBuilder

class TestSchemaBuilder():

  def test_it_builds_single_level_dict(self):
    builder = SchemaBuilder(-1, 'query_param_name')
    param_names = builder.build({ 'id': 1, 'name': 'test' })

    param_names_index = self.__index(param_names)
    expected_queries = ['id.Integer', 'name.String']

    for query in expected_queries:
      assert param_names_index.get(query), query

  def test_it_builds_two_level_dict(self):
    builder = SchemaBuilder(-1, 'query_param_name')
    param_names = builder.build({ 'list': [{ 'id': 1, 'name': 'test' }], 'total': 1 })

    param_names_index = self.__index(param_names)
    expected_queries = [
      'list.Array', 'total.Integer', 'list[*].id.Integer', 'list[*].name.String'
    ]

    for query in expected_queries:
      assert param_names_index.get(query), query

  def test_it_builds_single_level_array(self):
    builder = SchemaBuilder(-1, 'body_param_name')
    param_names = builder.build([1, 'a'])

    param_names_index = self.__index(param_names)
    expected_queries = [
      '[*].Integer', '[*].String'
    ]

    for query in expected_queries:
      assert param_names_index.get(query), query

  def test_it_builds_item_and_single_level_array(self):
    builder = SchemaBuilder(-1, 'query_param_name')
    param_names = builder.build({ 'tags': [''], 'limit': 0 })

    param_names_index = self.__index(param_names)
    expected_queries = [
      'limit.Integer', 'tags.Array', 'tags[*].String' 
    ]

    for query in expected_queries:
      assert param_names_index.get(query), query

  def __index(self, param_names):
    param_names_index = {}
    for param_name in param_names:
      param_names_index[f"{param_name['query']}.{param_name['inferred_type']}"] = param_name
    return param_names_index
