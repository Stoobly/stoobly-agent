from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mitmproxy.http import Request, Response

from stoobly_agent.app.models.factories.resource.local_db.helpers.log import Log
from stoobly_agent.app.models.factories.resource.local_db.helpers.log_event import LogEvent
from stoobly_agent.app.models.factories.resource.local_db.helpers.request_snapshot import RequestSnapshot
from stoobly_agent.app.proxy.record.join_request_service import join_request_from_request_response

class SnapshotMigration():
  _request: 'Request'
  _response: 'Response'
  _snapshot: RequestSnapshot

  def __init__(self, snapshot: RequestSnapshot, log_event: LogEvent, log: Log = None):
    self._dirty = False
    self._event = log_event
    self._log = log or Log()
    self._request = snapshot.mitmproxy_request
    self._response = snapshot.mitmproxy_response
    self._snapshot = snapshot

  @property
  def dirty(self):
    return self._dirty

  @property
  def event(self):
    return self._event

  @property
  def log(self):
    return self._log

  @property
  def request(self):
    return self._request

  @request.setter
  def request(self, v: 'Request'):
    # Lazy import for runtime isinstance check
    from mitmproxy.http import Request
    if not isinstance(v, Request):
      raise TypeError('Invalid type.')
    self._request = v
    self._dirty = True

  @property
  def response(self):
    return self._response

  @response.setter
  def response(self, v: 'Response'):
    # Lazy import for runtime isinstance check
    from mitmproxy.http import Response
    if not isinstance(v, Response):
      raise TypeError('Invalid type.')
    self._response = v
    self._dirty = True

  @property
  def snapshot(self):
    return self._snapshot

  @property
  def uuid(self):
    return self.snapshot.uuid