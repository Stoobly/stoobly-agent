import pdb

from stoobly_agent.app.models.request_model import RequestModel
from stoobly_agent.app.models.scenario_model import ScenarioModel
from stoobly_agent.lib.api.keys.scenario_key import InvalidScenarioKey, ScenarioKey

from stoobly_agent.app.settings import Settings

def overwrite_scenario(scenario_key: str):
  if not scenario_key:
    return

  try:
    scenario_key = ScenarioKey(scenario_key)
  except InvalidScenarioKey:
    return

  settings = Settings.instance()
  scenario_model = ScenarioModel(settings) 
  scenario, status = scenario_model.show(scenario_key.id)

  if status != 200:
    return

  if not scenario.get('overwritable'):
    return

  status = scenario_model.update(scenario_key.id, **{ 'overwritable': False })[1]

  if status != 200:
    return 

  requests_model = RequestModel(settings)
  res, status = requests_model.destroy_all(scenario_id=scenario['id'])

  if status != 200:
    return

  return res