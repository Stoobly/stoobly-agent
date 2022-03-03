import time
import pdb

from mitmproxy.http import HTTPFlow as MitmproxyHTTPFlow
from mitmproxy.net.http.request import Request as MitmproxyRequest

from ..api.requests_resource import RequestsResource
from ..constants import custom_headers
from ..logger import Logger
from ..settings import IProjectMockSettings, Settings
from .constants import custom_response_codes, mock_policy
from .mock.context import MockContext
from .mock.eval_request_service import inject_eval_request
from .settings import is_proxy_enabled, get_mock_policy, get_service_url, is_proxy_enabled
from .utils.allowed_request_service import allowed_request
from .utils.response_handler import bad_request, pass_on, reverse_proxy

LOG_ID = 'HandleMock'

###
#
# @param request [mitmproxy.net.http.request.Request]
# @param settings [Dict]
#
def handle_request_mock_generic(context: MockContext, **kwargs):
    api: RequestsResource = context.api
    active_mode_settings = context.active_mode_settings
    flow = context.flow
    request: MitmproxyRequest = flow.request

    eval_request = inject_eval_request(api, active_mode_settings)
    handle_success = kwargs['success'] if 'success' in kwargs and callable(kwargs['success']) else None
    handle_failure = kwargs['failure'] if 'failure' in kwargs and callable(kwargs['failure']) else None

    if is_proxy_enabled(request.headers, active_mode_settings) and allowed_request(active_mode_settings, request):
        policy = get_mock_policy(request.headers, active_mode_settings)
    else:
        # If the request path does not match accepted paths, do not mock
        policy = mock_policy.NONE

    if policy == mock_policy.NONE:
        if handle_failure:
            return handle_failure(context)
    elif policy == mock_policy.ALL:
        ignored_components = [kwargs['ignored_components'] if 'ignored_components' in kwargs else []] 

        res = eval_request(request, ignored_components)

        if res.status_code == custom_response_codes.IGNORE_COMPONENTS:
            ignored_components.append(res.content)
            res = eval_request(request, [res.content] + ignored_components)

        context.with_response(res)

        if handle_success:
            handle_success(context)
    elif policy == mock_policy.FOUND:
        ignored_components = [kwargs['ignored_components'] if 'ignored_components' in kwargs else None]
        res = eval_request(request, ignored_components)

        if res.status_code == custom_response_codes.IGNORE_COMPONENTS:
            ignored_components.append(res.content)
            res = eval_request(request, ignored_components)
        
        context.with_response(res)

        if res.status_code == custom_response_codes.NOT_FOUND:
            if handle_failure:
                return handle_failure(context)
        else:
            if handle_success:
                handle_success(context)
    else:
        return bad_request(
            flow,
            "Valid env MOCK_POLICY: %s, %s, %s, Got: %s" %
            [mock_policy.ALL, mock_policy.FOUND, mock_policy.NONE, mock_policy]
        )

    return pass_on(flow, res)

def handle_request_mock(flow: MitmproxyHTTPFlow, settings: Settings):
    active_mode_settings: IProjectMockSettings = settings.active_mode_settings
    api = RequestsResource(settings.api_url, settings.api_key)
    context = MockContext(flow, active_mode_settings).with_api(api)

    handle_request_mock_generic(
        context,
        failure=__handle_mock_failure,
        success=__handle_mock_success
    )

def __handle_mock_success(context: MockContext) -> None:
    response = context.response
    start_time = context.start_time
    __simulate_latency(response.headers.get(custom_headers.RESPONSE_LATENCY), start_time)

def __handle_mock_failure(context: MockContext):
    req = context.flow.request
    active_mode_settings = context.active_mode_settings
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
def __simulate_latency(expected_latency: str, start_time: float) -> float:
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
