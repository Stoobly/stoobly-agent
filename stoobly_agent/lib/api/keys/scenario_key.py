from .resource_key import ResourceKey

class ScenarioKey(ResourceKey):

  @property
  def project_id(self) -> str:
    return self.decoded_key.get('p')

  @property
  def id(self) -> str:
    return self.decoded_key.get('i')