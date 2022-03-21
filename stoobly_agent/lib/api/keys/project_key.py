from .resource_key import ResourceKey

class ProjectKey(ResourceKey):

  @property
  def id(self) -> str:
    return self.decoded_key.get('id')
