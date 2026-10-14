import copy
import hashlib
import itertools
import logging
import re
import yaml

from functools import reduce
from jsonschema_path import SchemaPath
from typing import Dict, List, Tuple, Union
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

      missing_oauth2_scopes = self.__is_missing_oauth2_scopes(file_data)
      if missing_oauth2_scopes:
        self.__add_oauth2_default_scopes(file_data)

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
      if '$ref' in parameter.keys():
        parameter = self.__dereference(self.components, parameter['$ref'], self.spec)

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

    required_params = []
    literal_params = []
    endpoint['query_param_names'] = []

    for parameter in parameters:
      if parameter.get('required'):
        required_params.append(parameter['name'])

      schema = parameter.get('schema', {})
      self.__extract_param_properties(self.components, required_params, {parameter['name']: schema}, literal_params, curr_id=len(literal_params)+1)

    self.__convert_literal_component_param(endpoint, literal_params, 'query_param_name')

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
    literal_params = []

    # Only support first media type
    for _, media_type in content.items():
      schema = media_type.get('schema')
      if schema:
        self.__extract_param_properties(self.components, [], {_ANONYMOUS: schema}, literal_params)
      break

    return literal_params

  def __add_info(self, file_data: Dict):
    file_data['info'] = {
      'version': '0.0.1',
      'title': ''
    }

  def __is_missing_oauth2_scopes(self, file_data: Dict):
    is_missing = False
    if 'components' in file_data:
      components = file_data['components']

      if 'securitySchemes' in components:
        security_schemes = components['securitySchemes']

        for scheme_name, scheme in security_schemes.items():
          if scheme.get('type') == 'oauth2':
            flows = scheme.get('flows')

            if flows and flows.get('clientCredentials'):
              scopes = flows.get('clientCredentials').get('scopes')

              if scopes is None:
                return True

            break

    return is_missing

  def __add_oauth2_default_scopes(self, file_data: Dict):
    if 'components' not in file_data:
      return
    components = file_data['components']

    if 'securitySchemes' not in components:
      return
    security_schemes = components['securitySchemes']

    oauth_security_scheme = {}
    for scheme_name, scheme in security_schemes.items():
      if scheme.get('type') == 'oauth2':
        oauth_security_scheme = scheme
        break

    # If empty dict or None
    if not oauth_security_scheme:
      return

    flows = oauth_security_scheme['flows']
    if not flows:
      return

    client_credentials = flows['clientCredentials']
    if not client_credentials:
      return

    client_credentials['scopes'] = {}

  def __get_most_recent_param(self, literal_params: dict):
    return list(literal_params)[-1] if literal_params else None

  def __get_second_most_recent_param(self, literal_params: dict):
    if not literal_params or len(literal_params) < 2:
      return None

    return list(literal_params)[-2]

  def __extract_param_properties(self, components, required_component_params, schema_object, literal_component_params, curr_id=0, parent_id=None, parent=None, query_string='', override_required=False):
    # Name of the schema object (i.e. the name of the body_param_name or response_param_name component)
    property_name = list(schema_object.keys())[0]

    # The actual OpenAPI schema object
    property_schema = list(schema_object.values())[0] 

    if '$ref' in property_schema.keys():
      property_schema = self.__dereference(components, property_schema.get('$ref'), self.spec)

    # Generates the entire query string for this particular property (ex: Pets[*].name for property 'name' of a 'Pet' element in the 'Pets' array
    if property_name == _ANONYMOUS:
      query = query_string 
    else:
      if property_name.endswith('Element'):
        query = f"{query_string}[*]"
      elif query_string == '':
        query = property_name
      else:
        query = f"{query_string}.{property_name}"

    # A schema is traversable if it has one more non-empty nested schema objects
    traversable = property_schema.get('properties') or property_schema.get('items') or property_schema.get('allOf')
    
    if not traversable:
      # Ex: {'name': {'type': 'string', 'description': 'Name of pet', 'Example': 'Buddy'}}
      if property_name != _ANONYMOUS:
        literal_val_type = self.__open_api_to_default_python_type(property_schema.get('type', 'object'))
        literal_val = {'name': property_name, 'values': [literal_val_type], 'required': override_required or bool(property_schema.get('required', False)), 'query': query, 'id': curr_id, 'parent_id': parent_id}
        literal_component_params.append(literal_val)
      return curr_id

    if 'properties' in property_schema.keys():
      # Ex: {'tmp': {'type': 'object', 'required': ['name'], 'properties': {'name': {'type': 'string'}, 'tag': {'type': 'string'}}}}
      _required = property_schema.get('required')
      if _required is not None:
        _required_list = _read_value(_required)
        required_component_params += _required_list if isinstance(_required_list, list) else []

      # curr_id_tmp is the parent_id of all elements in param_properties
      # Should be set to parent_id when property_name is 'tmp' to handle case where a schema uses the 'allOf' keyword since curr_id will change between every recursive call on each 'part' element in the allOf list
      curr_id_tmp = parent_id if property_name == _ANONYMOUS else curr_id 

      literal_val = parent if property_name == _ANONYMOUS else {'name': property_name, 'value': {}, 'required': override_required or bool(property_schema.get('schema_required', False)), 'query': query, 'id': curr_id, 'parent_id': parent_id}

      if property_name != _ANONYMOUS:
        literal_component_params.append(literal_val)

      param_properties = property_schema.get('properties')
      for property_key, property_value in param_properties.items():
        is_required = property_key in required_component_params
        if is_required:
          required_component_params.remove(property_key)
        curr_id = self.__extract_param_properties(components, required_component_params, {property_key: property_value}, literal_component_params, curr_id=curr_id+1, parent_id=curr_id_tmp, parent=literal_val, query_string=query, override_required=is_required)    

    elif property_schema.get('type') == 'array':
      # Ex: {'tmp': {'type': 'array', 'items': {'$ref': '#/components/schemas/NewPet'}}}
      if property_name == _ANONYMOUS:
        schema_object = {"Element": property_schema['items']}
        curr_id = self.__extract_param_properties(components, required_component_params, schema_object, literal_component_params, curr_id=curr_id+1, parent_id=parent_id, parent=parent, query_string=query)
      else:
        schema_object = {f"{property_name}Element": property_schema['items']}
        literal_val = {'name': property_name, 'value': [], 'required': override_required or bool(property_schema.get('required', False)), 'query': query, 'id': curr_id, 'parent_id': parent_id}
        literal_component_params.append(literal_val)
        curr_id = self.__extract_param_properties(components, required_component_params, schema_object, literal_component_params, curr_id=curr_id+1, parent_id=curr_id, parent=parent, query_string=query)

    elif 'allOf' in property_schema.keys():
      # Ex: {'Element': {'type': 'object', 'allOf': [{'$ref': '#/components/schemas/NewPet'}, {'type': 'object', 'required': ['id'], 'properties': {'id': {'type': 'integer', 'format': 'int64'}}}]}}
      all_of = property_schema.get('allOf')
      literal_val = parent if property_name == _ANONYMOUS else {'name': property_name, 'value': {}, 'required': override_required or bool(property_schema.get('self_required', False)), 'query': query, 'id': curr_id, 'parent_id': parent_id}
      if property_name != _ANONYMOUS:
        literal_component_params.append(literal_val)

      curr_id_tmp = parent_id if property_name == _ANONYMOUS else curr_id 
      for part in all_of:
        _part_required = part.get('required')
        if _part_required is not None:
          _part_required_list = _read_value(_part_required)
          required_component_params.extend(_part_required_list if isinstance(_part_required_list, list) else [])
        curr_id = self.__extract_param_properties(components, required_component_params, {_ANONYMOUS: part}, literal_component_params, curr_id=curr_id, parent_id=curr_id_tmp, parent=literal_val, query_string=query)

    return curr_id
  

  # Returns the schema object located at the given reference path
  def __dereference(self, components: SchemaPath, reference: str, spec: SchemaPath = None):
    # '#/components/schemas/NewPet' or '#/paths/~1users~1{id}/get/responses/200'
    if not reference.startswith('#'):
      # External reference (e.g., 'external-file.yaml#/components/schemas/Pet')
      if self.strict_refs:
        raise ValueError(f'External references are not supported yet: {reference}')
      else:
        # Log warning and return a placeholder object
        logger.warning(f'External reference "{reference}" cannot be resolved. Using placeholder object.')
        # Return a generic object schema as fallback
        return {
          'type': 'object',
          'description': f'External reference: {reference}',
          'x-external-ref': reference
        }
    
    # Remove leading '#'
    ref_path = reference[1:]
    
    # Handle component references: #/components/schemas/Pet
    if reference.startswith('#/components'):
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
    
    # Handle non-component references: #/paths/~1users/get/parameters/0
    if spec is None:
      raise ValueError(f'Non-component reference requires spec parameter: {reference}')
    
    # Split path by '/' and navigate through spec
    # Note: OpenAPI uses ~1 to escape '/' and ~0 to escape '~' in JSON pointers (RFC 6901)
    path_parts = ref_path.split('/')[1:]  # Skip empty string from leading '/'
    
    current = spec
    for i, part in enumerate(path_parts):
      # Unescape JSON pointer tokens
      unescaped_part = part.replace('~1', '/').replace('~0', '~')
      
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
    # Instantiate per call so mutable defaults (list, dict) are never shared
    return _OPENAPI_DEFAULT_TYPES.get(open_api_type, dict)()

  def __num_variables(self, url: str) -> int:
    num = url.count('{')
    return num

  def __evaluate_servers(self, servers: SchemaPath) -> List[dict]:
    result = []

    if not servers:
      default_server = {'url': '/'}
      return [default_server]

    for server in servers:
      original_url = server["url"]

      variables = server.get("variables", {})
      if not variables:
        result.append({'url': original_url})
        continue

      split_url = re.split('{|}', original_url)
      existent_vars = {}
      for part in split_url:
        if part in variables.keys():
          existent_vars[part] = variables[part]

      var_to_possible_vals = {}
      all_possible_vals = []

      for variable_name, variable in existent_vars.items():
        enum_list = variable.get('enum')
        if enum_list:
          var_to_possible_vals[variable_name] = _read_value(enum_list)
        else:
          var_to_possible_vals[variable_name] = [_read_value(variable.get('default'))]

      all_possible_vals = list(var_to_possible_vals.values())
      product = list(itertools.product(*all_possible_vals))

      for permutation in product:
        split_url_copy = copy.deepcopy(split_url)

        for i, part in enumerate(split_url_copy):
          for j, var in enumerate(var_to_possible_vals.keys()):
            if var == part:
              split_url_copy[i] = permutation[j]
              break

        evaluated_url = ''.join(split_url_copy)
        result.append({'url': evaluated_url})
    
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

    if '$ref' in header_definition:
      header_definition = self.__dereference(self.components, header_definition.get('$ref'), self.spec)

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