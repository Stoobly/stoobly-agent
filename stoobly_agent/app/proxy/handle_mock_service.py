import pdb

from typing import TYPE_CHECKING, Callable, TypedDict, Union

from stoobly_agent.app.proxy.handle_normalize_service import handle_request_normalize, handle_response_normalize
from stoobly_agent.app.proxy.replay.context import ReplayContext

if TYPE_CHECKING:
    from requests import Response
    from mitmproxy.http import Request as MitmproxyRequest, Response as MitmproxyResponse

from stoobly_agent.app.models.request_model import RequestModel
from stoobly_agent.app.proxy.mitmproxy.request_facade import MitmproxyRequestFacade
from stoobly_agent.app.proxy.utils.request_transformation_entry_logger import RequestTransformationEntryLogger
from stoobly_agent.app.proxy.utils.rewrite_rules_to_ignored_components_service import rewrite_rules_to_ignored_components
from stoobly_agent.config.constants import custom_headers, lifecycle_hooks, mock_policy, mode, request_origin
from stoobly_agent.lib.logger import Logger
from stoobly_agent.lib.intercepted_requests.logger import InterceptedRequestsLogger
from .constants import custom_response_codes
from .mock.context import MockContext
from .mock.eval_fixtures_service import eval_fixtures
from .mock.eval_request_service import inject_eval_request
from .utils.allowed_request_service import get_intercept_mode_policy
from .utils.request_handler import reverse_proxy
from .utils.response_handler import apply_response, bad_request, enable_cors
from .utils.rewrite import rewrite_request, rewrite_response

LOG_ID = 'Mock'

class MockOptions(TypedDict):
    failure: Callable
    ignored_components: list 
    infer: bool
    no_rewrite: bool
    policy_override: str
    success: Callable

def handle_mock_failure(context: MockContext) -> Union[None, 'MitmproxyResponse']:
    flow = context.flow
    request = flow.request
    response = flow.response

    if request.method.upper() == 'OPTIONS':
        # Default OPTIONS request to allow CORS
        enable_cors(flow)
        return flow.response

    InterceptedRequestsLogger.error("Mock failure", request=request, response=response)

def handle_mock_success(context: MockContext) -> None:
    response = context.flow.response

    if response:
        request = context.flow.request

        request_key = response.headers.get(custom_headers.MOCK_REQUEST_KEY)
        if request_key:
            RequestTransformationEntryLogger.log_mocked_response(request, request.url, request_key)
            InterceptedRequestsLogger.info("Mock success", request=request, response=response, request_key=request_key)

        fixture_path = response.headers.get(custom_headers.MOCK_FIXTURE_PATH)
        if fixture_path:
            RequestTransformationEntryLogger.log_mocked_response(request, request.url, fixture_path)
            InterceptedRequestsLogger.info("Mock success", request=request, response=response, fixture_path=fixture_path)

def handle_request_mock_generic_without_rewrite(context: MockContext, **options: MockOptions):
    options['no_rewrite'] = True
    handle_request_mock_generic(context, **options)

###
#
# 1. Rewrites mock request by default
# 2. BEFORE_MOCK gets triggered
# 3. AFTER_MOCK gets triggered
#
# @param request [mitmproxy.http.Request]
# @param settings [Dict]
#
def handle_request_mock_generic(context: MockContext, **options: MockOptions):
    handle_error = options['error'] if 'error' in options and callable(options['error']) else None
    handle_failure = options['failure'] if 'failure' in options and callable(options['failure']) else None
    handle_success = options['success'] if 'success' in options and callable(options['success']) else None
    intercept_settings = context.intercept_settings
    policy_override = options['policy_override'] if 'policy_override' in options else None
    request: MitmproxyRequest = context.flow.request
    res = None

    # If policy override is set, use it, otherwise use the intercept mode policy
    policy = policy_override or get_intercept_mode_policy(request, intercept_settings, mode.MOCK)

    if policy == mock_policy.NONE:
        if handle_error:
            res = handle_error(context)

            if res:
                apply_response(context.flow, res)
        return

    if policy not in [mock_policy.ALL, mock_policy.FOUND]:
        if handle_error:
            res = handle_error(context)

        if res:
            apply_response(context.flow, res)
        else:
            bad_request(
                context.flow,
                "Valid mock policies: %s, Got: %s" %
                ([mock_policy.ALL, mock_policy.FOUND, mock_policy.NONE], policy)
            )
        return

    if not options.get('no_rewrite'):
        __rewrite_request(context)

    __mock_hook(lifecycle_hooks.BEFORE_MOCK, context)

    # If ignore rules are set, then ignore specified request parameters
    ignore_rules = intercept_settings.ignore_rules
    if len(ignore_rules) > 0:
        request_facade = MitmproxyRequestFacade(request)
        _ignore_rules = request_facade.select_parameter_rules(ignore_rules)
        ignored_components = rewrite_rules_to_ignored_components(_ignore_rules)
        options['ignored_components'] += ignored_components if 'ignored_components' in options else ignored_components 

    request_model = RequestModel(intercept_settings.settings)
    eval_request = inject_eval_request(request_model, intercept_settings)

    if policy == mock_policy.ALL:
        res = eval_request_with_retry(context, eval_request, **options) 
    elif policy == mock_policy.FOUND:
        res = eval_request_with_retry(context, eval_request, **options) 
        
        if res.status_code == custom_response_codes.NOT_FOUND:
            try:
                return __handle_found_policy(context) # Continue proxying the request
            except RuntimeError:
                # Do nothing, return custom error response
                pass 

    flow = context.flow
    apply_response(flow, res)

    if res.status_code == custom_response_codes.NOT_FOUND:
        __mock_hook(lifecycle_hooks.AFTER_MOCK_NOT_FOUND, context)

        # If custom hook did not override resonse, continue with handle_failure
        if flow.response.status_code == custom_response_codes.NOT_FOUND and handle_failure:
            return handle_failure(context)
    
    if handle_success:
        handle_success(context)

def eval_request_with_retry(context: MockContext, eval_request, **options: MockOptions):
    request = context.flow.request
    infer = bool(options.get('infer'))
    ignored_components = options['ignored_components'] if 'ignored_components' in options else []

    res: 'Response' = eval_request(request, ignored_components)

    if res.status_code == custom_response_codes.IGNORE_COMPONENTS:
        ignored_components.append(res.content)
        res = eval_request(request, ignored_components, infer=infer, retry=1)

    if res.status_code == custom_response_codes.NOT_FOUND:
        intercept_settings = context.intercept_settings
        fixture = eval_fixtures(
            request,
            public_directory_path=intercept_settings.public_directory_path,
            response_fixtures_path=intercept_settings.response_fixtures_path
        )
        if fixture:
            res = fixture

    return res

###
# 
# 1. BEFORE_NORMALIZE gets triggered
#
def handle_request_mock(context: MockContext):
    handle_request_normalize(ReplayContext(context.flow, context.intercept_settings))
    handle_request_mock_generic(
        context,
        failure=handle_mock_failure,
        success=handle_mock_success,
    )

###
#
# Occurs if mock is found
# 1. AFTER_RESPONSE gets triggered
# 3. Rewrites mock response
# 3. AFTER_MOCK gets triggered
#
def handle_response_mock(context: MockContext):
    handle_response_normalize(ReplayContext(context.flow, context.intercept_settings))
    __rewrite_response(context)
    __mock_hook(lifecycle_hooks.AFTER_MOCK, context)

def __handle_found_policy(context: MockContext) -> None:
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

def __rewrite_request(context: MockContext):
    # Rewrite request with paramter rules for mock

    intercept_settings = context.intercept_settings
    rewrite_rules = intercept_settings.mock_rewrite_rules

    if len(rewrite_rules) > 0:
        rewrite_request(context.flow, rewrite_rules, mode=mode.MOCK) 

def __rewrite_response(context: MockContext):
    # Rewrite request with paramter rules for mock

    intercept_settings = context.intercept_settings
    rewrite_rules = intercept_settings.mock_rewrite_rules

    if len(rewrite_rules) > 0:
        rewrite_response(context.flow, rewrite_rules, mode=mode.MOCK) 

def __mock_hook(hook: str, context: MockContext):
    intercept_settings = context.intercept_settings
    lifecycle_hooks_module = intercept_settings.lifecycle_hooks

    if hook in lifecycle_hooks_module:
        lifecycle_hooks_module[hook](context)