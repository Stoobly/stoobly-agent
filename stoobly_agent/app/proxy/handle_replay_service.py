import time
import pdb

from mitmproxy.http import HTTPFlow as MitmproxyHTTPFlow
from mitmproxy.net.http.request import Request as MitmproxyRequest

from stoobly_agent.app.models.request_model import RequestModel
from stoobly_agent.app.proxy.intercept_settings import InterceptSettings
from stoobly_agent.app.proxy.mitmproxy.request_facade import MitmproxyRequestFacade
from stoobly_agent.config.constants import custom_headers, replay_policy
from stoobly_agent.lib.logger import Logger

from .constants import custom_response_codes
from .mock.context import MockContext
from .mock.eval_request_service import inject_eval_request
from .utils.allowed_request_service import allowed_request
from .utils.request_handler import reverse_proxy

LOG_ID = 'HandleReplay'

def handle_request_replay(request: MitmproxyRequest, intercept_settings: InterceptSettings):
  if intercept_settings.active and allowed_request(intercept_settings, request):
      policy = intercept_settings.policy
  else:
      # If the request path does not match accepted paths, do not mock
      policy = replay_policy.NONE

  if policy == replay_policy.ALL:
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

