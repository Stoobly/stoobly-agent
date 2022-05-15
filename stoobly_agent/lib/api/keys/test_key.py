from .resource_key import ResourceKey

class InvalidTestKey(Exception):
  pass

class TestKey(ResourceKey):

  def __init__(self, key: str):
    super().__init__(key)

    if not self.id:
      raise InvalidTestKey('Missing id')

    if not self.project_id:
      raise InvalidTestKey('Missing project_id')

  @property
  def id(self) -> str:
    return self.get('i')
  
  @property
  def project_id(self) -> str:
    return self.get('p')