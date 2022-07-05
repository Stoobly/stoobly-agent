import requests
import time
import pdb

from mitmproxy.http import HTTPFlow as MitmproxyHTTPFlow
from mitmproxy.http import Request as MitmproxyRequest
from typing import Callable, TypedDict

from stoobly_agent.app.models.request_model import RequestModel
from stoobly_agent.app.proxy.intercept_settings import InterceptSettings
from stoobly_agent.app.proxy.mitmproxy.request_facade import MitmproxyRequestFacade
from stoobly_agent.app.proxy.utils.rewrite_rules_to_ignored_components_service import rewrite_rules_to_ignored_components
from stoobly_agent.app.settings import intercept_settings
from stoobly_agent.config.constants import custom_headers, mock_policy
from stoobly_agent.lib.logger import Logger

from .constants import custom_response_codes
from .mock.context import MockContext
from .mock.eval_request_service import inject_eval_request
from .utils.allowed_request_service import get_active_mode_policy
from .utils.request_handler import reverse_proxy
from .utils.response_handler import bad_request, pass_on

LOG_ID = 'HandleMock'

class MockOptions(TypedDict):
    failure: Callable
    ignored_components: list 
    infer: bool
    success: Callable

###
#
# @param request [mitmproxy.http.Request]
# @param settings [Dict]
#
def handle_request_mock_generic(context: MockContext, **options: MockOptions):
    intercept_settings = context.intercept_settings
    request_model = RequestModel(intercept_settings.settings)
    request: MitmproxyRequest = context.flow.request

    # Rewrite request with paramter rules for mock
    request_facade = MitmproxyRequestFacade(request)
    rewrite_rules = intercept_settings.rewrite_rules
    request_facade.with_rewrite_rules(rewrite_rules).rewrite()

    # If ignore rules are set, then ignore specified request parameters
    ignore_rules = intercept_settings.ignore_rules
    if len(ignore_rules) > 0:
        _ignore_rules = request_facade.select_parameter_rules(ignore_rules)
        ignored_components = rewrite_rules_to_ignored_components(_ignore_rules)
        options['ignored_components'] += ignored_components  if 'ignored_components' in options else ignored_components

    handle_success = options['success'] if 'success' in options and callable(options['success']) else None
    handle_failure = options['failure'] if 'failure' in options and callable(options['failure']) else None
    
    eval_request = inject_eval_request(request_model, intercept_settings)
    policy = get_active_mode_policy(request, intercept_settings)
 
    if policy == mock_policy.NONE:
        if handle_failure:
            res = handle_failure(context)
    elif policy == mock_policy.ALL:
        res = eval_request_with_retry(eval_request, request, **options) 

        context.with_response(res)

        if handle_success:
            res = handle_success(context) or res
    elif policy == mock_policy.FOUND:
        res = eval_request_with_retry(eval_request, request, **options) 

        context.with_response(res)

        if res.status_code in [custom_response_codes.NOT_FOUND, custom_response_codes.IGNORE_COMPONENTS]:
            if handle_failure:
                res = handle_failure(context)
        else:
            if handle_success:
                res = handle_success(context) or res
    else:
        return bad_request(
            context.flow,
            "Valid env MOCK_POLICY: %s, %s, %s, Got: %s" %
            [mock_policy.ALL, mock_policy.FOUND, policy]
        )

    return pass_on(context.flow, res)

def eval_request_with_retry(eval_request, request, **options: MockOptions):
    infer = bool(options.get('infer'))
    ignored_components = options['ignored_components'] if 'ignored_components' in options else []

    res: requests.Response = eval_request(request, ignored_components)

    if res.status_code == custom_response_codes.IGNORE_COMPONENTS:
        ignored_components.append(res.content)
        res = eval_request(request, ignored_components, infer=infer, retry=1)

    return res

def handle_request_mock(context: MockContext):
    handle_request_mock_generic(
        context,
        failure=lambda context: __handle_mock_failure(context),
        success=lambda context: __handle_mock_success(context)
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
