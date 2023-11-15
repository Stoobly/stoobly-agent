import uuid

from .uuid_key import UuidKey

class InvalidScenarioKey(Exception):
  pass

class ScenarioKey(UuidKey):

  def __init__(self, key: str):
    super().__init__(key)

    self.__raw = key

    if not self.id:
      raise InvalidScenarioKey('Missing id')

    if not self.project_id:
      raise InvalidScenarioKey('Missing project_id')

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