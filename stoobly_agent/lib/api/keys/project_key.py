from .resource_key import ResourceKey

LOCAL_PROJECT_ID = 0

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
  def is_local(self) -> bool:
    return int(self.id) == LOCAL_PROJECT_ID

  @property
  def id(self) -> str:
    return self.get('i')
  
  @property
  def organization_id(self) -> str:
    return self.get('o')