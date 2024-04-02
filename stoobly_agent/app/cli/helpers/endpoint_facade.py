import pdb

from stoobly_agent.app.models.factories.resource.request import RequestResourceFactory
from stoobly_agent.app.settings import Settings
from stoobly_agent.lib.api.endpoints_resource import EndpointsResource
from stoobly_agent.lib.api.header_names_resource import HeaderNamesResource
from stoobly_agent.lib.api.body_param_names_resource import BodyParamNamesResource
from stoobly_agent.lib.api.query_param_names_resource import QueryParamNamesResource
from stoobly_agent.lib.api.response_param_names_resource import ResponseParamNamesResource
from stoobly_agent.lib.api.response_header_names_resource import ResponseHeaderNamesResource

from .endpoints_apply_context import EndpointsApplyContext
from .endpoints_import_context import EndpointsImportContext
from .endpoints_apply_service import apply_endpoints
from .endpoints_import_service import import_endpoints
from .synchronize_request_service import SynchronizeRequestService

class EndpointFacade():
  def __init__(self, __settings: Settings):
    self.__settings = __settings
  
  def apply(self, context: EndpointsApplyContext):
    local_db_request_adapter = RequestResourceFactory(self.__settings.remote).local_db()
    context.with_request_model(local_db_request_adapter)

    lifecycle_hooks = context.lifecycle_hooks
    synchronize_request_service = SynchronizeRequestService(local_db_request_adapter=local_db_request_adapter)
    request_handler = lambda request, endpoint: synchronize_request_service.synchronize_request(
      request, endpoint, lifecycle_hooks
    )
    context.with_request_handler(request_handler)

    apply_endpoints(context)
  
  def import_endpoints(self, context: EndpointsImportContext):
    api_url = self.__settings.remote.api_url
    api_key = self.__settings.remote.api_key

    context.with_endpoint_resource(EndpointsResource(api_url, api_key))
    context.with_header_name_resource(HeaderNamesResource(api_url, api_key))
    context.with_body_param_name_resource(BodyParamNamesResource(api_url, api_key))
    context.with_query_param_name_resource(QueryParamNamesResource(api_url, api_key))
    context.with_response_param_name_resource(ResponseParamNamesResource(api_url, api_key))
    context.with_response_header_name_resource(ResponseHeaderNamesResource(api_url, api_key))

    import_endpoints(context)