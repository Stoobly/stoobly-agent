import pdb

from urllib.parse import urlparse

from stoobly_agent.lib.api.keys.request_key import RequestKey
from stoobly_agent.lib.api.keys.scenario_key import ScenarioKey

def search_request(base_model, query: str):
  try:
    key = RequestKey(query)
    return base_model.where('uuid', key.id)
  except Exception as e:
    uri = urlparse(query)

    if uri.hostname:
      return base_model.where('host', uri.hostname).where('path', uri.path)
    else:
      pattern = f"%{query}%"
      return base_model.where('path', 'like', pattern).or_where('host', 'like', pattern)

def search_scenario(base_model, query: str):
  try:
    key = ScenarioKey(query)
    return base_model.where('uuid', key.id)
  except Exception as e:
    return base_model.where('name', 'like', f"%{query}%")