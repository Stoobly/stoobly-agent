import time
import pdb

from mitmproxy.http import HTTPFlow as MitmproxyHTTPFlow
from mitmproxy.net.http.request import Request as MitmproxyRequest

from stoobly_agent.app.models.request_model import RequestModel
from stoobly_agent.app.proxy.intercept_settings import InterceptSettings
from stoobly_agent.config.constants import custom_headers, mock_policy
from stoobly_agent.lib.logger import Logger

from .constants import custom_response_codes
from .mock.context import MockContext
from .mock.eval_request_service import inject_eval_request
from .utils.allowed_request_service import allowed_request
from .utils.request_handler import reverse_proxy
from .utils.response_handler import bad_request, pass_on

LOG_ID = 'HandleMock'

###
#
# @param request [mitmproxy.net.http.request.Request]
# @param settings [Dict]
#
def handle_request_mock_generic(context: MockContext, **kwargs):
    request_model: RequestModel = context.model
    intercept_settings = context.intercept_settings
    request: MitmproxyRequest = context.flow.request

    eval_request = inject_eval_request(request_model, intercept_settings)
    handle_success = kwargs['success'] if 'success' in kwargs and callable(kwargs['success']) else None
    handle_failure = kwargs['failure'] if 'failure' in kwargs and callable(kwargs['failure']) else None

    if intercept_settings.active and allowed_request(intercept_settings, request):
        policy = intercept_settings.policy
    else:
        # If the request path does not match accepted paths, do not mock
        policy = mock_policy.NONE
 
    if policy == mock_policy.NONE:
        if handle_failure:
            res = handle_failure(context)
    elif policy == mock_policy.ALL:
        ignored_components = kwargs['ignored_components'] if 'ignored_components' in kwargs else []

        res = eval_request(request, ignored_components)

        if res.status_code == custom_response_codes.IGNORE_COMPONENTS:
            ignored_components.append(res.content)
            res = eval_request(request, [res.content] + ignored_components)

        context.with_response(res)

        if handle_success:
            res = handle_success(context) or res
    elif policy == mock_policy.FOUND:
        ignored_components = kwargs['ignored_components'] if 'ignored_components' in kwargs else []
        res = eval_request(request, ignored_components)

        if res.status_code == custom_response_codes.IGNORE_COMPONENTS:
            ignored_components.append(res.content)
            res = eval_request(request, ignored_components)
        
        context.with_response(res)

        if res.status_code == custom_response_codes.NOT_FOUND:
            if handle_failure:
                res = handle_failure(context)
        else:
            if handle_success:
                res = handle_success(context) or res
    else:
        return bad_request(
            context.flow,
            "Valid env MOCK_POLICY: %s, %s, %s, Got: %s" %
            [mock_policy.ALL, mock_policy.FOUND, mock_policy]
        )

    return pass_on(context.flow, res)

def handle_request_mock(flow: MitmproxyHTTPFlow, intercept_settings: InterceptSettings):
    request_model = RequestModel(intercept_settings.settings)
    context = MockContext(flow, intercept_settings).with_model(request_model)

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
    intercept_settings = context.intercept_settings
    upstream_url = intercept_settings.upstream_url

    Logger.instance().debug(f"{LOG_ID}:ReverseProxy:UpstreamUrl: {upstream_url}")

    return reverse_proxy(req, upstream_url, {})

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
