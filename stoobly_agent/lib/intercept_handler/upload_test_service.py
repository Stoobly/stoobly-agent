from mitmproxy.http import HTTPFlow as MitmproxyHTTPFlow
from requests import Response

from stoobly_agent.lib.settings import IProjectTestSettings

from ..stoobly_api import StooblyApi
from ..logger import Logger
from .join_request_service import join_request

def upload_test(
  flow: MitmproxyHTTPFlow, 
  api: StooblyApi, 
  active_mode_settings: IProjectTestSettings, 
  **kwargs
) -> Response:
    joined_request = join_request(flow, active_mode_settings)

    Logger.instance().info(f"Uploading {joined_request.proxy_request.url()}")

    raw_requests = joined_request.build()

    return api.test_create(
        active_mode_settings.get('project_key'),
        raw_requests,
        { 'scenario_key': active_mode_settings.get('scenario_key'), **kwargs }
    )
