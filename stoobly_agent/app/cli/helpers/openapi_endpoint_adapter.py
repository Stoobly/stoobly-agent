import hashlib
import itertools
import logging
import re
import yaml

from functools import reduce
from jsonschema_path import SchemaPath
from typing import Callable, Dict, List, Tuple, Union
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

from stoobly_agent.lib.api.interfaces.endpoints import (
  Alias,
  OpenApiEndpointShowResponse,
  RequestComponentName,
)
from stoobly_agent.lib.utils.python_to_ruby_type import convert_reverse

from .schema_builder import SchemaBuilder


HTTP_METHODS = ["get", "put", "post", "delete", "options", "head", "patch", "trace"]

_DEFAULT_PORTS = {'https': '443', 'http': '80'}

# Name given to the schema object at the root of a body/response, or to an `allOf` part.
# It is not a real property, so it never produces a param of its own.
_ANONYMOUS = 'tmp'

# https://swagger.io/docs/specification/data-models/data-types/
_OPENAPI_DEFAULT_TYPES = {
  'string': str,
  'number': float,
  'integer': int,
  'boolean': bool,
  'array': list,
  'object': dict,
}


def _md5_hex(value: str) -> str:
  return hashlib.md5(value.encode('utf-8')).hexdigest()


def _read_value(value):
  return value.read_value() if hasattr(value, 'read_value') else value


def _resolve_port(parsed_url) -> str:
  if parsed_url.port is None:
    return _DEFAULT_PORTS.get(parsed_url.scheme, '-')
  return str(parsed_url.port)


def _first_oauth2_scheme(file_data: Dict):
  if 'components' not in file_data:
    return None
  components = file_data['components']

  if 'securitySchemes' not in components:
    return None

  for scheme in components['securitySchemes'].values():
    if scheme.get('type') == 'oauth2':
      return scheme

  return None


def _server_variable_values(variable) -> list:
  enum_list = variable.get('enum')
  if enum_list:
    return _read_value(enum_list)

  return [_read_value(variable.get('default'))]


def _substitute_variables(split_url: List[str], values: Dict[str, str]) -> str:
  return ''.join(values.get(part, part) for part in split_url)


# OpenAPI uses ~1 to escape '/' and ~0 to escape '~' in JSON pointers (RFC 6901)
def _unescape_json_pointer_token(token: str) -> str:
  return token.replace('~1', '/').replace('~0', '~')


def _split_path_pattern(path: str) -> Tuple[str, List[str]]:
  """
  Returns the match pattern and the segment names of ``path``, e.g.
  '/pets/{id}' -> ('/pets/%', ['', 'pets', ':id'])
  """
  pattern_parts = []
  segment_names = []

  for part in path.split('/'):
    if part.startswith('{') and part.endswith('}'):
      pattern_parts.append('%')
      segment_names.append(f":{part[1:-1]}")
    else:
      pattern_parts.append(part)
      segment_names.append(part)

  return '/'.join(pattern_parts), segment_names


def compute_openapi_service_id(hostname: str, port: str) -> str:
  """MD5 hex of ``{hostname}:{port}`` (hostname lowercased). Used by tests and callers."""
  hn = (hostname or "").lower()
  return _md5_hex(f"{hn}:{port}")


def compute_openapi_endpoint_id(service_id: str, match_pattern: str, method: str) -> str:
  """
  MD5 hex of ``service_id``, ``match_pattern``, and HTTP ``method`` (concatenated).

  ``method`` is included so operations that share the same ``match_pattern`` (e.g. GET vs POST)
  do not receive the same ``id``.
  """
  return _md5_hex(f"{service_id}{match_pattern or ''}{method}")


def _default_python_value(open_api_type: str):
  # Instantiate per call so mutable defaults (list, dict) are never shared
  return _OPENAPI_DEFAULT_TYPES.get(open_api_type, dict)()


# Generates the entire query string for a property
# Ex: Pets[*].name for property 'name' of a 'Pet' element in the 'Pets' array
def _build_query(prefix: str, name: str) -> str:
  if name == _ANONYMOUS:
    return prefix
  if name.endswith('Element'):
    return f"{prefix}[*]"
  if prefix == '':
    return name
  return f"{prefix}.{name}"


def _make_param(name: str, value_key: str, value, required: bool, query: str, param_id: int, parent_id: int) -> dict:
  return {'name': name, value_key: value, 'required': required, 'query': query, 'id': param_id, 'parent_id': parent_id}


class _SchemaParamWalker():
  """
  Flattens an OpenAPI schema into a list of literal params (``params``), one per named property.
  Params are listed parent first and get consecutive ids in that order.

  ``required`` collects the property names that parent schemas marked as required. It is shared by
  every schema walked with the same walker, and a name is removed once a property consumes it.
  """

  def __init__(self, dereference: Callable):
    self.params: List[dict] = []
    self.required: List[str] = []
    self._dereference = dereference
    self._last_id = 0

  # Ids continue after the params collected so far, e.g. when walking several query params in a row
  def walk_root(self, name: str, schema):
    self._last_id = len(self.params)
    self.walk(name, schema)

  # `name` is the name of the schema object, i.e. the name of the body_param_name or response_param_name component
  # An anonymous schema (the root of a body/response, or an allOf part) adds no param of its own
  def walk(self, name: str, schema, parent_id=None, query_prefix='', override_required=False):
    schema = self._dereference(schema)
    anonymous = name == _ANONYMOUS
    query = _build_query(query_prefix, name)

    node_id = None if anonymous else self.__claim_id()
    # The anonymous schema's children belong to the closest named ancestor
    # Ex: the properties of every allOf part are children of the schema declaring the allOf
    children_parent_id = parent_id if anonymous else node_id

    # A schema is traversable if it has one more non-empty nested schema objects
    traversable = schema.get('properties') or schema.get('items') or schema.get('allOf')

    if not traversable:
      self.__visit_leaf(name, schema, node_id, parent_id, query, override_required)
    elif 'properties' in schema.keys():
      self.__visit_object(name, schema, node_id, parent_id, query, override_required, children_parent_id)
    elif schema.get('type') == 'array':
      self.__visit_array(name, schema, node_id, parent_id, query, override_required)
    elif 'allOf' in schema.keys():
      self.__visit_all_of(name, schema, node_id, parent_id, query, override_required, children_parent_id)

  # Every named schema takes an id, even if it ends up adding no param
  def __claim_id(self) -> int:
    self._last_id += 1
    return self._last_id

  def __add_required(self, required):
    if required is None:
      return

    names = _read_value(required)
    if isinstance(names, list):
      self.required.extend(names)

  # Ex: {'name': {'type': 'string', 'description': 'Name of pet', 'Example': 'Buddy'}}
  def __visit_leaf(self, name, schema, node_id, parent_id, query, override_required):
    if name == _ANONYMOUS:
      return

    default_value = _default_python_value(schema.get('type', 'object'))
    required = override_required or bool(schema.get('required', False))
    self.params.append(_make_param(name, 'values', [default_value], required, query, node_id, parent_id))

  # Ex: {'tmp': {'type': 'object', 'required': ['name'], 'properties': {'name': {'type': 'string'}, 'tag': {'type': 'string'}}}}
  def __visit_object(self, name, schema, node_id, parent_id, query, override_required, children_parent_id):
    self.__add_required(schema.get('required'))

    if name != _ANONYMOUS:
      required = override_required or bool(schema.get('schema_required', False))
      self.params.append(_make_param(name, 'value', {}, required, query, node_id, parent_id))

    for property_key, property_value in schema.get('properties').items():
      is_required = property_key in self.required
      if is_required:
        self.required.remove(property_key)
      self.walk(property_key, property_value, children_parent_id, query, is_required)

  # Ex: {'tmp': {'type': 'array', 'items': {'$ref': '#/components/schemas/NewPet'}}}
  def __visit_array(self, name, schema, node_id, parent_id, query, override_required):
    if name == _ANONYMOUS:
      self.walk('Element', schema['items'], parent_id, query)
      return

    required = override_required or bool(schema.get('required', False))
    self.params.append(_make_param(name, 'value', [], required, query, node_id, parent_id))
    self.walk(f"{name}Element", schema['items'], node_id, query)

  # Ex: {'Element': {'type': 'object', 'allOf': [{'$ref': '#/components/schemas/NewPet'}, {'type': 'object', 'required': ['id'], 'properties': {'id': {'type': 'integer', 'format': 'int64'}}}]}}
  def __visit_all_of(self, name, schema, node_id, parent_id, query, override_required, children_parent_id):
    if name != _ANONYMOUS:
      required = override_required or bool(schema.get('self_required', False))
      self.params.append(_make_param(name, 'value', {}, required, query, node_id, parent_id))

    for part in schema.get('allOf'):
      self.__add_required(part.get('required'))
      self.walk(_ANONYMOUS, part, children_parent_id, query)


class OpenApiEndpointAdapter():
  def __init__(self, strict_refs=False):
    """
    Initialize the OpenAPI Endpoint Adapter.
    
    Args:
      strict_refs: If True, raise errors for unsupported references.
                   If False, log warnings and return placeholder objects.
    """
    self.spec = None
    self.components = None
    self.strict_refs = strict_refs

  def adapt_from_file(self, file_path) -> List[OpenApiEndpointShowResponse]:
    from openapi_core import OpenAPI

    spec = {}

    with open(file_path, "r") as stream:
      file_data: Dict = yaml.safe_load(stream)

      if not file_data:
        return []

      if 'info' not in file_data:
        self.__add_info(file_data)

      self.__ensure_oauth2_scopes(file_data)

      openApi = OpenAPI.from_dict(file_data)
      spec = openApi.spec

    return self.adapt(spec)

  def adapt(self, spec: SchemaPath) -> List[OpenApiEndpointShowResponse]:
    self.spec = spec  # Store spec for use in __dereference
    self.components = spec.get("components", {})
    paths = spec['paths']
    endpoints = []

    for server in self.__evaluate_servers(spec.get("servers")):
      parsed_url = urlparse(server["url"])

      for path_name, path in paths.items():
        for http_method in HTTP_METHODS:
          if http_method not in path:
            continue

          endpoints.append(self.__build_endpoint(parsed_url, path_name, http_method, path[http_method]))

    return endpoints

  def __build_endpoint(self, parsed_url, path_name: str, http_method: str, operation) -> OpenApiEndpointShowResponse:
    endpoint: OpenApiEndpointShowResponse = {}
    endpoint['method'] = http_method.upper()

    self.__apply_location(endpoint, parsed_url, path_name)
    self.__apply_parameters(endpoint, operation)

    # TODO: nested servers

    self.__apply_request_body(endpoint, operation)

    # Responses -> construct lists of response header and response param name resources
    self.__parse_responses(endpoint, operation.get('responses', {}))

    return endpoint

  # Sets everything derived from the server url and path: host, port, path, ids
  def __apply_location(self, endpoint: OpenApiEndpointShowResponse, parsed_url, path_name: str):
    endpoint['host'] = '-' if parsed_url.netloc == '' else parsed_url.netloc

    joined_path = self.__urljoin(parsed_url.path, path_name)
    match_pattern, segment_names = _split_path_pattern(joined_path)
    endpoint['match_pattern'] = match_pattern
    endpoint['path'] = joined_path

    endpoint['path_segment_names'] = [
      {'name': name, 'type': 'alias' if name.startswith(':') else 'static'}
      for name in segment_names if name != ''
    ]

    endpoint['port'] = _resolve_port(parsed_url)
    endpoint['service_id'] = compute_openapi_service_id(parsed_url.hostname, endpoint['port'])
    endpoint['id'] = compute_openapi_endpoint_id(endpoint['service_id'], endpoint['match_pattern'], endpoint['method'])

  def __apply_parameters(self, endpoint: OpenApiEndpointShowResponse, operation):
    query_parameters = []

    for parameter in operation.get("parameters", {}):
      parameter = self.__deref(parameter)

      if parameter['in'] == 'query':
        query_parameters.append(parameter)
      elif parameter['in'] == 'header':
        self.__add_header_param(endpoint, parameter)
      elif parameter['in'] == 'path':
        self.__add_path_alias(endpoint, parameter)

    self.__add_query_params(endpoint, query_parameters)

  # All query params of an endpoint are extracted together so their ids and required names are shared
  def __add_query_params(self, endpoint: OpenApiEndpointShowResponse, parameters: list):
    if not parameters:
      return

    walker = _SchemaParamWalker(self.__deref)
    endpoint['query_param_names'] = []

    for parameter in parameters:
      if parameter.get('required'):
        walker.required.append(parameter['name'])

      walker.walk_root(parameter['name'], parameter.get('schema', {}))

    self.__convert_literal_component_param(endpoint, walker.params, 'query_param_name')

  def __add_header_param(self, endpoint: OpenApiEndpointShowResponse, parameter):
    header_names = endpoint.setdefault('header_names', [])

    header: RequestComponentName = {}
    header['name'] = parameter['name']
    header['values'] = self.__extract_examples(parameter)
    header['is_required'] = bool(parameter.get('required'))
    header['is_deterministic'] = True
    header['id'] = len(header_names) + 1

    header_names.append(header)

  def __add_path_alias(self, endpoint: OpenApiEndpointShowResponse, parameter):
    aliases = endpoint.setdefault('aliases', [])

    if any(parameter['name'] == alias['name'] for alias in aliases):
      return

    alias: Alias = {}
    alias['id'] = len(aliases) + 1
    alias['name'] = '{' + parameter['name'] + '}'

    aliases.append(alias)

  def __apply_request_body(self, endpoint: OpenApiEndpointShowResponse, operation):
    request_body = operation.get("requestBody", {})
    literal_params = self.__extract_content_params(request_body.get("content", {}))
    self.__convert_literal_component_param(endpoint, literal_params, 'body_param_name')

  # Returns the literal params of the first media type's schema
  def __extract_content_params(self, content) -> list:
    walker = _SchemaParamWalker(self.__deref)

    # Only support first media type
    for _, media_type in content.items():
      schema = media_type.get('schema')
      if schema:
        walker.walk_root(_ANONYMOUS, schema)
      break

    return walker.params

  def __add_info(self, file_data: Dict):
    file_data['info'] = {
      'version': '0.0.1',
      'title': ''
    }

  # The clientCredentials flow requires scopes, so default them to empty when missing
  def __ensure_oauth2_scopes(self, file_data: Dict):
    oauth2_scheme = _first_oauth2_scheme(file_data)
    if not oauth2_scheme:
      return

    flows = oauth2_scheme.get('flows')
    client_credentials = flows.get('clientCredentials') if flows else None

    if client_credentials and client_credentials.get('scopes') is None:
      client_credentials['scopes'] = {}

  def __get_most_recent_param(self, literal_params: dict):
    return list(literal_params)[-1] if literal_params else None

  def __get_second_most_recent_param(self, literal_params: dict):
    if not literal_params or len(literal_params) < 2:
      return None

    return list(literal_params)[-2]

  # Returns the node's referenced schema, if it is a $ref
  def __deref(self, node):
    if '$ref' in node.keys():
      return self.__dereference(self.components, node.get('$ref'), self.spec)

    return node

  # Returns the schema object located at the given reference path
  def __dereference(self, components: SchemaPath, reference: str, spec: SchemaPath = None):
    # '#/components/schemas/NewPet' or '#/paths/~1users~1{id}/get/responses/200'
    if not reference.startswith('#'):
      return self.__resolve_external(reference)

    if reference.startswith('#/components'):
      return self.__resolve_component(components, reference, spec)

    return self.__resolve_json_pointer(components, reference, spec)

  # External reference (e.g., 'external-file.yaml#/components/schemas/Pet')
  def __resolve_external(self, reference: str):
    if self.strict_refs:
      raise ValueError(f'External references are not supported yet: {reference}')

    # Log warning and return a placeholder object
    logger.warning(f'External reference "{reference}" cannot be resolved. Using placeholder object.')
    # Return a generic object schema as fallback
    return {
      'type': 'object',
      'description': f'External reference: {reference}',
      'x-external-ref': reference
    }

  # Component reference: #/components/schemas/Pet
  def __resolve_component(self, components: SchemaPath, reference: str, spec: SchemaPath = None):
    ref_split = reference.split('#/components/')
    component_data = ref_split[1].split('/')
    component_type = component_data[0]
    component_name = component_data[1]
    component = components.get(component_type, {})

    # Example: {'type': 'object', 'required': ['name'], 'properties': {'name': {'type': 'string'}, 'tag': {'type': 'string'}}}
    body_spec = component.get(component_name)
    if body_spec is None:
      raise ValueError(f'Component "{component_name}" not found in "{component_type}"')

    if '$ref' in body_spec.keys():
      body_spec = self.__dereference(components, body_spec.get('$ref'), spec)

    return body_spec

  # Non-component reference: #/paths/~1users/get/parameters/0
  def __resolve_json_pointer(self, components: SchemaPath, reference: str, spec: SchemaPath = None):
    if spec is None:
      raise ValueError(f'Non-component reference requires spec parameter: {reference}')

    # Split path by '/' and navigate through spec
    path_parts = reference[1:].split('/')[1:]  # Skip empty string from leading '/'

    current = spec
    for i, part in enumerate(path_parts):
      unescaped_part = _unescape_json_pointer_token(part)

      # Try to navigate
      if hasattr(current, 'get'):
        # SchemaPath objects use .get() method
        current = current.get(unescaped_part)
      elif hasattr(current, '__getitem__'):
        try:
          # Try as integer index for arrays
          if unescaped_part.isdigit():
            current = current[int(unescaped_part)]
          else:
            current = current[unescaped_part]
        except (KeyError, IndexError, TypeError):
          raise ValueError(f'Could not resolve reference path "{reference}" at "{unescaped_part}"')
      else:
        raise ValueError(f'Could not navigate reference "{reference}" at "{unescaped_part}"')
      
      # Check if resolution failed
      if current is None:
        # Provide better error message
        resolved_path = '/'.join(path_parts[:i+1])
        raise ValueError(f'Could not resolve reference path "{reference}" - path "{resolved_path}" not found')
    
    # If the resolved value itself has a $ref, recursively resolve it
    if isinstance(current, dict) and '$ref' in current:
      current = self.__dereference(components, current['$ref'], spec)
    
    return current 
  
  def __convert_literal_component_param(self, endpoint: OpenApiEndpointShowResponse,
      literal_component_params: Union[dict, list], component_name: str) -> None:

    if not literal_component_params:
      return

    builder = SchemaBuilder(endpoint['id'], component_name)
    built_params = builder.build(literal_component_params)

    built_params_list = list(built_params)
    for param in built_params_list:
      if param.get('is_required', False):
        inferred_type = param['inferred_type']
        default_python_type = convert_reverse(inferred_type)

        if not param.get('values'):
          param['values'] = []
        param['values'].append(default_python_type)
      else:
        param['is_required'] = False

    if not endpoint.get(component_name + 's'):
      endpoint[component_name + 's'] = built_params_list
    else:
      endpoint[component_name + 's'].extend(built_params_list)

  # urllib.parse.urljoin() doesn't work for some of our edge cases
  # and results in missing path components so use the custom __urljoin
  # https://stackoverflow.com/a/58037371
  def __join_slash(self, a: str, b: str):
    return a.rstrip('/') + '/' + b.lstrip('/')

  def __urljoin(self, *args: str):
    return reduce(self.__join_slash, args) if args else ''

  def __to_simple_dict(self, complex_dict):
    simple_dict = {}
    for key, val in complex_dict.items():
      simple_dict[key] = val['value']

    return simple_dict

  def __build_url(self, host, scheme, port, path, query):
    s = host
    if scheme and len(scheme) > 0:
      s = f"{scheme}://{s}"

    if port != None:
      if not ((scheme == 'https' and port == 443) or (scheme == 'http' and port == 80)):
        s = f"{s}:{port}"

    s += path

    _query = query
    if _query and len(_query) > 0:
      s = f"{s}?{_query}"

    return s

  # https://swagger.io/docs/specification/data-models/data-types/
  def __convert_open_api_type(self, open_api_type: str) -> str:
    type_map = {
      'string': str(str),
      'number': str(float),
      'integer': str(int),
      'boolean': str(bool),
      'array': str(list),
      'object': str(dict)
    }
    return type_map.get(open_api_type, str(dict))

  def __open_api_to_default_python_type(self, open_api_type: str):
    return _default_python_value(open_api_type)

  def __num_variables(self, url: str) -> int:
    num = url.count('{')
    return num

  def __evaluate_servers(self, servers: SchemaPath) -> List[dict]:
    if not servers:
      return [{'url': '/'}]

    result = []

    for server in servers:
      original_url = server["url"]

      variables = server.get("variables", {})
      if not variables:
        result.append({'url': original_url})
        continue

      # Splitting on the braces leaves the variable names at the odd positions
      split_url = re.split('{|}', original_url)
      var_to_possible_vals = {
        part: _server_variable_values(variables[part]) for part in split_url if part in variables.keys()
      }

      # One url per combination of the variables' possible values
      for permutation in itertools.product(*var_to_possible_vals.values()):
        values = dict(zip(var_to_possible_vals.keys(), permutation))
        result.append({'url': _substitute_variables(split_url, values)})
    
    return result

  def __parse_responses(self, endpoint: OpenApiEndpointShowResponse, responses: SchemaPath):
    for response_code, response_definition in responses.items():
      # Only support status code 200 for now
      if response_code != '200':
        continue

      # Construct response param name components
      literal_params = self.__extract_content_params(response_definition.get('content', {}))
      self.__convert_literal_component_param(endpoint, literal_params, 'response_param_name')

      # Construct response header name components
      response_headers = response_definition.get('headers', {})
      for header_name, header_definition in response_headers.items():
        endpoint.setdefault('response_header_names', []).append(
          self.__build_response_header(header_name, header_definition)
        )

  def __build_response_header(self, header_name: str, header_definition) -> RequestComponentName:
    response_header_name: RequestComponentName = {}
    response_header_name['name'] = header_name

    header_definition = self.__deref(header_definition)

    response_header_name['is_required'] = header_definition.get('is_required', False)
    response_header_name['is_deterministic'] = True
    response_header_name['values'] = self.__extract_examples(header_definition)

    return response_header_name

  def __extract_examples(self, definition: dict):
    values = []

    if 'example' in definition:
      values = [definition['example']]

    examples = definition.get('examples', {})
    if examples:
      for example in examples.values():
        if 'value' in example:
          values.append(example['value'])

    return values