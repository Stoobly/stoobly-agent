import copy
import pdb

from functools import reduce
from openapi_core import Spec
from typing import List, TypedDict, Union
from urllib.parse import urlparse

from stoobly_agent.lib.api.interfaces.endpoints import (
  Alias,
  BodyParamName,
  EndpointShowResponse,
  RequestComponentName,
)
from stoobly_agent.lib.utils.python_to_ruby_type import convert

from .schema_builder import SchemaBuilder

class OpenApiEndpointAdapter():
  def __init__(self):
    return

  def adapt_from_file(self, file_path) -> List[EndpointShowResponse]:
    spec = Spec.from_file_path(file_path)
    return self.adapt(spec)

  def adapt(self, spec: Spec) -> List[EndpointShowResponse]:
    endpoints = []
    endpoint_counter = 0
    components = spec.get("components")
    schemas = components.get("schemas", {})
    paths = spec.getkey('paths')

    servers = spec / "servers"
    if not servers:
      default_server = {'url': '/'}
      servers = [default_server]

    for _, server in enumerate(servers):
      url = server["url"]
      variables = server.get("variables", {})

      for variable_name, variable in variables.items():
        variable["default"]
        variable["enum"]

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
            if parsed_url.scheme == 'http':
              endpoint['port'] = '80'

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

              if parameter['required'] == True:
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
                  item_default = default_value
                else:
                  item_default = self.__open_api_to_default_python_type(item_type)

                param_value = [item_default]

              # TODO: can query params be something besides raw or array?
              else:
                default_value = schema.get('default')
                if default_value:
                  param_value = default_value
                else:
                  param_value = self.__open_api_to_default_python_type(open_api_type)

              literal_query_param = {
                parameter['name']: param_value
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
          # servers = operation.get("servers", [])
          # for _, server in enumerate(servers):
          #   server["url"]
          #   server["description"]
          #
          #   variables = server.get("variables", {})
          #   for variable_name, variable in variables.items():
          #     variable["default"]
          #     variable.getkey("enum")

          request_body = operation.get("requestBody", {})
          required_request_body = request_body.get("required")

          content = request_body.get("content", {})
          for mimetype, media_type in content.items():
            schema = media_type['schema']
            # schema.type.value
            # schema.format
            # schema.required

            # If Spec Component reference, look it up in components
            if '$ref' in schema:
              # '#/components/schemas/NewPet'
              reference = schema['$ref']
              if not reference.startswith('#'):
                print('external references are not supported yet')
              if not reference.startswith('#/components/schemas'):
                print('non component references are not supported yet')
              else:
                ref_split = reference.split('#/components/schemas/')
                component_name = ref_split[-1]

                # {'type': 'object', 'required': ['name'], 'properties': {'name': {'type': 'string'}, 'tag': {'type': 'string'}}}
                body_spec = schemas.content()[component_name]

                required_body_params = body_spec.get('required', [])

                if not endpoint.get('literal_body_params'):
                  endpoint['literal_body_params'] = {}

                # {'name': {'type': 'string'}, 'tag': {'type': 'string'}}
                param_properties = body_spec['properties']
                literal_body_params = {}

                for property_name, property_type_dict in param_properties.items():
                  literal_val = self.__open_api_to_default_python_type(property_type_dict['type'])
                  literal_body_params[property_name] = literal_val

                endpoint['literal_body_params'] = literal_body_params

            else:
              print('non reference')

          literal_query_params = endpoint.get('literal_query_params')
          if literal_query_params:
            builder = SchemaBuilder(endpoint['id'], 'query_param_name')
            built_params = builder.build(literal_query_params)

            built_params_list = list(built_params)
            for param in built_params_list:
              if param in required_query_params:
                param['is_required'] = True
              else:
                param['is_required'] = False
            endpoint['query_param_names'] = built_params_list

            del endpoint['literal_query_params']
            
          literal_body_params = endpoint.get('literal_body_params')
          if literal_body_params:
            builder = SchemaBuilder(endpoint['id'], 'body_param_name')
            built_params = builder.build(literal_body_params)

            built_params_list  = list(built_params)
            for param in built_params_list:
              if param['name'] in required_body_params:
                param['is_required'] = True
              else:
                param['is_required'] = False
            endpoint['body_param_names'] = built_params_list

            del endpoint['literal_body_params']

          endpoints.append(endpoint)
    
    return endpoints

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
