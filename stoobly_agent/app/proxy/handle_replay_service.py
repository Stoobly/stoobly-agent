import pdb

from mitmproxy.http import Request as MitmproxyRequest

from stoobly_agent.app.proxy.intercept_settings import InterceptSettings
from stoobly_agent.app.proxy.mitmproxy.request_facade import MitmproxyRequestFacade
from stoobly_agent.app.proxy.replay.context import ReplayContext
from stoobly_agent.config.constants import lifecycle_hooks, replay_policy
from stoobly_agent.lib.logger import Logger

from .utils.allowed_request_service import get_active_mode_policy
from .utils.request_handler import reverse_proxy

LOG_ID = 'HandleReplay'

def handle_request_replay(replay_context: ReplayContext):
  request: MitmproxyRequest = replay_context.flow.request
  intercept_settings: InterceptSettings = replay_context.intercept_settings

  policy = get_active_mode_policy(request, intercept_settings)
  if policy != replay_policy.NONE:
    __replay_request(replay_context)

def handle_response_replay(replay_context: ReplayContext):
    __replay_hook(lifecycle_hooks.AFTER_REPLAY, replay_context)

def __replay_request(replay_context: ReplayContext):
    request: MitmproxyRequest = replay_context.flow.request
    intercept_settings: InterceptSettings = replay_context.intercept_settings

    """
    Before replaying a request, see if the request needs to be rewritten
    """
    rewrite_rules = intercept_settings.rewrite_rules
    if len(rewrite_rules) > 0:
        request_facade = MitmproxyRequestFacade(request)
        request_facade.with_rewrite_rules(rewrite_rules).rewrite()

    upstream_url = intercept_settings.upstream_url

    #
    # Try forwarding the request to the service specified by Settings.service_url
    #
    if not upstream_url:
        raise Exception('config service_url is not set')

    Logger.instance().debug(f"{LOG_ID}:ReverseProxy:UpstreamUrl: {upstream_url}")

    __replay_hook(lifecycle_hooks.BEFORE_REPLAY, replay_context)

    reverse_proxy(request, upstream_url, {})

def __replay_hook(hook: str, replay_context: ReplayContext):
    intercept_settings: InterceptSettings = replay_context.intercept_settings

    lifecycle_hooks_module = intercept_settings.lifecycle_hooks
    if hook in lifecycle_hooks_module:
        lifecycle_hooks_module[hook](replay_context)