import pdb

from mitmproxy.http import Request as MitmproxyRequest
from typing import TypedDict

from stoobly_agent.app.proxy.intercept_settings import InterceptSettings
from stoobly_agent.app.proxy.replay.context import ReplayContext
from stoobly_agent.config.constants import lifecycle_hooks, replay_policy

from .utils.allowed_request_service import get_active_mode_policy
from .utils.rewrite import rewrite_request, rewrite_response

LOG_ID = 'HandleReplay'

class ReplayOptions(TypedDict):
    no_rewrite: bool

###
#
# 1. Rewrites replay request by default
# 2. BEFORE_REPLAY gets triggered
#
def handle_request_replay_without_rewrite(replay_context: ReplayContext):
    options = { 'no_rewrite': True }
    handle_request_replay(replay_context, **options)

def handle_request_replay(replay_context: ReplayContext, **options: ReplayOptions):
    request: MitmproxyRequest = replay_context.flow.request
    intercept_settings: InterceptSettings = replay_context.intercept_settings

    policy = get_active_mode_policy(request, intercept_settings)
    if policy != replay_policy.NONE:
        if not options.get('no_rewrite'):
            __rewrite_request(replay_context)

        __replay_hook(lifecycle_hooks.BEFORE_REPLAY, replay_context)

###
#
# 1. Rewrites replay response
# 2. AFTER_REPLAY gets triggered
#
def handle_response_replay(replay_context: ReplayContext):
    __rewrite_response(replay_context)
    __replay_hook(lifecycle_hooks.AFTER_REPLAY, replay_context)

def __replay_hook(hook: str, replay_context: ReplayContext):
    intercept_settings: InterceptSettings = replay_context.intercept_settings

    lifecycle_hooks_module = intercept_settings.lifecycle_hooks
    if hook in lifecycle_hooks_module:
        lifecycle_hooks_module[hook](replay_context)

def __rewrite_request(replay_context: ReplayContext):
    """
    Before replaying a request, see if the request needs to be rewritten
    """
    intercept_settings: InterceptSettings = replay_context.intercept_settings
    rewrite_rules = intercept_settings.replay_rewrite_rules

    if len(rewrite_rules) > 0:
        rewrite_request(replay_context.flow, rewrite_rules)

def __rewrite_response(replay_context: ReplayContext):
    """
    After replaying a request, see if the request needs to be rewritten
    """
    intercept_settings: InterceptSettings = replay_context.intercept_settings
    rewrite_rules = intercept_settings.replay_rewrite_rules

    if len(rewrite_rules) > 0:
        rewrite_response(replay_context.flow, rewrite_rules)