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

class OpenApiEndpointAdapter():
  def __init__(self):
    return

  def adapt_from_file(self, file_path) -> Spec:
    spec = Spec.from_file_path(file_path)
    return self.adapt(spec)

  def adapt(self, spec: Spec) -> List[EndpointShowResponse]:
    endpoints = []
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

          parsed_url = urlparse(url)
          endpoint: EndpointShowResponse = {}
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

          query_params = {}
          alias_counter = 0
          header_param_counter = 0
          query_param_counter = 0
          operation = path[http_method]

          parameters = operation.get("parameters", {})
          for parameter in parameters:
            if parameter['in'] == 'query':
              query_param: RequestComponentName = {}
              query_param['name'] = parameter['name']

              query_param_example = parameter.get('example')
              if query_param_example:
                query_param['values'].append(query_param_example)
              if parameter['required'] == True:
                query_param['is_required'] = True
              else:
                query_param['is_required'] = False

              if not endpoint.get('query_param_names'):
                endpoint['query_param_names'] = []
              query_param_counter += 1
              query_param['id'] = query_param_counter

              schema = parameter['schema']
              open_api_type = schema['type']
              python_type = self.__convert_open_api_type(open_api_type)
              ruby_type = convert(python_type)
              query_param['inferred_type'] = ruby_type

              query_param['is_deterministic'] = True
              query_param['query_param_name_id'] = None

              if open_api_type == 'array' or open_api_type == 'object':
                query_param['items_type'] = schema['items']['type']

                builder = SchemaBuilder(0, 'QueryParamName', 'query_param_name')
                new_query_params = builder.build(query_param)
                query_param_counter += len(new_query_params) - 1

                endpoint['query_param_names'] += new_query_params
              else:
                query_param['query'] = query_param['name']
                endpoint['query_param_names'].append(query_param)

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

          # if query_params:
          #   simple_dict = self.__to_simple_dict(query_params)
          #   endpoint['query'] = urllib.parse.urlencode(simple_dict)

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

          # TODO: is url needed here? no
          # if not endpoint.get('url'):
          #   endpoint['url'] = self.__build_url(host=endpoint['host'], scheme='', port=endpoint['port'], path=endpoint['path'], query=endpoint.get('query'))

          request_body = operation.get("requestBody", {})
          # if not request_body:
          #   continue

          required_request_body = request_body.get("required")
          # if not required_request_body:
          #   continue

          body_param_counter = 0
          content = request_body.get("content", {})
          for mimetype, media_type in content.items():
            # if mimetype in [JSON, MULTIPART_FORM, WWW_FORM_URLENCODED]: 
            #   body = decode_response(content='', content_type=mimetype)

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
                # body_spec['content_type'] = mimetype
                # body_spec['required_body'] = required_request_body

                body_params: List[BodyParamName] = []
                required_body_params = body_spec.get('required', [])
                for body_param_name, body_param_props in body_spec['properties'].items():
                  body_param: BodyParamName = { 'body_param_name_id': None }
                  body_param['name'] = body_param_name
                  body_param['is_deterministic'] = True
                  if body_param_name in required_body_params:
                    body_param['is_required'] = True
                  else:
                    body_param['is_required'] = False

                  open_api_type = body_param_props['type']
                  python_type = self.__convert_open_api_type(open_api_type)
                  ruby_type = convert(python_type)
                  body_param['inferred_type'] = ruby_type

                  body_param_counter += 1
                  body_param['id'] = body_param_counter
                  body_param['query'] = body_param['name']

                  body_params.append(body_param)

                if not endpoint.get('body_param_names'):
                  endpoint['body_param_names'] = []

                endpoint['body_param_names'] = body_params
            else:
              print('non reference')

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

class SchemaBuilder:
  ###
  #
  # @param endpoint_id [Integer]
  # @param param_name_class [QueryParamName, BodyParamName, ResponseParamName]
  # @param param_column_name [String] e.g. query_param_name, body_param_name, response_param_name
  #
  def __init__(self, endpoint_id, param_name_class, param_column_name: str):
    self.endpoint_id = endpoint_id
    self.param_name_class = param_name_class
    self.param_column_name: str = param_column_name

    self.param_names = []
    self.param_names_created = []

  def __infer_type(self, val) -> str:
    return val.__class__.__name__
  
  def build(self, params):
    return self.__traverse('', params, None)

  ###
  #
  # @param name [String] name of current param
  # @param value [Object] value of current param
  # @param param [QueryParamName, BodyParamName, ResponseParamName] parent param record
  #
  def __traverse(self, name: str, value, param: RequestComponentName):

    # if type(value) is list:
    #   self.__traverse_array(name, value, param)
    # elif type(value) is dict:
    #   self.__traverse_hash(name, value, param)

    if value['inferred_type'] == 'Array':
      return self.__traverse_array(name, value, param)
    if value['inferred_type'] == 'Hash':
      return self.__traverse_hash(name, value, param)

  def __traverse_array(self, name: str, value, parent_param: RequestComponentName):
    columns = {
      # 'name':  f"{name.capitalize()}Element",
      # 'query': f"{parent_param.get('query')}[*]" if parent_param else '[*]'
      'query': value['name']
    }
    # columns[self.param_column_name] = parent_param

    # Iterate
    # types = {}
    # for e in value:
    #   _type = self.__infer_type(e)
    #
    #   if types.get(_type) is None:
    #     columns['inferred_type'] = convert(_type)
    #     types[_type] = self.__find_or_create_by(columns, value)
    #
    #   self.__traverse('', e, types[_type])

    new_parent = {**value, **columns}
    child = copy.deepcopy(new_parent)
    child['id'] = new_parent['id'] + 1
    child['name'] = f"{value['name']}Element"
    child['query'] = f"{value['name']}[*]"
    child['inferred_type'] = new_parent['items_type']
    child[self.param_column_name + '_id'] = new_parent['id']

    new_params = [new_parent, child]

    return new_params 

  def __traverse_hash(self, name, value, parent_param: RequestComponentName):
    # Iterate
    for k, v in value.items():
      columns = {
        # 'endpoint_id': self.endpoint_id,
        'inferred_type': convert(self.__infer_type(v)),
        'is_required': v is not None,
        'name': k,
        'query': f"{parent_param.get('query')}.{k}" if parent_param else k, 
      }
      # columns[self.param_column_name] = parent_param
      param = self.__find_or_create_by(columns, value)

      # self.__traverse(k, v, param)
    return

  def __find_or_create_by(self, columns, params):
    param = self.__find_by(columns, params) 
    if param is None:
      self.__create(columns, params)

    return

  def __find_by(self, columns, params) -> Union[RequestComponentName, None]:
    # columns: [('name', 'Element'), ('query', '[*]'), ('inferred_type', None)]
    found_count = len(columns)
    for field_key, field_val in columns.items():

      # params: [{'name': 'tags', 'is_required': False, 'is_deterministic': True, 'id': 1}, {'name': 'limit', 'is_required': False, 'is_deterministic': True, 'id': 2}]
      for param in params:
        if field_key == param.get(field_key) and param[field_key] == field_val:
          found_count -= 1
          if found_count == 0:
            return columns
          break

    return None

  def __create(self, columns, params):
    # create
    param: RequestComponentName = columns
    param[self.param_column_name + '_id'] = None
    params.append(param)

    self.param_names_created.append(param)
    self.param_names.append(param)
    return
