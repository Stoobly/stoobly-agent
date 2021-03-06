from .resource_key import ResourceKey

class InvalidProjectKey(Exception):
  pass

class ProjectKey(ResourceKey):

  def __init__(self, key: str):
    super().__init__(key)

    if not self.id:
      raise InvalidProjectKey('Missing id')

    if not self.organization_id:
      raise InvalidProjectKey('Missing organization_id')

  @property
  def id(self) -> str:
    return self.get('i')
  
  @property
  def organization_id(self) -> str:
    return self.get('o')