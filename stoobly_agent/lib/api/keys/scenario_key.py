from .resource_key import ResourceKey

class InvalidScenarioKey(Exception):
  pass

class ScenarioKey(ResourceKey):

  def __init__(self, key: str):
    super().__init__(key)

    if not self.id:
      raise InvalidScenarioKey('Missing id')

    if not self.project_id:
      raise InvalidScenarioKey('Missing project_id')

  @property
  def project_id(self) -> str:
    return self.get('p')

  @property
  def id(self) -> str:
    return self.get('i')

  @staticmethod
  def encode(project_id: str, request_id: str):
    return ResourceKey.encode({
      'p': project_id,
      'i': request_id,
    })