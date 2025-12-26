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
    self._event = log_event
    self._log = log or Log()
    self._request = snapshot.mitmproxy_request
    self._response = snapshot.mitmproxy_response
    self._snapshot = snapshot

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

  @property
  def snapshot(self):
    return self._snapshot

  @property
  def uuid(self):
    return self.snapshot.uuid

  def delete(self, log: Log = None):
    log = log or self._log
    new_event = self._event.duplicate_as_delete()
    log.append(str(new_event))

  def save(self, log: Log = None):
    log = log or self._log
    request_uuid = self.snapshot.uuid
    joined_request = join_request_from_request_response(self.request, self.response, id=request_uuid)
    raw_request = joined_request.build()
    self.snapshot.write_raw(raw_request)
    new_event = self._event.duplicate()
    log.append(str(new_event))
    return new_event