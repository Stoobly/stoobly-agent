from mitmproxy.net.http.request import Request as MitmproxyRequest

from ..settings import Settings
from .constants.mock_policy import MOCK_POLICY
from .constants.record_policy import RECORD_POLICY
from .constants.custom_headers import CUSTOM_HEADERS
from .constants.modes import MODES

def get_proxy_mode(headers: MitmproxyRequest.headers, settings: Settings) -> str:
    access_control_header =  'Access-Control-Request-Headers'
    do_proxy_header = CUSTOM_HEADERS['DO_PROXY']

    if access_control_header in headers and do_proxy_header.lower() in headers[access_control_header]:
        return MODES['NONE']
    elif do_proxy_header in headers:
        return MODES['NONE']
    elif CUSTOM_HEADERS['PROXY_MODE'] in headers:
        return headers[CUSTOM_HEADERS['PROXY_MODE']]
    else:
        return settings.active_mode

def get_mock_policy(headers: MitmproxyRequest.headers, settings: Settings) -> str:
    if CUSTOM_HEADERS['MOCK_POLICY'] in headers:
        return headers[CUSTOM_HEADERS['MOCK_POLICY']]
    else:
        return settings.get('policy') or MOCK_POLICY['FOUND']

def get_record_policy(headers: MitmproxyRequest.headers, settings: Settings) -> str:
    if CUSTOM_HEADERS['RECORD_POLICY'] in headers:
        return headers[CUSTOM_HEADERS['RECORD_POLICY']]
    else:
        return settings.get('policy') or RECORD_POLICY['ALL']

def get_service_url(request: MitmproxyRequest, settings: Settings) -> str:
    service_url = request.headers.get(CUSTOM_HEADERS['SERVICE_URL'])

    if service_url:
        return service_url
    else:
        if settings.get('service_url') and len(settings.get('service_url')) > 0:
            return settings.get('service_url')

        return __upstream_url(request)

def __upstream_url(request: MitmproxyRequest) -> str:
    return f"{request.scheme}://{request.host}:{request.port}"
