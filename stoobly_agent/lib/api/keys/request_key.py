
from .uuid_key import UuidKey

from stoobly_agent.app.settings import Settings

class InvalidRequestKey(Exception):
  pass

class RequestKey(UuidKey):
  def __init__(self, key: str):
    super().__init__(key)

    self.__raw = key

    if not self.id:
      raise InvalidRequestKey('Missing id')

    if not self.project_id:
      settings = Settings.instance()
      if settings.cli.features.remote:
        raise InvalidRequestKey('Missing request_id') 
    
  @property
  def project_id(self) -> str:
    return self.get('p')

  @property
  def raw(self):
    return self.__raw

  @staticmethod
  def encode(project_id: str, request_id: str):
    return UuidKey.encode({
      'p': project_id,
      'i': request_id.replace('-', ''),
    })