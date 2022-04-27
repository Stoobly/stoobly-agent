from .resource_key import ResourceKey

class InvalidProjectKey(Exception):
  pass

class ProjectKey(ResourceKey):

  @property
  def id(self) -> str:
    return self.get('i')
  
  @property
  def organization_id(self) -> str:
    return self.get('o')