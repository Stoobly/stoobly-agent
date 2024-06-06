import copy
import itertools
import re
import yaml

from functools import reduce
from jsonschema_path import SchemaPath
from openapi_core import OpenAPI
from pprint import pprint
from typing import Dict, List, Union
from urllib.parse import urlparse

from stoobly_agent.lib.api.interfaces.endpoints import (
  Alias,
  EndpointShowResponse,
  RequestComponentName,
)
from stoobly_agent.lib.utils.python_to_ruby_type import convert_reverse

from .schema_builder import SchemaBuilder

class OpenApiEndpointAdapter():
  def __init__(self):
    return

  def adapt_from_file(self, file_path) -> List[EndpointShowResponse]:
    spec = {}

    with open(file_path, "r") as stream:
      file_data: Dict = yaml.safe_load(stream)

      if 'info' not in file_data:
        self.__add_info(file_data)

      missing_oauth2_scopes = self.__is_missing_oauth2_scopes(file_data)
      if missing_oauth2_scopes:
        self.__add_oauth2_default_scopes(file_data)

      openApi = OpenAPI.from_dict(file_data)
      spec = openApi.spec

    return self.adapt(spec)

  def adapt(self, spec: SchemaPath) -> List[EndpointShowResponse]:
    endpoints = []
    endpoint_counter = 0
    components = spec.get("components", {})
    schemas = components.get("schemas", {})
    paths = spec.getkey('paths')

    servers_spec = spec.get("servers")
    servers = self.__evaluate_servers(servers_spec)

    for _, server in enumerate(servers):
      url = server["url"]

      for path_name, path in paths.items():
        operations = [
            "get",
            "put",
            "post",
            "delete",
            "options",
            "head",
            "patch",
            "trace",
        ]
        for http_method in operations:
          if http_method not in path:
            continue

          endpoint_counter += 1

          parsed_url = urlparse(url)
          endpoint: EndpointShowResponse = {}
          endpoint['id'] = endpoint_counter
          endpoint['method'] = http_method.upper()
          endpoint['host'] = '-' if parsed_url.netloc == '' else parsed_url.netloc

          joined_path = self.__urljoin(parsed_url.path, path_name)
          split_parts = joined_path.split('/')
          pattern_path = []
          segment_names = []
          for part in split_parts:
            sanitized_part = part
            segment_name = part
            if part.startswith('{') and part.endswith('}'):
              sanitized_part = '%' 
              segment_name = f":{part[1:-1]}"
            pattern_path.append(sanitized_part)
            segment_names.append(segment_name)
          pattern_path_str = '/'.join(pattern_path)
          endpoint['match_pattern'] = pattern_path_str
          endpoint['path'] = joined_path

          endpoint['path_segment_names'] = []
          for segment_name in segment_names:
            if segment_name == "":
              continue
            path_component_name: RequestComponentName = {}
            path_component_name['name'] = segment_name
            path_component_name['type'] = "alias" if segment_name.startswith(':') else "static"
            endpoint['path_segment_names'].append(path_component_name)
          
          endpoint['port'] = str(parsed_url.port)
          if endpoint['port'] is None or endpoint['port'] == 'None':
            if parsed_url.scheme == 'https':
              endpoint['port'] = '443'
            elif parsed_url.scheme == 'http':
              endpoint['port'] = '80'
            else:
              endpoint['port'] = '0'

          alias_counter = 0
          header_param_counter = 0
          operation = path[http_method]
          required_query_params = []
          required_body_params = []
          literal_query_params = []

          parameters = operation.get("parameters", {})
          for parameter in parameters:
            if '$ref' in parameter.keys():
              parameter = self.__dereference(components, parameter['$ref'])

            if parameter['in'] == 'query':
              # query_param: RequestComponentName = {}
              # query_param['name'] = parameter['name']
              #
              # query_param_example = parameter.get('example')
              # if query_param_example:
              #   query_param['values'].append(query_param_example)

              if parameter.get('required') == True:
                required_query_params.append(parameter['name'])

              if not endpoint.get('query_param_names'):
                endpoint['query_param_names'] = []

              schema = parameter.get('schema', {})
              self.__extract_param_properties(components, required_query_params, {parameter['name']: schema}, literal_query_params, curr_id=len(literal_query_params)+1)

              endpoint['literal_query_params'] = literal_query_params

            elif parameter['in'] == 'header':
              header: RequestComponentName = {}
              header['name'] = parameter['name']
              header_example = parameter.get('example')
              if header_example:
                header['values'].append(header_example)
              if parameter['required'] == True:
                header['is_required'] = True
              else:
                header['is_required'] = False

              if not endpoint.get('header_names'):
                endpoint['header_names'] = []
              header['is_deterministic'] = True
              header_param_counter += 1
              header['id'] = header_param_counter

              endpoint['header_names'].append(header)

            elif parameter['in'] == 'path':
              if not endpoint.get('aliases'):
                endpoint['aliases'] = []

              found_alias = None
              for alias in endpoint['aliases']:
                if parameter['name'] == alias['name']:
                  found_alias = alias

              if not found_alias:
                alias: Alias = {}
                alias_counter += 1
                alias['id'] = alias_counter
                alias['name'] = '{' + parameter['name'] + '}'

                endpoint['aliases'].append(alias)

          # TODO: nested servers

          request_body = operation.get("requestBody", {})
          required_request_body = request_body.get("required")
          required_body_params = []
          literal_body_params = []

          content = request_body.get("content", {})
          for mimetype, media_type in content.items():
            schema = media_type.get('schema')
            if schema:
              self.__extract_param_properties(components, required_body_params, {'tmp': schema}, literal_body_params)

            if literal_body_params:
              endpoint['literal_body_params'] = literal_body_params

            # Only support first media type
            break

          literal_query_params = endpoint.get('literal_query_params')
          if literal_query_params:
            self.__convert_literal_component_param(endpoint, required_query_params, literal_query_params, 'query_param_name', 'literal_query_params')
            
          literal_body_params = endpoint.get('literal_body_params')
          if literal_body_params:
            self.__convert_literal_component_param(endpoint, required_body_params, literal_body_params, 'body_param_name', 'literal_body_params')

          # Responses -> construct lists of response header and response param name resources
          responses = operation.get('responses', {})
          if responses:
            self.__parse_responses(endpoint, responses, components)

          endpoints.append(endpoint)
    
    return endpoints

  def __add_info(self, file_data: Dict):
    if 'info' in file_data:
      return

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

  def __extract_param_properties(self, components, required_component_params, schema_object, literal_component_params, curr_id=0, parent_id=None, parent=None, query_string=''):
    # Name of the schema object (i.e. the name of the body_param_name or response_param_name component)
    property_name = list(schema_object.keys())[0]

    # The actual OpenAPI schema object
    property_schema = list(schema_object.values())[0] 

    if '$ref' in property_schema.keys():
      property_schema = self.__dereference(components, property_schema.get('$ref'))

    # Generates the entire query string for this particular property (ex: Pets[*].name for property 'name' of a 'Pet' element in the 'Pets' array
    if property_name == 'tmp':
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
      if property_name != 'tmp':
        literal_val_type = self.__open_api_to_default_python_type(property_schema.get('type', 'object'))
        literal_val = {'name': property_name, 'value': literal_val_type, 'required': property_schema.get('required', False), 'query': query, 'id': curr_id, 'parent_id': parent_id}
        literal_component_params.append(literal_val)
      return curr_id

    if 'properties' in property_schema.keys():
      # Ex: {'tmp': {'type': 'object', 'required': ['name'], 'properties': {'name': {'type': 'string'}, 'tag': {'type': 'string'}}}}
      required_component_params += property_schema.get('required', [])

      # curr_id_tmp is the parent_id of all elements in param_properties
      # Should be set to parent_id when property_name is 'tmp' to handle case where a schema uses the 'allOf' keyword since curr_id will change between every recursive call on each 'part' element in the allOf list
      curr_id_tmp = parent_id if property_name == 'tmp' else curr_id 

      literal_val = parent if property_name == 'tmp' else {'name': property_name, 'value': {}, 'required': property_schema.get('schema_required', False), 'query': query, 'id': curr_id, 'parent_id': parent_id}

      if property_name != 'tmp':
        literal_component_params.append(literal_val)

      param_properties = property_schema.get('properties')
      for property_key, property_value in param_properties.items():
        if property_key in required_component_params:
          if property_value.get('type') == 'object':
            # Necessary to avoid overwriting the 'required' list of an object-type schema
            property_value['schema_required'] = True
          else:
            property_value['required'] = True
          required_component_params.remove(property_key)
        curr_id = self.__extract_param_properties(components, required_component_params, {property_key: property_value}, literal_component_params, curr_id=curr_id+1, parent_id=curr_id_tmp, parent=literal_val, query_string=query)    

    elif property_schema.get('type') == 'array':
      # Ex: {'tmp': {'type': 'array', 'items': {'$ref': '#/components/schemas/NewPet'}}}
      if property_name == 'tmp':
        schema_object = {"Element": property_schema['items']}
        curr_id = self.__extract_param_properties(components, required_component_params, schema_object, literal_component_params, curr_id=curr_id+1, parent_id=parent_id, parent=parent, query_string=query)
      else:
        schema_object = {f"{property_name}Element": property_schema['items']}
        literal_val = {'name': property_name, 'value': [], 'required': property_schema.get('required', False), 'query': query, 'id': curr_id, 'parent_id': parent_id}
        literal_component_params.append(literal_val)
        curr_id = self.__extract_param_properties(components, required_component_params, schema_object, literal_component_params, curr_id=curr_id+1, parent_id=curr_id, parent=parent, query_string=query)

    elif 'allOf' in property_schema.keys():
      # Ex: {'Element': {'type': 'object', 'allOf': [{'$ref': '#/components/schemas/NewPet'}, {'type': 'object', 'required': ['id'], 'properties': {'id': {'type': 'integer', 'format': 'int64'}}}]}}
      all_of = property_schema.get('allOf')
      literal_val = parent if property_name == 'tmp' else {'name': property_name, 'value': {}, 'required': property_schema.get('self_required', False), 'query': query, 'id': curr_id, 'parent_id': parent_id}
      if property_name != 'tmp':
        literal_component_params.append(literal_val)

      curr_id_tmp = parent_id if property_name == 'tmp' else curr_id 
      for part in all_of:
        required_component_params = part.get('required', [])
        curr_id = self.__extract_param_properties(components, required_component_params, {'tmp': part}, literal_component_params, curr_id=curr_id, parent_id=curr_id_tmp, parent=literal_val, query_string=query)

    return curr_id
  

  # Returns the schema object located at the given reference path
  def __dereference(self, components: SchemaPath, reference: str):
    # '#/components/schemas/NewPet'
    if not reference.startswith('#'):
      print('external references are not supported yet')
    if not reference.startswith('#/components'):
      print('non component references are not supported yet')
    else:
      ref_split = reference.split('#/components/')
      component_data = ref_split[1].split('/')
      component_type = component_data[0]
      component_name = component_data[1]
      component = components.get(component_type, {})

      # Example: {'type': 'object', 'required': ['name'], 'properties': {'name': {'type': 'string'}, 'tag': {'type': 'string'}}}
      body_spec = component.content()[component_name]
        
      if '$ref' in body_spec.keys():
        body_spec = self.__dereference(components, body_spec.get('$ref'))
      
      return body_spec 
  
  def __convert_literal_component_param(self, endpoint: EndpointShowResponse,
      required_component_params: List[str], literal_component_params: Union[dict, list],
      component_name: str, literal_component_name: str) -> None:

    if not literal_component_params:
      return

    builder = SchemaBuilder(endpoint['id'], component_name)
    built_params = builder.build(literal_component_params)

    built_params_list = list(built_params)
    for param in built_params_list:
      if param.get('is_required', False) == True:
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

    del endpoint[literal_component_name]

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
    type_map = {}
    type_map['string'] = str(str)
    type_map['number'] = str(float)
    type_map['integer'] = str(int) 
    type_map['boolean'] = str(bool) 
    type_map['array'] = str(list)
    type_map['object'] = str(dict)

    return type_map[open_api_type]

  def __open_api_to_default_python_type(self, open_api_type: str):
    type_map = {}
    type_map['string'] = str()
    type_map['number'] = float()
    type_map['integer'] = int()
    type_map['boolean'] = bool()
    type_map['array'] = list()
    type_map['object'] = dict()

    return type_map[open_api_type]

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
          var_to_possible_vals[variable_name] = enum_list
        else:
          default_value = variable['default']
          var_to_possible_vals[variable_name] = [default_value]

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

  def __parse_responses(self, endpoint: EndpointShowResponse, responses: SchemaPath, components: SchemaPath):
    for response_code, response_definition in responses.items():
      # Only support status code 200 for now
      if response_code != '200':
        continue

      # Construct response param name components
      literal_response_params = []
      required_response_params = []
      response_content = response_definition.get('content', {})
      for mimetype, media_type in response_content.items():
        schema = media_type.get('schema')
        if schema:
          self.__extract_param_properties(components, required_response_params, {'tmp': schema}, literal_response_params)
        
        if literal_response_params:
          endpoint['literal_response_params'] = literal_response_params

        # Only support first media type
        break
      
      literal_response_params = endpoint.get('literal_response_params')
      if literal_response_params:
        self.__convert_literal_component_param(endpoint, required_response_params, literal_response_params, 'response_param_name', 'literal_response_params')

      # Construct response header name components
      response_headers = response_definition.get('headers', {})
      for header_name, header_definition in response_headers.items():
        response_header_name: RequestComponentName = {}
        response_header_name['name'] = header_name
        
        if '$ref' in header_definition:
          header_definition = self.__dereference(components, header_definition.get('$ref'))

        header_example = header_definition.get('example')
        if header_example:
          response_header_name['value']= header_example
        response_header_name['is_required'] = header_definition.get('is_required', False)
        response_header_name['is_deterministic'] = True
          
        if not endpoint.get('response_header_names'):
          endpoint['response_header_names'] = []
        endpoint['response_header_names'].append(response_header_name)	  
