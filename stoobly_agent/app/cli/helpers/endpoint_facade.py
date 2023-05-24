import copy
import pdb
from urllib.parse import parse_qs, urlencode
from urllib.parse import urlparse

from stoobly_agent.app.models.endpoint_model import EndpointModel
from stoobly_agent.app.models.factories.resource.request import RequestResourceFactory
from stoobly_agent.app.models.types import EndpointCreateParams, OPENAPI_FORMAT
from stoobly_agent.app.models.types.request import RequestFindParams
from stoobly_agent.app.settings import Settings
from stoobly_agent.app.settings import Settings

class EndpointFacade():
  def __init__(self, __settings: Settings):
    self.__settings = __settings
    self.__endpoint_model = EndpointModel()
    self.local_db_request_adapter = RequestResourceFactory(self.__settings.remote).local_db()
  
  def create(self, **kwargs: EndpointCreateParams):
    if kwargs.get('format') == OPENAPI_FORMAT:
      self.__create_from_openapi(kwargs.get('endpoints'))

  # def __create_from_openapi(self, endpoints: str):
  def __create_from_openapi(self, file_path: str):
    open_api_spec = self.__endpoint_model.validate_and_parse(file_path=file_path)
    endpoints = self.__endpoint_model.adapt_openapi_endpoints(open_api_spec)

    for endpoint in endpoints:
      host = endpoint['host']
      if host == '':
        host = '%'
      port = endpoint['port']
      method = endpoint['method']
      pattern = endpoint['match_pattern']
      url = endpoint.get('url', '')
      # host = 'petstore.swagger.io'
      # port = '443'
      # method = 'GET'
      # pattern = "pets"
      endpoint_body = endpoint.get('body')

      params = RequestFindParams(host=host, port=port, method=method, pattern=pattern)
      similar_requests = self.local_db_request_adapter.find_similar_requests(params)
      pdb.set_trace()


      # TODO: replace
       
      # for request in similar_requests:
      #   pdb.set_trace()
      #
      #   # --- Compare query params
      #   request_query_params: dict = parse_qs(request.get_raw_attribute('query'))
      #   endpoint_query_params = endpoint.get('query_params', {})
      #   new_query_params = copy.deepcopy(request_query_params)
      #
      #   # 1. Remove components that are no longer a part of the endpoint spec
      #   for request_query_param_key, request_query_param_val in request_query_params.items():
      #     if request_query_param_key not in endpoint_query_params:
      #       del new_query_params[request_query_param_key] 
      #
      #   # 2. Create components that exist in the endpoint spec but not in the request and look for a default value
      #   # 3. If the endpoint spec says the component is optional, don't add it if it doesn't exist
      #   for endpoint_query_param_key, endpoint_query_param_val in endpoint_query_params.items():
      #     if endpoint_query_param_val['required'] and endpoint_query_param_key not in new_query_params:
      #       new_query_params[endpoint_query_param_key] = endpoint_query_params[endpoint_query_param_key]
      #   
      #   # Create full url such as 'http://petstore.swagger.io/v1/pets?limit=10'
      #   parsed_url = urlparse(request.url)
      #   parsed_url = parsed_url._replace(query=urlencode(new_query_params, True))
      #   new_url: str = parsed_url.geturl()
      #
      #
      #
      #   # --- Compare body params
      #   python_request: requests.Request = RawHttpRequestAdapter(request.raw).to_request()
      #   request_body_data: bytes = python_request.data
      #   request_body: dict = json.loads(request_body_data.decode('utf-8'))
      #   new_request_body = copy.deepcopy(request_body)
      #
      #   # '{"type": "object", "required": ["name"], "properties": {"name": {"type": "string"}, "tag": {"type": "string"}}, "content_type": "application/json"}'
      #   pdb.set_trace()
      #   endpoint_body_dict: dict = json.loads(endpoint_body)
      #   if endpoint_body_dict['required_body']:
      #     required_body_params: List[str] = endpoint_body_dict['required']
      #     body_params_spec = endpoint_body_dict['properties']
      #
      #     # If body param not in spec, remove from request
      #     for request_body_param in request_body.keys():
      #       if request_body_param not in body_params_spec:
      #         del new_request_body[request_body_param]
      #    
      #     # If body param is required but doesn't exist, add it.
      #     # If no example then default to the default of the type
      #     for required_body_param in required_body_params:
      #       if required_body_param not in request_body:
      #         default_body_param_value = None
      #         body_param_value_type = body_params_spec[required_body_param]
      #         if body_param_value_type == 'string':
      #           default_body_param_value = ''
      #         elif body_param_value_type == 'integer':
      #           default_body_param_value = int()
      #         elif body_param_value_type == 'number':
      #           default_body_param_value = float
      #         new_request_body[required_body_param] = default_body_param_value
      #
      #   new_request_body_str: str = json.dumps(new_request_body)
      #   new_body: Union[bytes, str] = encode_response(content=new_request_body_str, content_type=endpoint_body_dict['content_type'])
      #
      #   assert new_url == request.url
      #
      #   update_params: RequestShowResponse = {
      #     'body': new_body,
      #     'url': new_url
      #   }
      #
      #   pdb.set_trace()
      #
      #   print(f"request_id: {request.id}, params: {update_params}")
      #   # self.local_db_request_adapter.update(request_id=request.id, **update_params)
    
    return
 
