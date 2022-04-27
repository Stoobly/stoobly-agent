from .resource_key import ResourceKey

class InvalidScenarioKey(Exception):
  pass

class ScenarioKey(ResourceKey):

  @property
  def project_id(self) -> str:
    return self.get('p')

  @property
  def id(self) -> str:
    return self.get('i')