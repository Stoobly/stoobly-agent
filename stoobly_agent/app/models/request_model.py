import pdb

from stoobly_agent.app.models.schemas.request import Request
from stoobly_agent.app.settings import Settings

from .factories.resource.request import RequestResourceFactory
from .model import Model
from .types import RequestCreateParams, RequestDestroyParams, RequestDestroyAllParams, RequestIndexSimilarParams, RequestShowParams

class RequestModel(Model):

  def __init__(self, settings: Settings, **options):
    super().__init__(settings, **options)

  def as_local(self):
    self.adapter = RequestResourceFactory(self.settings.remote).local_db()
    self.is_local = True

  def as_remote(self):
    self.adapter = RequestResourceFactory(self.settings.remote).stoobly()
    self.is_local = False

  def create(self, **body_params: RequestCreateParams):
    try:
      return self.adapter.create(**body_params)
    except Exception as e:
      # Lazy import for runtime exception handling
      import requests
      if isinstance(e, requests.exceptions.RequestException):
        return self.handle_request_error(e)
      raise

  def show(self, request_id: str, **params: RequestShowParams):
    try:
      return self.adapter.show(request_id, **params)
    except Exception as e:
      import requests
      if isinstance(e, requests.exceptions.RequestException):
        return self.handle_request_error(e)
      raise

  def index_similar(self, params: RequestIndexSimilarParams):
    try:
      local_adapter = RequestResourceFactory(self.settings.remote).local_db()
      return local_adapter.similar(params)
    except Exception as e:
      import requests
      if isinstance(e, requests.exceptions.RequestException):
        return self.handle_request_error(e)
      raise

  def response(self, **query_params):
    return self.adapter.response(**query_params)

  def index(self, **query_params):
    try:
      return self.adapter.index(**query_params)
    except Exception as e:
      import requests
      if isinstance(e, requests.exceptions.RequestException):
        return self.handle_request_error(e)
      raise

  def update(self, request_id: str, **params: Request):
    try:
      return self.adapter.update(request_id, **params)
    except Exception as e:
      import requests
      if isinstance(e, requests.exceptions.RequestException):
        return self.handle_request_error(e)
      raise

  def destroy(self, request_id: str, **params: RequestDestroyParams):
    try:
      return self.adapter.destroy(request_id, **params)
    except Exception as e:
      import requests
      if isinstance(e, requests.exceptions.RequestException):
        return self.handle_request_error(e)
      raise

  def destroy_all(self, **params: RequestDestroyAllParams):
    try:
      return self.adapter.destroy_all(**params)
    except Exception as e:
      import requests
      if isinstance(e, requests.exceptions.RequestException):
        return self.handle_request_error(e)
      raise

  def snapshot(self, request_id: str, **params):
    try:
      return self.adapter.snapshot(request_id, **params)
    except Exception as e:
      import requests
      if isinstance(e, requests.exceptions.RequestException):
        return self.handle_request_error(e)
      raise
