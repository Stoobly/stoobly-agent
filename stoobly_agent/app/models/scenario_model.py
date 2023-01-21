import pdb
import requests

from typing import Union

from stoobly_agent.lib.logger import Logger
from stoobly_agent.lib.api.interfaces.scenarios import ScenarioShowResponse, ScenariosIndexResponse
from stoobly_agent.app.settings import Settings

from .adapters.scenario_adapter_factory import ScenarioAdapterFactory
from .adapters.types import ScenarioCreateParams
from .model import Model

class ScenarioModel(Model):

  def __init__(self, settings: Settings):
    super().__init__(settings)

  def as_local(self):
      self.adapter = ScenarioAdapterFactory(self.settings.remote).local_db()

  def as_remote(self):
      self.adapter = ScenarioAdapterFactory(self.settings.remote).stoobly()

  def create(self, **body_params: ScenarioCreateParams) -> Union[ScenarioShowResponse, None]:
    try:
      return self.adapter.create(**body_params)
    except requests.exceptions.RequestException as e:
      self.__handle_scenario_error(e)
      return None

  def show(self, scenario_id: str) -> Union[ScenarioShowResponse, None]:
    try:
      return self.adapter.show(scenario_id)
    except requests.exceptions.RequestException as e:
      self.__handle_scenario_error(e)
      return None

  def index(self, **query_params) -> Union[ScenariosIndexResponse, None]:
    try:
      return self.adapter.index(**query_params)
    except requests.exceptions.ScenarioException as e:
      self.__handle_scenario_error(e)
      return None

  def update(self, scenario_id: str, **params: ScenarioCreateParams) -> Union[ScenarioShowResponse, None]:
    try:
      return self.adapter.update(scenario_id, **params)
    except requests.exceptions.RequestException as e:
      self.__handle_scenario_error(e)
      return None

  def destroy(self, scenario_id) -> Union[ScenarioShowResponse, None]:
    try:
      return self.adapter.destroy(scenario_id)
    except requests.exceptions.RequestException as e:
      self.__handle_scenario_error(e)
      return None 

  def __handle_scenario_error(self, e: requests.exceptions.RequestException):
      response: requests.Response = e.response
      if response:
        Logger.instance().error(f"{response.status_code} {response.content}")