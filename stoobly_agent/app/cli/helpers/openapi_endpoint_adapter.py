import copy
from functools import reduce
import itertools
from pprint import pprint
import re
from typing import Dict, List, Union
from urllib.parse import urlparse

from openapi_core import Spec
import yaml

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

      spec = Spec.from_dict(file_data)

    return self.adapt(spec)

  def adapt(self, spec: Spec) -> List[EndpointShowResponse]:
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
          endpoint['host'] = parsed_url.netloc

          joined_path = self.__urljoin(parsed_url.path, path_name)
          split_parts = joined_path.split('/')
          pattern_path = []
          for part in split_parts:
            sanitized_part = part
            if part.startswith('{') and part.endswith('}'):
              sanitized_part = '%' 
            pattern_path.append(sanitized_part)
          pattern_path_str = '/'.join(pattern_path)
          endpoint['match_pattern'] = pattern_path_str
          endpoint['path'] = joined_path
          
          endpoint['port'] = str(parsed_url.port)
          if endpoint['port'] is None or endpoint['port'] == 'None':
            if parsed_url.scheme == 'https':
              endpoint['port'] = '443'
            elif parsed_url.scheme == 'http':
              endpoint['port'] = '80'
            else:
              endpoint['port'] = ''

          alias_counter = 0
          header_param_counter = 0
          operation = path[http_method]
          required_query_params = []
          required_body_params = []

          parameters = operation.get("parameters", {})
          for parameter in parameters:
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

              schema = parameter['schema']
              open_api_type = schema['type']

              param_value = None
              if open_api_type == 'array':
                item_type = schema['items']['type']
                default_value = schema['items'].get('default')
                item_default = None
                if default_value:
                  item_default = {'value': default_value}
                else:
                  item_default = {'value': self.__open_api_to_default_python_type(item_type)}

                param_value = [item_default]

              # TODO: can query params be something besides raw or array?
              else:
                default_value = schema.get('default')
                if default_value:
                  param_value = default_value
                else:
                  param_value = self.__open_api_to_default_python_type(open_api_type)

              literal_query_param = {
                parameter['name']: {'value': param_value}
              }

              if not endpoint.get('literal_query_params'):
                endpoint['literal_query_params'] = {}
              endpoint['literal_query_params'].update(literal_query_param)

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
          literal_body_params = {}
          request_body_array = False

          content = request_body.get("content", {})
          for mimetype, media_type in content.items():
            param_properties = {}
            schema = media_type['schema']

            # If Spec Component reference, look it up in components
            if '$ref' in schema:
              reference = schema['$ref']
              self.__dereference(components, reference, required_body_params, literal_body_params)
            else:
              required_body_params = schema.get('required', [])

              schema_type = schema.get('type')
              if schema_type:
                if schema_type == 'object':
                  param_properties = schema.get('properties', {})
                elif schema_type == 'array':
                  request_body_array = True
                  param_properties = {'tmp': schema['items']}

            for property_key, property_value in param_properties.items():
              if property_key in required_body_params:
                param_properties[property_key]['required'] = True

            if not endpoint.get('literal_body_params'):
              endpoint['literal_body_params'] = {}

            self.__extract_param_properties(components, None, required_body_params, param_properties, literal_body_params)

            endpoint['literal_body_params'] = literal_body_params

            # Only support first media type
            break

          literal_query_params = endpoint.get('literal_query_params')
          if literal_query_params:
            self.__convert_literal_component_param(endpoint, required_query_params, literal_query_params, 'query_param_name', 'literal_query_params')
            
          literal_body_params = endpoint.get('literal_body_params')
          if literal_body_params:
            if not request_body_array:
              self.__convert_literal_component_param(endpoint, required_body_params, literal_body_params, 'body_param_name', 'literal_body_params')
            else:
              self.__convert_literal_component_param(endpoint, required_body_params, [literal_body_params], 'body_param_name', 'literal_body_params')

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

  def __extract_param_properties(self, components, reference, required_body_params, param_properties, literal_body_params, nested_parameters: bool = False):
    if not param_properties:
      return

    flatten: bool = False

    for property_name, property_type_dict in param_properties.items():
      if '$ref' in property_type_dict.keys():
        if property_name not in literal_body_params:
          literal_body_params[property_name] = {'value': {}} 

        reference = property_type_dict['$ref']
        self.__dereference(components, reference, required_body_params, literal_body_params, nested_parameters=True)

      elif property_type_dict.get('properties'): 
        reference = None
        required_body_params += property_type_dict.get('required', [])
        param_properties = {}
        if not nested_parameters:
          param_properties = property_type_dict.get('properties')

        for property_key, property_value in param_properties.items():
          if property_key in required_body_params:
            property_value['required'] = True
            required_body_params.remove(property_key)

        self.__extract_param_properties(components, reference, required_body_params, param_properties, literal_body_params, nested_parameters=False)

      elif property_type_dict.get('type') == 'array':
        reference = None
        param_properties = {'tmp': property_type_dict['items']}

        if property_name not in literal_body_params:
          literal_body_params[property_name] = {'value': []} 
          if property_type_dict.get('required') == True:
            literal_body_params[property_name]['required'] = True

        self.__extract_param_properties(components, reference, required_body_params, param_properties, literal_body_params, nested_parameters=True)

      else:
        literal_val_type = self.__open_api_to_default_python_type(property_type_dict['type'])
        literal_val = {'value': literal_val_type, 'required': property_type_dict.get('required', False)}

        if nested_parameters:
          most_recent_param = self.__get_most_recent_param(literal_body_params)
          second_most_recent_param = self.__get_second_most_recent_param(literal_body_params)
          if most_recent_param == 'tmp':
            flatten = True

          if flatten:
            if second_most_recent_param and type(literal_body_params[second_most_recent_param]['value']) is list:
              literal_body_params[second_most_recent_param]['value'].append({ property_name: literal_val })
            else:
              literal_body_params[property_name] = literal_val
          else:
            if type(literal_body_params[most_recent_param]['value']) is dict:
              if not literal_body_params[most_recent_param].get('value'):
                literal_body_params[most_recent_param]['value'] = {}
              literal_body_params[most_recent_param]['value'][property_name] = literal_val

            elif type(literal_body_params[most_recent_param]['value']) is list:
              literal_body_params[most_recent_param]['value'].append(literal_val)
        else:
          literal_body_params[property_name] = literal_val

    literal_body_params.pop('tmp', None)

  def __dereference(self, components: Spec, reference: str, required_body_params: List, literal_body_params, nested_parameters: bool = False):
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
      required_body_params += body_spec.get('required', [])

      param_properties = body_spec.get('properties')
      all_of = body_spec.get('allOf')
      any_of = body_spec.get('anyOf')
      one_of = body_spec.get('oneOf')

      if param_properties:
        for param_prop_key, param_prop_val in param_properties.items():
          if param_prop_key in required_body_params:
            param_prop_val['required'] = True
            required_body_params.remove(param_prop_key)

        self.__extract_param_properties(components, None, required_body_params, param_properties, literal_body_params, nested_parameters=nested_parameters)

      elif all_of:
        for part in all_of:
          required_body_params = part.get('required', [])
          nested_reference = part.get('$ref')
          if nested_reference:
            self.__extract_param_properties(components, nested_reference, required_body_params, {'tmp': part}, literal_body_params)
          else:
            self.__extract_param_properties(components, None, required_body_params, {'tmp': part}, literal_body_params)

      # TODO
      # elif any_of or one_of:

      return param_properties 

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

    endpoint[component_name + 's'] = built_params_list
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

  def __evaluate_servers(self, servers: Spec) -> List[dict]:
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

