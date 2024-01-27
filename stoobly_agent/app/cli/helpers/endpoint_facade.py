import pdb

from stoobly_agent.app.models.factories.resource.request import RequestResourceFactory
from stoobly_agent.app.settings import Settings

from .endpoints_apply_context import EndpointsApplyContext
from .endpoints_apply_service import apply_endpoints
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