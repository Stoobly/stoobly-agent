from .resource_key import ResourceKey

class InvalidRequestKey(Exception):
  pass

class RequestKey(ResourceKey):
  def __init__(self, key: str):
    super().__init__(key)

    if not self.id:
      raise InvalidRequestKey('Missing id')

    if not self.project_id:
      raise InvalidRequestKey('Missing request_id')

  @property
  def id(self) -> str:
    return self.get('i')
    
  @property
  def project_id(self) -> str:
    return self.get('p')

  @staticmethod
  def encode(project_id: str, request_id: str):
    return ResourceKey.encode({
      'p': project_id,
      'i': request_id,
    })