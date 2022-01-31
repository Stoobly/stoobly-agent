import time

from mitmproxy.http import HTTPFlow as MitmproxyHTTPFlow
from mitmproxy.net.http.request import Request as MitmproxyRequest
from mitmproxy.net.http.response import Response as MitmproxyResponse
from typing import Union

from ..logger import Logger
from ..settings import IProjectMockSettings, IProjectTestSettings, Settings
from ..stoobly_api import StooblyApi
from .allowed_request_service import allowed_request
from .custom_headers import CUSTOM_HEADERS
from .custom_response_codes import CUSTOM_RESPONSE_CODES
from .eval_request_service import eval_request
from .settings import get_mock_policy, get_service_url
from .response_handler import bad_request, pass_on, reverse_proxy

LOG_ID = 'HandleMock'
MOCK_POLICY = {
    'ALL': 'all',
    'NONE': 'none',
    'FOUND': 'found',
}

###
#
# @param request [mitmproxy.net.http.request.Request]
# @param settings [Dict]
#
def handle_request_mock_generic(
    flow: MitmproxyHTTPFlow, 
    api: StooblyApi, 
    active_mode_settings: Union[IProjectMockSettings , IProjectTestSettings], 
    **kwargs
):
    request: MitmproxyRequest = flow.request
    handle_success = kwargs['success'] if 'success' in kwargs and callable(kwargs['success']) else None
    handle_failure = kwargs['failure'] if 'failure' in kwargs and callable(kwargs['failure']) else None

    if active_mode_settings.get('enabled') and allowed_request(active_mode_settings, request):
        mock_policy = get_mock_policy(request.headers, active_mode_settings)
    else:
        # If the request path does not match accepted paths, do not mock
        mock_policy = MOCK_POLICY['NONE']

    if mock_policy == MOCK_POLICY['NONE']:
        if handle_failure:
            return handle_failure(request)
    elif mock_policy == MOCK_POLICY['ALL']:
        res = eval_request(request, api, active_mode_settings)

        if res.status_code == CUSTOM_RESPONSE_CODES['IGNORE_COMPONENTS']:
            res = eval_request(request, api, active_mode_settings, res.content)

        if handle_success:
            handle_success(request, res)
    elif mock_policy == MOCK_POLICY['FOUND']:
        res = eval_request(request, api, active_mode_settings)

        if res.status_code == CUSTOM_RESPONSE_CODES['IGNORE_COMPONENTS']:
            res = eval_request(request, api, active_mode_settings, res.content)

        if res.status_code == CUSTOM_RESPONSE_CODES['NOT_FOUND']:
            if handle_failure:
                return handle_failure(request)
        else:
            if handle_success:
                handle_success(request, res)
    else:
        return bad_request(
            flow,
            "Valid env MOCK_POLICY: %s, %s, %s, Got: %s" %
            [MOCK_POLICY['ALL'], MOCK_POLICY['FOUND'], MOCK_POLICY['NONE'], mock_policy]
        )

    return pass_on(flow, res)

def handle_request_mock(flow: MitmproxyHTTPFlow, settings: Settings):
    active_mode_settings: IProjectMockSettings = settings.active_mode_settings
    api = StooblyApi(settings.api_url, settings.api_key)
    start_time = time.time()

    handle_request_mock_generic(
        flow, api, active_mode_settings,
        failure=lambda req: __handle_mock_failure(req, active_mode_settings),
        success=lambda req, res: __handle_mock_success(req, res, start_time)
    )

def __handle_mock_success(req: MitmproxyRequest, res: MitmproxyResponse, start_time: float) -> None:
    __simulate_latency(res.headers.get(CUSTOM_HEADERS['RESPONSE_LATENCY']), start_time)

def __handle_mock_failure(req: MitmproxyRequest, active_mode_settings: IProjectMockSettings):
    service_url = get_service_url(req, active_mode_settings)
    Logger.instance().debug(f"{LOG_ID}:ReverseProxy:ServiceUrl: {service_url}")
    return reverse_proxy(req, service_url, {})

###
#
# Try to simulate expected response latency
#
# wait_time (seconds) = expected_latency - estimated_rtt_network_latency - api_latency
#
# expected_latency = provided value
# estimated_rtt_network_latency = 15ms
# api_latency = current_time - start_time of this request
#
def __simulate_latency(expected_latency: int, start_time: float) -> float:
    if not expected_latency:
        return 0

    estimated_rtt_network_latency = 0.015 # seconds
    api_latency = (time.time() - start_time)
    expected_latency = float(expected_latency) / 1000

    wait_time = expected_latency - estimated_rtt_network_latency - api_latency

    Logger.instance().debug(f"{LOG_ID}:Expected latency: {expected_latency}")
    Logger.instance().debug(f"{LOG_ID}:API latency: {api_latency}")
    Logger.instance().debug(f"{LOG_ID}:Wait time: {wait_time}")

    if wait_time > 0:
        time.sleep(wait_time)

    return wait_time
