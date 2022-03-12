from ..settings import Settings
from .adapters.request_adapter_factory import RequestAdapterFactory

class Request():

  def __init__(self, settings: Settings):
    self.adapter = RequestAdapterFactory(settings).get()

  def create(self, project_id: str, raw_requests, params):
    return self.adapter.create(project_id, raw_requests, params)

  def show(self, project_id: str, request_id: str, query_params):
    return self.adapter.show(project_id, request_id, query_params)

  def index(self, project_id: int, query_params):
    return self.adapter.index(project_id, query_params)