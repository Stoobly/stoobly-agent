"""Ephemeral reverse-proxy host remapping from --proxy-regular-upstream / env."""

from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Optional

if TYPE_CHECKING:
    from mitmproxy.http import HTTPFlow as MitmproxyHTTPFlow
    from mitmproxy.http import Request as MitmproxyRequest

from stoobly_agent.app.proxy.utils.request_handler import reverse_proxy
from stoobly_agent.lib.logger import Logger

LOG_ID = 'Upstreams'

_ORIGINAL_HOST_ATTR = '_stoobly_upstreams_original_host'
_ORIGINAL_PORT_ATTR = '_stoobly_upstreams_original_port'
_ORIGINAL_SCHEME_ATTR = '_stoobly_upstreams_original_scheme'


def parse_proxy_regular_upstreams(raw: Optional[str]) -> Dict[str, str]:
    """
    Parse comma-separated ``HOST:PORT=SPEC`` mappings into a dict.

    SPEC format matches proxy-mode reverse SPEC: ``http[s]://host[:port]``
    Port is optional and inferred from scheme if omitted (80 for http, 443 for https).

    Examples:
      ``local.api.stoobly:3001=http://host.docker.internal:3002``
      ``api.example.com:443=https://backend,other:80=http://internal:8080``
    """
    if not raw:
        return {}

    upstreams: Dict[str, str] = {}
    for entry in raw.split(','):
        entry = entry.strip()
        if not entry:
            continue
        if '=' not in entry:
            Logger.instance(LOG_ID).warning(f"Ignoring invalid proxy-regular-upstream entry: {entry}")
            continue
        source, destination = entry.split('=', 1)
        source = source.strip()
        destination = destination.strip()
        if not source or not destination:
            Logger.instance(LOG_ID).warning(f"Ignoring invalid proxy-regular-upstream entry: {entry}")
            continue
        upstreams[source] = destination
    return upstreams


def apply_upstreams(flow: 'MitmproxyHTTPFlow', upstreams: Optional[Dict[str, str]] = None) -> bool:
    """
    If the request host:port matches an upstreams entry, reverse-proxy to the mapped
    upstream spec for the outbound connection. Stashes the prior host/port so
    ``restore_upstreams`` can undo the change in the response hook.
    
    Upstream spec format: http[s]://host[:port]
    Port is inferred from scheme if omitted (80 for http, 443 for https).
    """
    if not upstreams:
        return False

    if getattr(flow, 'response', None) is not None:
        return False
    
    request: 'MitmproxyRequest' = flow.request
    match_key = f"{request.host}:{request.port}"
    spec = upstreams.get(match_key)
    if not spec:
        return False

    setattr(request, _ORIGINAL_HOST_ATTR, request.host)
    setattr(request, _ORIGINAL_PORT_ATTR, request.port)
    setattr(request, _ORIGINAL_SCHEME_ATTR, request.scheme)

    # Normalize spec: ensure scheme:// prefix and infer port if omitted
    if '://' not in spec:
        spec = f"http://{spec}"
    
    reverse_proxy(request, spec, {})
    Logger.instance(LOG_ID).debug(f"Remapped {match_key} -> {spec}")
    return True


def restore_upstreams(flow: 'MitmproxyHTTPFlow') -> bool:
    """Restore host/port/scheme stashed by ``apply_upstreams``, if present."""
    request: 'MitmproxyRequest' = flow.request
    original_host = getattr(request, _ORIGINAL_HOST_ATTR, None)
    original_port = getattr(request, _ORIGINAL_PORT_ATTR, None)
    original_scheme = getattr(request, _ORIGINAL_SCHEME_ATTR, None)
    
    if original_host is None or original_port is None or original_scheme is None:
        return False

    request.scheme = original_scheme
    request.host = original_host
    request.port = original_port

    delattr(request, _ORIGINAL_SCHEME_ATTR)
    delattr(request, _ORIGINAL_HOST_ATTR)
    delattr(request, _ORIGINAL_PORT_ATTR)
    return True
