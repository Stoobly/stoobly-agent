from typing import Union

from stoobly_agent.lib.api.requests_resource import RequestsResource

from ...settings import Settings
from .local_db_request_adapter import LocalDBRequestAdapter
from .stoobly_request_adapter import StooblyRequestAdapter

class RequestAdapterFactory():

  def __init__(self, settings: Settings):
    self.settings = settings

  def get(self) -> Union[LocalDBRequestAdapter, StooblyRequestAdapter]:
    api = RequestsResource(self.settings.api_url, self.settings.api_key)
    return api