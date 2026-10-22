from typing import List, Optional

import pytest
import yaml

from stoobly_agent.app.cli.helpers.openapi_endpoint_adapter import OpenApiEndpointAdapter

_STRING = {'type': 'string'}
_PET = {
  'type': 'object',
  'required': ['name'],
  'properties': {'name': _STRING, 'tags': {'type': 'array', 'items': _STRING}},
}


def _object(properties: dict, **kwargs) -> dict:
  return {'type': 'object', 'properties': properties, **kwargs}


def _body(schema: dict) -> dict:
  return {'requestBody': {'content': {'application/json': {'schema': schema}}}}


def _adapt(tmp_path, operation: Optional[dict] = None, servers: Optional[list] = None, security_schemes: Optional[dict] = None) -> List[dict]:
  spec = {
    'openapi': '3.0.0',
    'info': {'title': 'test', 'version': '1.0.0'},
    'paths': {'/pets': {'post': {'responses': {'200': {'description': 'ok'}}, **(operation or {})}}},
    'components': {'schemas': {'Pet': _PET}},
  }

  if servers:
    spec['servers'] = servers

  if security_schemes:
    spec['components']['securitySchemes'] = security_schemes

  spec_path = tmp_path / 'spec.yaml'
  spec_path.write_text(yaml.safe_dump(spec))

  return OpenApiEndpointAdapter().adapt_from_file(spec_path)


def _summarize(params: List[dict], parent_key: str, include_required=True) -> List[tuple]:
  summary = []
  for param in params:
    item = (param['id'], param['name'], param['query'], param[parent_key])
    summary.append(item + (param['is_required'],) if include_required else item)

  return summary


def _body_params(tmp_path, schema: dict) -> List[tuple]:
  endpoints = _adapt(tmp_path, _body(schema))
  return _summarize(endpoints[0]['body_param_names'], 'body_param_name_id')


@pytest.mark.openapi
class TestOpenApiEndpointAdapterSchemaWalking():
  def test_nested_object_params_reference_their_parent(self, tmp_path):
    params = _body_params(tmp_path, _object({'a': _STRING, 'b': _object({'c': _STRING})}))

    assert params == [
      (1, 'a', 'a', None, False),
      (2, 'b', 'b', None, False),
      (3, 'c', 'b.c', 2, False),
    ]

  def test_required_names_apply_to_the_properties_of_their_schema(self, tmp_path):
    schema = _object({'a': _STRING, 'b': _object({'c': _STRING}, required=['c'])}, required=['a'])

    params = _body_params(tmp_path, schema)

    assert params == [
      (1, 'a', 'a', None, True),
      (2, 'b', 'b', None, False),
      (3, 'c', 'b.c', 2, True),
    ]

  def test_root_array_params_are_queried_through_each_element(self, tmp_path):
    params = _body_params(tmp_path, {'type': 'array', 'items': {'$ref': '#/components/schemas/Pet'}})

    assert params == [
      (1, 'Element', '[*]', None, False),
      (2, 'name', '[*].name', 1, True),
      (3, 'tags', '[*].tags', 1, False),
      (4, 'tagsElement', '[*].tags[*]', 3, False),
    ]

  def test_array_of_arrays(self, tmp_path):
    schema = {'type': 'array', 'items': {'type': 'array', 'items': _object({'z': _STRING})}}

    params = _body_params(tmp_path, schema)

    assert params == [
      (1, 'Element', '[*]', None, False),
      (2, 'ElementElement', '[*][*]', 1, False),
      (3, 'z', '[*][*].z', 2, False),
    ]

  def test_root_all_of_merges_the_parts_into_one_level(self, tmp_path):
    schema = {'allOf': [{'$ref': '#/components/schemas/Pet'}, _object({'id': _STRING}, required=['id'])]}

    params = _body_params(tmp_path, schema)

    assert params == [
      (1, 'name', 'name', None, True),
      (2, 'tags', 'tags', None, False),
      (3, 'tagsElement', 'tags[*]', 2, False),
      (4, 'id', 'id', None, True),
    ]

  def test_nested_all_of_parts_are_children_of_the_declaring_property(self, tmp_path):
    schema = _object({
      'p': {'allOf': [{'$ref': '#/components/schemas/Pet'}, _object({'q': _STRING})]},
      'r': _STRING,
    })

    params = _body_params(tmp_path, schema)

    assert params == [
      (1, 'p', 'p', None, False),
      (2, 'name', 'p.name', 1, True),
      (3, 'tags', 'p.tags', 1, False),
      (4, 'tagsElement', 'p.tags[*]', 3, False),
      (5, 'q', 'p.q', 1, False),
      (6, 'r', 'r', None, False),
    ]

  # Documents current behavior: a schema with `items` but no `type: array` adds no param,
  # yet it still takes an id, so the ids that follow skip a number
  def test_schema_with_items_but_no_array_type_takes_an_id_without_adding_a_param(self, tmp_path):
    schema = _object({'a': {'items': _STRING}, 'b': _STRING, 'c': _object({'d': _STRING})})

    params = _body_params(tmp_path, schema)

    assert params == [
      (2, 'b', 'b', None, False),
      (3, 'c', 'c', None, False),
      (4, 'd', 'c.d', 3, False),
    ]

  def test_response_params_are_walked_like_body_params(self, tmp_path):
    operation = {'responses': {'200': {'description': 'ok', 'content': {'application/json': {
      'schema': _object({'a': _STRING, 'b': _object({'c': _STRING})}),
    }}}}}

    endpoints = _adapt(tmp_path, operation)

    params = _summarize(endpoints[0]['response_param_names'], 'response_param_name_id', include_required=False)
    assert params == [
      (1, 'a', 'a', None),
      (2, 'b', 'b', None),
      (3, 'c', 'b.c', 2),
    ]

  def test_query_params_share_ids_and_parents_across_params(self, tmp_path):
    operation = {'parameters': [
      {'name': 'q1', 'in': 'query', 'schema': _STRING},
      {'name': 'q2', 'in': 'query', 'schema': _object({'k': _STRING, 'l': _STRING})},
      {'name': 'q3', 'in': 'query', 'schema': {'type': 'array', 'items': _STRING}},
    ]}

    endpoints = _adapt(tmp_path, operation)

    params = _summarize(endpoints[0]['query_param_names'], 'query_param_name_id', include_required=False)
    assert params == [
      (1, 'q1', 'q1', None),
      (2, 'q2', 'q2', None),
      (3, 'k', 'q2.k', 2),
      (4, 'l', 'q2.l', 2),
      (5, 'q3', 'q3', None),
      (6, 'q3Element', 'q3[*]', 5),
    ]


@pytest.mark.openapi
class TestOpenApiEndpointAdapterServerVariables():
  def _hosts_and_paths(self, tmp_path, servers: list) -> List[tuple]:
    return [(endpoint['host'], endpoint['path']) for endpoint in _adapt(tmp_path, servers=servers)]

  def test_one_endpoint_per_combination_of_enum_values(self, tmp_path):
    servers = [{
      'url': 'https://{env}.example.com:{port}',
      'variables': {
        'env': {'default': 'dev', 'enum': ['dev', 'prod']},
        'port': {'default': '443', 'enum': ['443', '8443']},
      },
    }]

    endpoints = _adapt(tmp_path, servers=servers)

    assert [(endpoint['host'], endpoint['port']) for endpoint in endpoints] == [
      ('dev.example.com:443', '443'),
      ('dev.example.com:8443', '8443'),
      ('prod.example.com:443', '443'),
      ('prod.example.com:8443', '8443'),
    ]

  def test_default_is_used_when_there_is_no_enum(self, tmp_path):
    servers = [{'url': 'https://{env}.example.com', 'variables': {'env': {'default': 'dev'}}}]

    assert self._hosts_and_paths(tmp_path, servers) == [('dev.example.com', '/pets')]

  def test_variable_in_the_path(self, tmp_path):
    servers = [{'url': 'https://example.com/{version}', 'variables': {'version': {'default': 'v1', 'enum': ['v1', 'v2']}}}]

    assert self._hosts_and_paths(tmp_path, servers) == [('example.com', '/v1/pets'), ('example.com', '/v2/pets')]

  def test_repeated_variable_gets_the_same_value_everywhere(self, tmp_path):
    servers = [{'url': 'https://{a}.example.com/{a}', 'variables': {'a': {'default': 'x', 'enum': ['x', 'y']}}}]

    assert self._hosts_and_paths(tmp_path, servers) == [('x.example.com', '/x/pets'), ('y.example.com', '/y/pets')]

  def test_servers_with_and_without_variables(self, tmp_path):
    servers = [
      {'url': 'https://a.example.com'},
      {'url': 'http://{host}', 'variables': {'host': {'default': 'b.example.com'}}},
    ]

    endpoints = _adapt(tmp_path, servers=servers)

    assert [(endpoint['host'], endpoint['port']) for endpoint in endpoints] == [
      ('a.example.com', '443'),
      ('b.example.com', '80'),
    ]


@pytest.mark.openapi
class TestOpenApiEndpointAdapterOauth2Scopes():
  def _client_credentials(self, **kwargs) -> dict:
    return {'type': 'oauth2', 'flows': {'clientCredentials': {'tokenUrl': 'https://example.com/token', **kwargs}}}

  # Without default scopes the spec is invalid, so adapting would raise
  def test_scopes_are_added_to_the_first_oauth2_scheme_not_the_first_scheme(self, tmp_path):
    schemes = {
      'key': {'type': 'apiKey', 'in': 'header', 'name': 'X-Api-Key'},
      'oauth': self._client_credentials(),
    }

    assert len(_adapt(tmp_path, security_schemes=schemes)) == 1

  def test_existing_scopes_are_kept(self, tmp_path):
    schemes = {'oauth': self._client_credentials(scopes={'read': 'Read access'})}

    assert len(_adapt(tmp_path, security_schemes=schemes)) == 1

  def test_oauth2_without_a_client_credentials_flow(self, tmp_path):
    schemes = {'oauth': {'type': 'oauth2', 'flows': {'implicit': {'authorizationUrl': 'https://example.com/auth', 'scopes': {}}}}}

    assert len(_adapt(tmp_path, security_schemes=schemes)) == 1
