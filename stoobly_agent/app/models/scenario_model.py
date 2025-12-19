import pdb

from stoobly_agent.app.settings import Settings

from .types import ScenarioDestroyParams, ScenarioCreateParams
from .factories.resource.scenario import ScenarioResourceFactory
from .model import Model

class ScenarioModel(Model):

  def __init__(self, settings: Settings, **options):
    super().__init__(settings, **options)

  def as_local(self):
    self.adapter = ScenarioResourceFactory(self.settings.remote).local_db()
    self.is_local = True

  def as_remote(self):
    self.adapter = ScenarioResourceFactory(self.settings.remote).stoobly()
    self.is_local = False

  def create(self, **body_params: ScenarioCreateParams):
    try:
      return self.adapter.create(**body_params)
    except Exception as e:
      import requests
      if isinstance(e, requests.exceptions.RequestException):
        return self.handle_request_error(e)
      raise

  def show(self, scenario_id: str):
    try:
      return self.adapter.show(scenario_id)
    except Exception as e:
      import requests
      if isinstance(e, requests.exceptions.RequestException):
        return self.handle_request_error(e)
      raise

  def index(self, **query_params):
    try:
      return self.adapter.index(**query_params)
    except Exception as e:
      import requests
      if isinstance(e, requests.exceptions.RequestException):
        return self.handle_request_error(e)
      raise

  def update(self, scenario_id: str, **params: ScenarioCreateParams):
    try:
      return self.adapter.update(scenario_id, **params)
    except Exception as e:
      import requests
      if isinstance(e, requests.exceptions.RequestException):
        return self.handle_request_error(e)
      raise

  def destroy(self, scenario_id, **params: ScenarioDestroyParams):
    try:
      return self.adapter.destroy(scenario_id, **params)
    except Exception as e:
      import requests
      if isinstance(e, requests.exceptions.RequestException):
        return self.handle_request_error(e)
      raise

  def snapshot(self, scenario_id: str, **params):
    try:
      return self.adapter.snapshot(scenario_id, **params)
    except requests.exceptions.RequestException as e:
      return self.handle_request_error(e)   