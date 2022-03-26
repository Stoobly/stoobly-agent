from .resource_key import ResourceKey

class OrganizationKey(ResourceKey):

  @property
  def id(self) -> str:
    return self.decoded_key.get('i')

