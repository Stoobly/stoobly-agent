from .resource_key import ResourceKey

class InvalidOrganizationKey(Exception):
  pass

class OrganizationKey(ResourceKey):

  @property
  def id(self) -> str:
    return self.get('i')

