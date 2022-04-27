from .resource_key import ResourceKey

class InvalidReportKey(Exception):
  pass

class ReportKey(ResourceKey):

  def __init__(self, key: str):
    super().__init__(key)

    if not self.id:
      raise InvalidReportKey('Missing id')

    if not self.project_id:
      raise InvalidReportKey('Missing project_id')

  @property
  def project_id(self) -> str:
    return self.get('p')

  @property
  def id(self) -> str:
    return self.get('i')