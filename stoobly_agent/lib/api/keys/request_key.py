from .resource_key import ResourceKey

class RequestKey(ResourceKey):

  @property
  def project_id(self) -> str:
    return self.decoded_key.get('project_id')

  @property
  def request_id(self) -> str:
    return self.decoded_key.get('request_id')

  @staticmethod
  def encode(project_id: str, request_id: str):
    return ResourceKey.encode({
      'project_id': project_id,
      'request_id': request_id,
    })