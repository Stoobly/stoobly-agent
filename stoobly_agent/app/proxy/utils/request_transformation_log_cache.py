from __future__ import annotations

from typing import TYPE_CHECKING, List, Literal, Optional, TypedDict

if TYPE_CHECKING:
    from mitmproxy.http import Request as MitmproxyRequest

from stoobly_agent.app.settings.constants import request_component as req_comp
from stoobly_agent.config.constants import custom_headers
from stoobly_agent.config.constants.mode import AgentMode
from stoobly_agent.lib.cache import Cache

TransformationAction = Literal['rewrite', 'filter', 'noop']
TransformationLifecycle = Literal['request', 'response']
TransformationTarget = Literal[
    'url',
    req_comp.HEADER,
    req_comp.BODY_PARAM,
    req_comp.QUERY_PARAM,
    req_comp.RESPONSE_HEADER,
    req_comp.RESPONSE_PARAM,
]


class RequestTransformationLogEntry(TypedDict):
    action: TransformationAction
    lifecycle: TransformationLifecycle
    target: TransformationTarget
    mode: AgentMode
    details: str


def append_log_from_request(
    request: 'MitmproxyRequest',
    entry: RequestTransformationLogEntry,
    *,
    timeout: Optional[int] = None,
) -> None:
    request_uuid = request.headers.get(custom_headers.PROXY_REQUEST_UUID)
    if not request_uuid:
        return
    RequestTransformationLogCache.instance().append(str(request_uuid), entry, timeout=timeout)


class RequestTransformationLogCache:
    _instance: Optional['RequestTransformationLogCache'] = None

    def __init__(self):
        if RequestTransformationLogCache._instance:
            raise RuntimeError('Call instance() instead')
        self._cache = Cache.instance()

    @classmethod
    def instance(cls) -> 'RequestTransformationLogCache':
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def append(
        self,
        request_uuid: str,
        entry: RequestTransformationLogEntry,
        *,
        timeout: Optional[int] = None,
    ) -> None:
        datum = self._cache.read(request_uuid)
        existing: List[RequestTransformationLogEntry] = []
        if datum and datum.get('value') is not None:
            raw = datum['value']
            if isinstance(raw, list):
                existing = list(raw)
        entry_copy: RequestTransformationLogEntry = {
            'action': entry['action'],
            'lifecycle': entry['lifecycle'],
            'target': entry['target'],
            'mode': entry['mode'],
            'details': entry['details'],
        }
        existing.append(entry_copy)
        self._cache.write(request_uuid, existing, timeout=timeout)

    def append_many(
        self,
        request_uuid: str,
        entries: List[RequestTransformationLogEntry],
        *,
        timeout: Optional[int] = None,
    ) -> None:
        if not entries:
            return
        datum = self._cache.read(request_uuid)
        existing: List[RequestTransformationLogEntry] = []
        if datum and datum.get('value') is not None:
            raw = datum['value']
            if isinstance(raw, list):
                existing = list(raw)
        for entry in entries:
            existing.append({
                'action': entry['action'],
                'lifecycle': entry['lifecycle'],
                'target': entry['target'],
                'mode': entry['mode'],
                'details': entry['details'],
            })
        self._cache.write(request_uuid, existing, timeout=timeout)

    def read(self, request_uuid: str) -> List[RequestTransformationLogEntry]:
        datum = self._cache.read(request_uuid)
        if not datum or datum.get('value') is None:
            return []
        raw = datum['value']
        if not isinstance(raw, list):
            return []
        return list(raw)

    def delete(self, request_uuid: str) -> None:
        self._cache.delete(request_uuid)
