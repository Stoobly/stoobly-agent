from .resource_key import ResourceKey

class RequestKey(ResourceKey):

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