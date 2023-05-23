from functools import reduce
import pdb
from typing import Dict, List, TypedDict, Union
import urllib
import urllib.parse
from urllib.parse import urlparse

from openapi_core import Spec
from stoobly_agent.app.proxy.replay.body_parser_service import JSON, MULTIPART_FORM, WWW_FORM_URLENCODED, decode_response, encode_response
from stoobly_agent.lib.api.interfaces.endpoints import EndpointShowResponse

from stoobly_agent.lib.api.interfaces.requests import RequestShowResponse

class QueryParamValue(TypedDict):
  value: str
  required: bool


class EndpointModel():
  def __init__(self):
    return

  def validate_and_parse(self, file_path) -> Spec:
    spec = Spec.from_file_path(file_path)
    return spec

  def extract_endpoints(self, spec: Spec) -> List[EndpointShowResponse]:
    endpoints = []

    # for item in spec.items():
    #   print(item)
    #
    # print()

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
          operation = path[http_method]
          # print(f"method: {http_method}, url: {url}, path_name: {path_name}\noperation: {operation}\n")

          parsed_url = urlparse(url)
          # endpoint = RequestShowResponse()
          endpoint = EndpointShowResponse()
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
          endpoint['path'] = pattern_path_str

          endpoint['port'] = parsed_url.port 
          if endpoint['port'] is None:
            if parsed_url.scheme == 'https':
              endpoint['port'] = '443'
            if parsed_url.scheme == 'http':
              endpoint['port'] = '80'

          parameters = operation.get("parameters", {})
          query_params = {}
          # query_params = Dict[str, Union[QueryParamValue, None]]
          # query_params = Dict[str, QueryParamValue]
          for parameter in parameters:
            # print(f"req params: {parameters}\n")

            if parameter['in'] == 'query':
              # if not parameter['required']:
              #   continue

              query_param_val:  QueryParamValue = {
                'value': parameter.get('example'),
                'required': parameter['required']
              }
              query_params[parameter['name']] = query_param_val
            elif parameter['in'] == 'header':
              endpoint['headers'] += parameter['name'] 

          if query_params:
            simple_dict = self.__to_simple_dict(query_params)
            endpoint['query'] = urllib.parse.urlencode(simple_dict)
            endpoint['query_params'] = query_params

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

          request_body = operation.get("requestBody")
          # if not request_body:
          #   continue

          required_request_body = request_body.get("required")
          # if not required_request_body:
          #   continue

          content = request_body.get("content")
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
                body_spec = schemas.content()[component_name]
                body_spec['content_type'] = mimetype
                body_spec['required_body'] = required_request_body
                # pdb.set_trace()
                endpoint['body']: str = encode_response(content=body_spec, content_type=JSON)

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
    
    # pdb.set_trace()
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
