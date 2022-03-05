from .resource_key import ResourceKey

class RequestKey(ResourceKey):

  @property
  def project_id(self) -> str:
    return self.decoded_key.get('project_id')

  @property
  def request_id(self) -> str:
    return self.decoded_key.get('request_id')