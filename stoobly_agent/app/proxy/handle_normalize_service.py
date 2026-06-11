from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from mitmproxy.http import Request as MitmproxyRequest

from stoobly_agent.app.proxy.intercept_settings import InterceptSettings
from stoobly_agent.app.proxy.replay.context import ReplayContext
from stoobly_agent.config.constants import lifecycle_hooks, normalize_policy, mode
from stoobly_agent.lib.intercepted_requests.logger import InterceptedRequestsLogger

from .utils.allowed_request_service import get_intercept_mode_policy
from .utils.request_transformation_entry_logger import RequestTransformationEntryLogger
from .utils.rewrite import rewrite_request, rewrite_response

class NormalizeOptions(TypedDict):
    no_rewrite: bool

###
#
# 1. Rewrites normalize request by default
# 2. BEFORE_NORMALIZE gets triggered
#
def handle_request_normalize_without_rewrite(replay_context: ReplayContext):
    options = { 'no_rewrite': True }
    handle_request_normalize(replay_context, **options)

def handle_request_normalize(replay_context: ReplayContext, **options: NormalizeOptions):
    request: 'MitmproxyRequest' = replay_context.flow.request
    intercept_settings: InterceptSettings = replay_context.intercept_settings

    policy = get_intercept_mode_policy(request, intercept_settings, mode.NORMALIZE)
    if policy != normalize_policy.NONE:
        if not options.get('no_rewrite'):
            __rewrite_request(replay_context)

        __normalize_hook(lifecycle_hooks.BEFORE_NORMALIZE, replay_context)

###
#
# 1. Rewrites normalize response
# 2. AFTER_NORMALIZE gets triggered
#
def handle_response_normalize(replay_context: ReplayContext) -> str:
    request: 'MitmproxyRequest' = replay_context.flow.request
    intercept_settings: InterceptSettings = replay_context.intercept_settings

    policy = get_intercept_mode_policy(request, intercept_settings, mode.NORMALIZE)
    if policy != normalize_policy.NONE:
        __rewrite_response(replay_context)
        __normalize_hook(lifecycle_hooks.AFTER_NORMALIZE, replay_context)

    return policy

###
#
# Called when normalize is the active proxy mode, not as a sub-step of record.
# Wraps handle_response_normalize and writes to the request log.
#
def handle_response_normalize_primary(replay_context: ReplayContext):
    policy = handle_response_normalize(replay_context)

    if policy != normalize_policy.NONE:
        flow = replay_context.flow
        RequestTransformationEntryLogger.log_normalizing(flow.request, flow.request.url)
        response = flow.response
        if response is not None:
            InterceptedRequestsLogger.info("Normalize success", request=flow.request, response=response)
        else:
            InterceptedRequestsLogger.error("Normalize failure", request=flow.request, response=response)

def __normalize_hook(hook: str, replay_context: ReplayContext):
    intercept_settings: InterceptSettings = replay_context.intercept_settings

    lifecycle_hooks_module = intercept_settings.lifecycle_hooks
    if hook in lifecycle_hooks_module:
        lifecycle_hooks_module[hook](replay_context)

def __rewrite_request(replay_context: ReplayContext):
    """
    Before normalizing a request, see if the request needs to be rewritten
    """
    intercept_settings: InterceptSettings = replay_context.intercept_settings
    rewrite_rules = intercept_settings.normalize_rewrite_rules

    if len(rewrite_rules) > 0:
        rewrite_request(replay_context.flow, rewrite_rules, mode=mode.NORMALIZE)

def __rewrite_response(replay_context: ReplayContext):
    """
    After normalizing a request, see if the request needs to be rewritten
    """
    intercept_settings: InterceptSettings = replay_context.intercept_settings
    flow = replay_context.flow

    rewrite_rules = intercept_settings.normalize_rewrite_rules

    if len(rewrite_rules) > 0:
        rewrite_response(flow, rewrite_rules, mode=mode.NORMALIZE)
