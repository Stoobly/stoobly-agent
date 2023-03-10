from .resource_key import ResourceKey

LOCAL_ORGANIZATION_ID = 0

class InvalidOrganizationKey(Exception):
  pass

class OrganizationKey(ResourceKey):

  def __init__(self, key: str):
    super().__init__(key)

    if not self.id:
      raise InvalidOrganizationKey('Missing id')

  @property
  def id(self) -> str:
    return self.get('i')

  @staticmethod
  def encode(organization_id: str):
    return ResourceKey.encode({
      'i': organization_id,
    })