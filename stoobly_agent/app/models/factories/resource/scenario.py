from stoobly_agent.lib.orm.scenario import Scenario
from stoobly_agent.lib.api.scenarios_resource import ScenariosResource
from stoobly_agent.app.settings import RemoteSettings

from .local_db.scenario_adapter import LocalDBScenarioAdapter
from .stoobly.scenario_adapter import StooblyScenarioAdapter

class ScenarioResourceFactory():

  def __init__(self, settings: RemoteSettings):
    self.__remote_settings = settings

  def local_db(self) -> LocalDBScenarioAdapter:
    return LocalDBScenarioAdapter(Scenario)  

  def stoobly(self) -> StooblyScenarioAdapter:
    api = ScenariosResource(self.__remote_settings.api_url, self.__remote_settings.api_key)
    return StooblyScenarioAdapter(api)