import errno
import os
import time
import tempfile

from mitmproxy.http import HTTPFlow as MitmproxyHTTPFlow
from mitmproxy.net.http.request import Request as MitmproxyRequest

from stoobly_agent.lib.api.agent_api import AgentApi
from stoobly_agent.lib.api.requests_resource import RequestsResource
from stoobly_agent.lib.logger import Logger
from stoobly_agent.lib.settings import Settings

from .join_request_service import join_filtered_request

AGENT_STATUSES = {
    'REQUESTS_MODIFIED': 'requests-modified'
}

LOG_ID = 'UploadRequest'
NAMESPACE_FOLDER = 'stoobly'

def inject_upload_request(api: RequestsResource, settings: Settings):
    if not settings:
        settings = Settings.instance()

    if not api:
        api = RequestsResource(settings.api_url, settings.api_key)


    return lambda flow: upload_request(api, settings, flow)


###
#
# Upon receiving a response, create the request in API for future use
#
# @param api [StooblyApi]
# @param settings [Settings.mode.mock | Settings.mode.record]
# @param res [Net::HTTP::Response]
#
def upload_request(api: RequestsResource, settings: Settings, flow: MitmproxyHTTPFlow):
    active_mode_settings = settings.active_mode_settings
    joined_request = join_filtered_request(flow, active_mode_settings)

    Logger.instance().info(f"Uploading {joined_request.proxy_request.url()}")

    raw_requests = joined_request.build()
    body_params = { 'importer': 'gor' }

    res = api.with_scenario_key(
        active_mode_settings.get('scenario_key'), body_params
    ).from_project_key(
        active_mode_settings.get('project_key'), 
        lambda project_id: api.create(
            project_id, raw_requests, body_params 
        )
    )

    Logger.instance().debug(f"{LOG_ID}:StatusCode:{res.status_code}")

    if Settings.instance().is_debug():
        __debug_request(flow.request, raw_requests)

    if not Settings.instance().is_headless() and res.status_code == 201:
        __publish_change(settings)

    return res

# Write the request to a file to help debug
def __debug_request(request: MitmproxyRequest, raw_requests: bytes):
    # Build file path, replace slashes with underscores
    request_path = request.path.replace('/', '_')
    timestamp = str(int(time.time() * 1000))
    file_path = os.path.join(tempfile.gettempdir(), NAMESPACE_FOLDER, request_path, timestamp)

    if not os.path.exists(os.path.dirname(file_path)):
        try:
            os.makedirs(os.path.dirname(file_path))
        except OSError as err: # Guard against race condition
            if err.errno != errno.EEXIST:
                raise err

    Logger.instance().debug(f"{LOG_ID}: Writing request to {file_path}")

    with open(file_path, 'wb') as f:
        f.write(raw_requests)

def __publish_change(settings):
    active_mode_settings = settings.active_mode_settings
    agent_url = settings.agent_url

    if not agent_url:
        Logger.instance().warn('Settings.agent_url not configured')
    else:
        api: AgentApi = AgentApi(agent_url)
        api.update_status(AGENT_STATUSES['REQUESTS_MODIFIED'], active_mode_settings.get('project_key'))