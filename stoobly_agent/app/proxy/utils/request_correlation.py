"""Per-flow correlation id (typically mirroring ``HTTPFlow.id``) on the Request (not sent upstream)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from mitmproxy.http import Request as MitmproxyRequest

_CORRELATION_ATTR = '_stoobly_proxy_request_uuid'


def set_proxy_request_uuid(request: 'MitmproxyRequest', value: str) -> None:
    setattr(request, _CORRELATION_ATTR, value)


def get_proxy_request_uuid(request: 'MitmproxyRequest') -> Optional[str]:
    raw = getattr(request, _CORRELATION_ATTR, None)
    return str(raw) if raw is not None else None
