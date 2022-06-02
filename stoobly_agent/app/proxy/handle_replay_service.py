import time
import pdb

from mitmproxy.net.http.request import Request as MitmproxyRequest

from stoobly_agent.app.proxy.intercept_settings import InterceptSettings
from stoobly_agent.app.proxy.mitmproxy.request_facade import MitmproxyRequestFacade
from stoobly_agent.config.constants import replay_policy
from stoobly_agent.lib.logger import Logger

from .utils.allowed_request_service import get_active_mode_policy
from .utils.request_handler import reverse_proxy

LOG_ID = 'HandleReplay'

def handle_request_replay(request: MitmproxyRequest, intercept_settings: InterceptSettings):
  policy = get_active_mode_policy(request, intercept_settings)

  if policy != replay_policy.NONE:
    replay_request(request, intercept_settings)

def replay_request(request: MitmproxyRequest, intercept_settings: InterceptSettings):
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

    reverse_proxy(request, upstream_url, {})

