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


def _adapt(
  tmp_path, operation: Optional[dict] = None, servers: Optional[list] = None, security_schemes: Optional[dict] = None,
  path_parameters: Optional[list] = None,
) -> List[dict]:
  path_item = {'post': {'responses': {'200': {'description': 'ok'}}, **(operation or {})}}
  if path_parameters:
    path_item['parameters'] = path_parameters

  spec = {
    'openapi': '3.0.0',
    'info': {'title': 'test', 'version': '1.0.0'},
    'paths': {'/pets': path_item},
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

  def test_schema_with_items_but_no_array_type_is_walked_as_an_array(self, tmp_path):
    schema = _object({'a': {'items': _STRING}, 'b': _STRING})

    params = _body_params(tmp_path, schema)

    assert params == [
      (1, 'a', 'a', None, False),
      (2, 'aElement', 'a[*]', 1, False),
      (3, 'b', 'b', None, False),
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

  def test_additional_properties_schema_emits_wildcard_params(self, tmp_path):
    # Shape: { status: string, [k: string]: string[] }
    # Named field + open map of string arrays at the root.
    schema = _object(
      {'status': _STRING},
      additionalProperties={'type': 'array', 'items': _STRING},
    )
    params = _body_params(tmp_path, schema)

    assert params == [
      (1, 'status', 'status', None, False),
      (2, 'AdditionalProperty', '*', None, False),
      (3, 'AdditionalPropertyElement', '*[*]', 2, False),
    ]

  def test_additional_properties_only_object_emits_parent_and_wildcard(self, tmp_path):
    # Shape: { [k: string]: string }
    # Root object with no named properties — only a map of strings.
    schema = {
      'type': 'object',
      'additionalProperties': {'type': 'string'},
    }
    params = _body_params(tmp_path, schema)

    assert params == [
      (1, 'AdditionalProperty', '*', None, False),
    ]

  def test_nested_additional_properties_map_of_maps(self, tmp_path):
    # Shape: { [group: string]: { [name: string]: string[] } }
    # Two levels of dynamic keys; inner values are arrays.
    schema = {
      'type': 'object',
      'additionalProperties': {
        'type': 'object',
        'additionalProperties': {'type': 'array', 'items': _STRING},
      },
    }
    params = _body_params(tmp_path, schema)

    assert params == [
      (1, 'AdditionalProperty', '*', None, False),
      (2, 'AdditionalProperty', '*.*', 1, False),
      (3, 'AdditionalPropertyElement', '*.*[*]', 2, False),
    ]

  def test_additional_properties_object_with_named_fields(self, tmp_path):
    # Shape: { [id: string]: { name: string, tags?: string[] } }
    # Dynamic keys whose values are objects with fixed fields (name required).
    schema = {
      'type': 'object',
      'additionalProperties': _object({
        'name': _STRING,
        'tags': {'type': 'array', 'items': _STRING},
      }, required=['name']),
    }
    params = _body_params(tmp_path, schema)

    assert params == [
      (1, 'AdditionalProperty', '*', None, False),
      (2, 'name', '*.name', 1, True),
      (3, 'tags', '*.tags', 1, False),
      (4, 'tagsElement', '*.tags[*]', 3, False),
    ]

  def test_named_property_plus_nested_additional_properties(self, tmp_path):
    # Shape: { status?: string, message: { [breed: string]: string[] } }
    # Fixed sibling fields next to a nested open map (dogs.ceo-style).
    schema = _object({
      'status': _STRING,
      'message': {
        'type': 'object',
        'additionalProperties': {'type': 'array', 'items': _STRING},
      },
    }, required=['message'])
    params = _body_params(tmp_path, schema)

    # Property order follows OpenAPI/YAML serialization, not source dict insertion order.
    assert params == [
      (1, 'message', 'message', None, True),
      (2, 'AdditionalProperty', 'message.*', 1, False),
      (3, 'AdditionalPropertyElement', 'message.*[*]', 2, False),
      (4, 'status', 'status', None, False),
    ]

  def test_array_of_objects_with_additional_properties(self, tmp_path):
    # Shape: Array<{ [k: string]: integer }>
    # List elements are open maps of integers.
    schema = {
      'type': 'array',
      'items': {
        'type': 'object',
        'additionalProperties': {'type': 'integer'},
      },
    }
    params = _body_params(tmp_path, schema)

    assert params == [
      (1, 'Element', '[*]', None, False),
      (2, 'AdditionalProperty', '[*].*', 1, False),
    ]

  def test_array_of_objects_with_named_and_additional_properties(self, tmp_path):
    # Shape: Array<{ id: integer, [k: string]: string }>
    # List elements mix a required named field with an open string map.
    schema = {
      'type': 'array',
      'items': _object(
        {'id': {'type': 'integer'}},
        additionalProperties=_STRING,
        required=['id'],
      ),
    }
    params = _body_params(tmp_path, schema)

    assert params == [
      (1, 'Element', '[*]', None, False),
      (2, 'id', '[*].id', 1, True),
      (3, 'AdditionalProperty', '[*].*', 1, False),
    ]

  def test_deeply_nested_additional_properties_under_named_path(self, tmp_path):
    # Shape: { data: { meta: { [k: string]: { [k: string]: boolean } } } }
    # Named path down to a map-of-maps of booleans.
    schema = _object({
      'data': _object({
        'meta': {
          'type': 'object',
          'additionalProperties': {
            'type': 'object',
            'additionalProperties': {'type': 'boolean'},
          },
        },
      }),
    })
    params = _body_params(tmp_path, schema)

    assert params == [
      (1, 'data', 'data', None, False),
      (2, 'meta', 'data.meta', 1, False),
      (3, 'AdditionalProperty', 'data.meta.*', 2, False),
      (4, 'AdditionalProperty', 'data.meta.*.*', 3, False),
    ]

  def test_response_additional_properties_are_walked(self, tmp_path):
    # Shape (response): { results: { [k: string]: { score: number } } }
    # Same map-of-objects pattern, adapted from a 200 response schema.
    operation = {'responses': {'200': {'description': 'ok', 'content': {'application/json': {
      'schema': _object({
        'results': {
          'type': 'object',
          'additionalProperties': _object({'score': {'type': 'number'}}, required=['score']),
        },
      }),
    }}}}}
    endpoints = _adapt(tmp_path, operation)
    params = _summarize(endpoints[0]['response_param_names'], 'response_param_name_id')

    assert params == [
      (1, 'results', 'results', None, False),
      (2, 'AdditionalProperty', 'results.*', 1, False),
      (3, 'score', 'results.*.score', 2, True),
    ]

  def test_explicit_scalar_type_wins_over_leftover_items(self, tmp_path):
    # Shape: { message: { [k: string]: string } }
    # Invalid-but-common edit: type is string while leftover `items` remains; scalar wins.
    schema = _object({
      'message': {
        'type': 'object',
        'additionalProperties': {'type': 'string', 'items': {'type': 'string'}},
      },
    })
    params = _body_params(tmp_path, schema)

    assert params == [
      (1, 'message', 'message', None, False),
      (2, 'AdditionalProperty', 'message.*', 1, False),
    ]
    assert next(p for p in _adapt(tmp_path, _body(schema))[0]['body_param_names'] if p['query'] == 'message.*')['inferred_type'] == 'String'

  def test_additional_properties_false_marks_object_closed(self, tmp_path):
    # Shape: { name?: string } with additionalProperties: false
    # Closed object — extras forbidden. Root anonymous schemas have no parent to mark;
    # a named nested object (pet) carries allows_additional_properties=False.
    schema = _object({'name': _STRING}, additionalProperties=False)
    endpoints = _adapt(tmp_path, _body(schema))
    params = endpoints[0]['body_param_names']

    assert [(p['name'], p['query'], p.get('allows_additional_properties')) for p in params] == [
      ('name', 'name', None),
    ]
    nested = _object({'pet': _object({'name': _STRING}, additionalProperties=False)})
    nested_params = _adapt(tmp_path, _body(nested))[0]['body_param_names']
    pet = next(p for p in nested_params if p['query'] == 'pet')
    assert pet.get('allows_additional_properties') is False

  def test_nested_closed_object_under_additional_properties(self, tmp_path):
    # Shape: { [k: string]: { name: string } } where each value object is closed
    # Dynamic keys whose values reject unknown fields.
    schema = {
      'type': 'object',
      'additionalProperties': _object({'name': _STRING}, additionalProperties=False, required=['name']),
    }
    params = _adapt(tmp_path, _body(schema))[0]['body_param_names']

    assert [(p['query'], p['inferred_type'], p.get('allows_additional_properties'), p['is_required']) for p in params] == [
      ('*', 'Hash', False, False),
      ('*.name', 'String', None, True),
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

  def test_required_query_params_are_marked_required(self, tmp_path):
    operation = {'parameters': [
      {'name': 'q1', 'in': 'query', 'required': True, 'schema': _STRING},
      {'name': 'q2', 'in': 'query', 'schema': _STRING},
      {'name': 'q3', 'in': 'query', 'required': True, 'schema': _object({'k': _STRING})},
    ]}

    endpoints = _adapt(tmp_path, operation)

    params = _summarize(endpoints[0]['query_param_names'], 'query_param_name_id')
    assert params == [
      (1, 'q1', 'q1', None, True),
      (2, 'q2', 'q2', None, False),
      (3, 'q3', 'q3', None, True),
      (4, 'k', 'q3.k', 3, False),
    ]

  def test_required_query_param_name_does_not_mark_a_nested_property_required(self, tmp_path):
    operation = {'parameters': [
      {'name': 'name', 'in': 'query', 'required': True, 'schema': _STRING},
      {'name': 'filter', 'in': 'query', 'schema': _object({'name': _STRING})},
    ]}

    endpoints = _adapt(tmp_path, operation)

    params = _summarize(endpoints[0]['query_param_names'], 'query_param_name_id')
    assert params == [
      (1, 'name', 'name', None, True),
      (2, 'filter', 'filter', None, False),
      (3, 'name', 'filter.name', 2, False),
    ]


@pytest.mark.openapi
class TestOpenApiEndpointAdapterPathLevelParameters():
  def test_query_params_and_headers_declared_on_the_path_item_apply_to_its_operations(self, tmp_path):
    path_parameters = [
      {'name': 'shared', 'in': 'query', 'required': True, 'schema': _STRING},
      {'name': 'X-Shared', 'in': 'header', 'schema': _STRING},
    ]

    endpoints = _adapt(tmp_path, path_parameters=path_parameters)

    assert [param['name'] for param in endpoints[0]['query_param_names']] == ['shared']
    assert [header['name'] for header in endpoints[0]['header_names']] == ['X-Shared']

  def test_operation_parameter_overrides_path_item_parameter_with_the_same_name_and_location(self, tmp_path):
    path_parameters = [
      {'name': 'q', 'in': 'query', 'schema': _STRING},
      {'name': 'other', 'in': 'query', 'schema': _STRING},
    ]
    operation = {'parameters': [{'name': 'q', 'in': 'query', 'required': True, 'schema': _STRING}]}

    endpoints = _adapt(tmp_path, operation, path_parameters=path_parameters)

    params = _summarize(endpoints[0]['query_param_names'], 'query_param_name_id')
    assert params == [
      (1, 'other', 'other', None, False),
      (2, 'q', 'q', None, True),
    ]


@pytest.mark.openapi
class TestOpenApiEndpointAdapterResponseHeaders():
  def test_response_header_is_required_only_when_declared_required(self, tmp_path):
    operation = {'responses': {'200': {'description': 'ok', 'headers': {
      'X-Required': {'required': True, 'schema': _STRING},
      'X-Optional': {'schema': _STRING},
    }}}}

    endpoints = _adapt(tmp_path, operation)

    headers = {header['name']: header['is_required'] for header in endpoints[0]['response_header_names']}
    assert headers == {'X-Required': True, 'X-Optional': False}


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
