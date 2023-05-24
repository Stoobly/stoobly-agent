import pdb

from stoobly_agent.app.models.types import EndpointCreateParams, OPENAPI_FORMAT
from stoobly_agent.app.settings import Settings

class EndpointFacade():

  def __init__(self, __settings: Settings):
    self.__settings = __settings

  def create(self, **kwargs: EndpointCreateParams):
    if kwargs.get('format') == OPENAPI_FORMAT:
      self.__create_from_openapi(kwargs.get('endpoints'))

  def __create_from_openapi(self, endpoints: str):
    # Parse
    # Adapt endpoints -> Stoobly endpoints
    # Find similar requests
    # For each request, check contract
    pass