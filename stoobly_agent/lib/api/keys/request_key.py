from .resource_key import ResourceKey

class RequestKey(ResourceKey):

  @property
  def project_id(self) -> str:
    return self.decoded_key.get('p')

  @property
  def request_id(self) -> str:
    return self.decoded_key.get('i')

  @staticmethod
  def encode(project_id: str, request_id: str):
    return ResourceKey.encode({
      'p': project_id,
      'i': request_id,
    })