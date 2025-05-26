from requests import Request, Response

from stoobly_agent.app.models.factories.resource.local_db.helpers.request_snapshot import RequestSnapshot

class SnapshotMigration():
  request: Request
  response: Response
  _snapshot: RequestSnapshot

  def __init__(self, snapshot: RequestSnapshot):
    self.request = snapshot.python_request
    self.response = snapshot.python_response
    self._snapshot = snapshot

  @property
  def snapshot(self):
    return self._snapshot

  @property
  def uuid(self):
    return self.snapshot.uuid

  def delete(self):
    pass

  def save(self):
    pass
 