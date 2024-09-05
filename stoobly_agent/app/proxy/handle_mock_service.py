import os
import pdb
import requests
import time

from mitmproxy.http import Request as MitmproxyRequest
from typing import Callable, TypedDict

from stoobly_agent.app.models.request_model import RequestModel
from stoobly_agent.app.proxy.mitmproxy.request_facade import MitmproxyRequestFacade
from stoobly_agent.app.proxy.utils.rewrite_rules_to_ignored_components_service import rewrite_rules_to_ignored_components
from stoobly_agent.config.constants import custom_headers, env_vars, lifecycle_hooks, mock_policy, request_origin
from stoobly_agent.lib.logger import bcolors, Logger

from .constants import custom_response_codes
from .mock.context import MockContext
from .mock.eval_fixtures_service import eval_fixtures
from .mock.eval_request_service import inject_eval_request
from .utils.allowed_request_service import get_active_mode_policy
from .utils.request_handler import reverse_proxy
from .utils.response_handler import bad_request, pass_on

LOG_ID = 'Mock'

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
    __mock_hook(lifecycle_hooks.BEFORE_MOCK, context)

    intercept_settings = context.intercept_settings
    request: MitmproxyRequest = context.flow.request
    request_model = RequestModel(intercept_settings.settings)

    policy = get_active_mode_policy(request, intercept_settings)

    rewrite_rules = intercept_settings.mock_rewrite_rules
    if len(rewrite_rules) > 0:
        # Rewrite request with paramter rules for mock
        request: MitmproxyRequest = context.flow.request
        request_facade = MitmproxyRequestFacade(request)
        request_facade.with_parameter_rules(rewrite_rules).with_url_rules(rewrite_rules).rewrite()

    # If ignore rules are set, then ignore specified request parameters
    ignore_rules = intercept_settings.ignore_rules
    if len(ignore_rules) > 0:
        request_facade = MitmproxyRequestFacade(request)
        _ignore_rules = request_facade.select_parameter_rules(ignore_rules)
        ignored_components = rewrite_rules_to_ignored_components(_ignore_rules)
        options['ignored_components'] += ignored_components  if 'ignored_components' in options else ignored_components

    handle_success = options['success'] if 'success' in options and callable(options['success']) else None
    handle_failure = options['failure'] if 'failure' in options and callable(options['failure']) else None
    
    eval_request = inject_eval_request(request_model, intercept_settings)
 
    if policy == mock_policy.NONE:
        if handle_failure:
            res = handle_failure(context)
    elif policy == mock_policy.ALL:
        res = eval_request_with_retry(context, eval_request, **options) 

        context.with_response(res)

        if handle_success:
            res = handle_success(context) or res
    elif policy == mock_policy.FOUND:
        res = eval_request_with_retry(context, eval_request, **options) 

        context.with_response(res)

        if res.status_code in [custom_response_codes.NOT_FOUND, custom_response_codes.IGNORE_COMPONENTS]:
            if handle_failure:
                try:
                    res = handle_failure(context)
                except RuntimeError:
                    # Do nothing, return custom error response
                    pass
        else:
            if handle_success:
                res = handle_success(context) or res
    else:
        return bad_request(
            context.flow,
            "Valid env MOCK_POLICY: %s, Got: %s" %
            ([mock_policy.ALL, mock_policy.FOUND, mock_policy.NONE], policy)
        )

    __mock_hook(lifecycle_hooks.AFTER_MOCK, context)

    return pass_on(context.flow, res)

def eval_request_with_retry(context: MockContext, eval_request, **options: MockOptions):
    request = context.flow.request
    infer = bool(options.get('infer'))
    ignored_components = options['ignored_components'] if 'ignored_components' in options else []

    res: requests.Response = eval_request(request, ignored_components)

    if res.status_code == custom_response_codes.IGNORE_COMPONENTS:
        ignored_components.append(res.content)
        res = eval_request(request, ignored_components, infer=infer, retry=1)

    if res.status_code == custom_response_codes.NOT_FOUND:
        intercept_settings = context.intercept_settings
        fixture = eval_fixtures(
            request,
            public_directory_path=intercept_settings.public_directory_path,
            response_fixtures=intercept_settings.response_fixtures
        )
        if fixture:
            res = fixture

    return res

def handle_request_mock(context: MockContext):
    handle_request_mock_generic(
        context,
        failure=lambda context: __handle_mock_failure(context),
        success=lambda context: __handle_mock_success(context)
    )

def handle_response_mock(context: MockContext):
    response = context.flow.response
    request_key = response.headers.get(custom_headers.MOCK_REQUEST_KEY)

    if request_key:
        request = context.flow.request
        Logger.instance(LOG_ID).info(f"{bcolors.OKCYAN}Mocked{bcolors.ENDC} {request.url} -> {request_key}")

def __handle_mock_success(context: MockContext) -> None:
    if os.environ.get(env_vars.AGENT_SIMULATE_LATENCY):
        response = context.response
        start_time = context.start_time
        __simulate_latency(response.headers.get(custom_headers.RESPONSE_LATENCY), start_time)

def __handle_mock_failure(context: MockContext) -> None:
    req = context.flow.request
    intercept_settings = context.intercept_settings
    upstream_url = intercept_settings.upstream_url

    if req.headers.get(custom_headers.REQUEST_ORIGIN) == request_origin.PROXY:
        # If this header is set, then it is likely that we are going to infinite loop
        # Unless we stop sending the same request
        raise RuntimeError(f"Request originated from {request_origin.PROXY}")
    else:
        req.headers[custom_headers.REQUEST_ORIGIN] = request_origin.PROXY

    Logger.instance(LOG_ID).debug(f"UpstreamUrl: {upstream_url}")

    reverse_proxy(req, upstream_url, {})

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

    Logger.instance(LOG_ID).debug(f"Expected latency: {expected_latency}")
    Logger.instance(LOG_ID).debug(f"API latency: {api_latency}")
    Logger.instance(LOG_ID).debug(f"Wait time: {wait_time}")

    if wait_time > 0:
        time.sleep(wait_time)

    return wait_time

def __mock_hook(hook: str, context: MockContext):
    intercept_settings = context.intercept_settings
    lifecycle_hooks_module = intercept_settings.lifecycle_hooks

    if hook in lifecycle_hooks_module:
        lifecycle_hooks_module[hook](context)