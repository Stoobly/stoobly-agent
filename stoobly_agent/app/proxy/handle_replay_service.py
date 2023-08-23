import pdb

from mitmproxy.http import Request as MitmproxyRequest

from stoobly_agent.app.proxy.intercept_settings import InterceptSettings
from stoobly_agent.app.proxy.mitmproxy.request_facade import MitmproxyRequestFacade
from stoobly_agent.app.proxy.replay.context import ReplayContext
from stoobly_agent.config.constants import lifecycle_hooks, replay_policy

from .utils.allowed_request_service import get_active_mode_policy

LOG_ID = 'HandleReplay'

def handle_request_replay(replay_context: ReplayContext):
  __replay_hook(lifecycle_hooks.BEFORE_REPLAY, replay_context)

  request: MitmproxyRequest = replay_context.flow.request
  intercept_settings: InterceptSettings = replay_context.intercept_settings

  policy = get_active_mode_policy(request, intercept_settings)
  if policy != replay_policy.NONE:
    __replay_request(replay_context)

def handle_response_replay(replay_context: ReplayContext):
    __replay_hook(lifecycle_hooks.AFTER_REPLAY, replay_context)

def __replay_request(replay_context: ReplayContext):
    """
    Before replaying a request, see if the request needs to be rewritten
    """
    intercept_settings: InterceptSettings = replay_context.intercept_settings
    rewrite_rules = intercept_settings.rewrite_rules

    if len(rewrite_rules) > 0:
        request: MitmproxyRequest = replay_context.flow.request
        request_facade = MitmproxyRequestFacade(request)
        request_facade.with_parameter_rules(rewrite_rules).with_url_rules(rewrite_rules).rewrite()

def __replay_hook(hook: str, replay_context: ReplayContext):
    intercept_settings: InterceptSettings = replay_context.intercept_settings

    lifecycle_hooks_module = intercept_settings.lifecycle_hooks
    if hook in lifecycle_hooks_module:
        lifecycle_hooks_module[hook](replay_context)