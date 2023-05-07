from .resource_key import ResourceKey
from .organization_key import LOCAL_ORGANIZATION_ID

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
  @classmethod
  def local_key(cls) -> str:
    return cls.encode({
      'i': LOCAL_PROJECT_ID,
      'o': LOCAL_ORGANIZATION_ID,
    })

  @property
  def is_local(self) -> bool:
    return int(self.id) == LOCAL_PROJECT_ID

  @property
  def id(self) -> str:
    return self.get('i')
  
  @property
  def organization_id(self) -> str:
    return self.get('o')

  @staticmethod
  def check_is_local(id):
    return int(id) == LOCAL_PROJECT_ID

  @staticmethod
  def encode(id, organization_id = -1):
    return super(ProjectKey, ProjectKey).encode({
      'i': id,
      'o': organization_id,
    })
