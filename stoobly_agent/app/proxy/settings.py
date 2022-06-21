from mitmproxy.http import Request as MitmproxyRequest
from typing import Union
from ...config.constants import mock_policy, record_policy

from stoobly_agent.config.constants import custom_headers
from stoobly_agent.app.settings import Settings
from stoobly_agent.app.settings.types import IProjectModeSettings

from ...config.constants import mode

def get_project_key(headers: MitmproxyRequest.headers, settings: IProjectModeSettings) -> str:
    if custom_headers.PROJECT_KEY in headers:
        return headers[custom_headers.PROJECT_KEY]

    return settings.get('project_key')

def get_report_key(headers: MitmproxyRequest.headers) -> Union[str, None]:
    return headers.get(custom_headers.REPORT_KEY)

def get_scenario_key(headers: MitmproxyRequest.headers, settings: IProjectModeSettings) -> str:
    if custom_headers.SCENARIO_KEY in headers:
        return headers[custom_headers.SCENARIO_KEY]

    return settings.get('scenario_key')

def is_proxy_enabled(headers: MitmproxyRequest.headers, settings: IProjectModeSettings) -> bool:
    return settings.get('enabled') or custom_headers.PROXY_MODE in headers

def get_proxy_mode(headers: MitmproxyRequest.headers, settings: Settings) -> str:
    access_control_header =  'Access-Control-Request-Headers'
    do_proxy_header = custom_headers.DO_PROXY

    if access_control_header in headers and do_proxy_header.lower() in headers[access_control_header]:
        return mode.NONE
    elif do_proxy_header in headers:
        return mode.NONE
    elif custom_headers.PROXY_MODE in headers:
        return headers[custom_headers.PROXY_MODE]
    else:
        return settings.proxy.intercept.active

def get_mock_policy(headers: MitmproxyRequest.headers, settings: IProjectModeSettings) -> str:
    if custom_headers.MOCK_POLICY in headers:
        return headers[custom_headers.MOCK_POLICY]
    else:
        return settings.get('policy') or mock_policy.FOUND

def get_record_policy(headers: MitmproxyRequest.headers, settings: Settings) -> str:
    if custom_headers.RECORD_POLICY in headers:
        return headers[custom_headers.RECORD_POLICY]
    else:
        return settings.get('policy') or record_policy.ALL

def get_service_url(request: MitmproxyRequest, settings: IProjectModeSettings) -> str:
    service_url = request.headers.get(custom_headers.SERVICE_URL)

    if service_url:
        return service_url
    else:
        if settings.up and len(settings.get('service_url')) > 0:
            return settings.get('service_url')

        return __upstream_url(request)

def __upstream_url(request: MitmproxyRequest) -> str:
    return f"{request.scheme}://{request.host}:{request.port}"
