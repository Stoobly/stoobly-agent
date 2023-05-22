import copy
import pdb
from urllib.parse import parse_qs, urlencode
from urllib.parse import urlparse


from stoobly_agent.app.cli.helpers.replay_facade import ReplayFacade
from stoobly_agent.app.models.endpoint_model import EndpointModel
from stoobly_agent.app.models.factories.resource.request import RequestResourceFactory
from stoobly_agent.app.models.types.request import RequestFindParams
from stoobly_agent.app.proxy.replay.body_parser_service import JSON, decode_response
from stoobly_agent.app.settings import Settings
from stoobly_agent.lib.api.interfaces.requests import RequestShowResponse

# class EndpointFacade(ReplayFacade):
class EndpointFacade():
  def __init__(self, settings: Settings):
    self.settings = settings
    self.__endpoint_model = EndpointModel()
    self.local_db_request_adapter = RequestResourceFactory(self.settings.remote).local_db()
    # super().__init__(settings)

  def main_foo(self, file_path: str):
    # pdb.set_trace()
    open_api_spec = self.__endpoint_model.validate_and_parse(file_path=file_path)
    endpoints = self.__endpoint_model.extract_endpoints(open_api_spec)

    for endpoint in endpoints:
      host = endpoint['host']
      port = endpoint['port']
      method = endpoint['method']
      pattern = endpoint['path']
      url = endpoint.get('url', '')
      # host = 'petstore.swagger.io'
      # port = '443'
      # method = 'GET'
      # pattern = "pets"

      params = RequestFindParams(host=host, port=port, method=method, pattern=pattern)
      similar_requests = self.local_db_request_adapter.find_similar(params)

      for request in similar_requests:

        # Compare query params
        request_query_params = parse_qs(request.get_raw_attribute('query'))
        endpoint_query_params = endpoint.get('query_params', {})
        new_query_params = copy.deepcopy(request_query_params)

        # 1. Remove components that are no longer a part of the endpoint spec
        for request_query_param_key, request_query_param_val in request_query_params.items():
          if request_query_param_key not in endpoint_query_params:
            del new_query_params[request_query_param_key] 

        # 2. Create components that exist in the endpoint spec but not in the request and look for a default value
        # 3. If the endpoint spec says the component is optional, don't add it if it doesn't exist
        for endpoint_query_param_key, endpoint_query_param_val in endpoint_query_params.items():
          if endpoint_query_param_val['required'] and endpoint_query_param_key not in new_query_params:
            new_query_params[endpoint_query_param_key] = endpoint_query_params[endpoint_query_param_key]
        
        # Create full url such as 'http://petstore.swagger.io/v1/pets?limit=10'
        parsed_url = urlparse(request.url)
        parsed_url = parsed_url._replace(query=urlencode(new_query_params, True))
        url: str = parsed_url.geturl()

        # Compare body params
        decoded_response = decode_response(content="", content_type=JSON)

        # pdb.set_trace()
        assert url == request.url

        update_params: RequestShowResponse = {
          'body': 'some body' ,
          'url': url
        }

        print(f"request_id: {request.id}, params: {update_params}")
        # self.local_db_request_adapter.update(request_id=request.id, **update_params)
    
    return


