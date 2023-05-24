from functools import reduce
import urllib
import pdb
from typing import List, TypedDict
import urllib
import urllib.parse
from urllib.parse import urlparse

from openapi_core import Spec

from stoobly_agent.lib.api.interfaces.endpoints import (
  Alias,
  BodyParamName,
  EndpointShowResponse,
  RequestComponentName,
)
from stoobly_agent.lib.utils.python_to_ruby_type import convert

class QueryParamValue(TypedDict):
  value: str
  required: bool


class EndpointModel():
  def __init__(self):
    return

  def validate_and_parse(self, file_path) -> Spec:
    spec = Spec.from_file_path(file_path)
    return spec

  def adapt_openapi_endpoints(self, spec: Spec) -> List[EndpointShowResponse]:
    endpoints = []

    components = spec.get("components")
    if not components:
      # return
      exit(0)

    schemas = components.get("schemas", {})
    for schema_name, schema in schemas.items():
      schema.getkey("readOnly")
      schema.getkey("writeOnly")

    # ---

    paths = spec.getkey('paths')

    servers = spec / "servers"
    if not servers:
      default_server = {'url': '/'}
      servers = [default_server]

    for _, server in enumerate(servers):
      url = server["url"]
      # variables = server / "variables"
      variables = server.get("variables", {})

      for variable_name, variable in variables.items():
        variable["default"]
        variable["enum"]

      for path_name, path in paths.items():
        # print(f"path_name: {path_name}\npath: {path}\n")

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

          operation = path[http_method]
          parameters = operation.get("parameters", {})
          query_params = {}
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
              query_param['is_deterministic'] = True
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
              endpoint['header_names'].append(header)

            elif parameter['in'] == 'path':
              alias: Alias = {}
              alias['name'] = '{' + parameter['name'] + '}'
              # if not alias['id']:
              #   alias['id'] = 1

              if not endpoint.get('aliases'):
                endpoint['aliases'] = []

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
                  body_param: BodyParamName = {}
                  body_param['name'] = body_param_name
                  if body_param_name in required_body_params:
                    body_param['is_required'] = True
                  else:
                    body_param['is_required'] = False

                  for prop_key, prop_val in body_param_props.items():
                    if prop_key == 'type':
                      open_api_type = prop_val
                      python_type = self.__convert_open_api_type(open_api_type)
                      ruby_type = convert(python_type)
                      body_param['inferred_type'] = ruby_type

                  body_param['is_deterministic'] = True
                  body_params.append(body_param)

                if not endpoint.get('body_param_names'):
                  endpoint['body_param_names'] = []
                endpoint['body_param_names'] = body_params

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
