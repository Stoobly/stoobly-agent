import errno
import os
import time
import tempfile

from mitmproxy.http import HTTPFlow as MitmproxyHTTPFlow
from mitmproxy.net.http.request import Request as MitmproxyRequest

from stoobly_agent.lib.api.agent_api import AgentApi
from stoobly_agent.lib.api.keys.project_key import ProjectKey
from stoobly_agent.lib.api.keys.scenario_key import ScenarioKey
from stoobly_agent.lib.models.request_model import RequestModel

from stoobly_agent.lib.logger import Logger
from stoobly_agent.lib.settings import Settings

from .join_request_service import join_filtered_request

AGENT_STATUSES = {
    'REQUESTS_MODIFIED': 'requests-modified'
}

LOG_ID = 'UploadRequest'
NAMESPACE_FOLDER = 'stoobly'

def inject_upload_request(request_model: RequestModel, settings: Settings):
    if not settings:
        settings = Settings.instance()

    if not request_model:
        request_model = RequestModel(settings)

    return lambda flow: upload_request(request_model, settings, flow)

###
#
# Upon receiving a response, create the request in API for future use
#
# @param request_model [StooblyApi]
# @param settings [Settings.mode.mock | Settings.mode.record]
# @param res [Net::HTTP::Response]
#
def upload_request(request_model: RequestModel, settings: Settings, flow: MitmproxyHTTPFlow):
    active_mode_settings = settings.active_mode_settings
    joined_request = join_filtered_request(flow, active_mode_settings)

    Logger.instance().info(f"Uploading {joined_request.proxy_request.url()}")

    project_id = None
    raw_requests = joined_request.build()
    body_params = { 'importer': 'gor' }

    if Settings.instance().is_debug():
        __debug_request(flow.request, raw_requests)

    # Try to see if a scenario is set, otherwise use project
    scenario_key = ScenarioKey(active_mode_settings.get('scenario_key'))
    if scenario_key:
        body_params['scenario_id'] = scenario_key.id
        project_id = scenario_key.project_id
    else:
        project_key = ProjectKey(active_mode_settings.get('project_key'))
        project_id = project_key.id

    try:
        request = request_model.create(project_id, raw_requests, body_params)
    except Exception as e:
        # If anything bad happens, just log it
        Logger.instance().error(e)
        return None

    if not Settings.instance().is_headless() and request:
        __publish_change(settings)

    return request

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

# Announce that a new request has been created
def __publish_change(settings):
    active_mode_settings = settings.active_mode_settings
    agent_url = settings.agent_url

    if not agent_url:
        Logger.instance().warn('Settings.agent_url not configured')
    else:
        request_model: AgentApi = AgentApi(agent_url)
        request_model.update_status(AGENT_STATUSES['REQUESTS_MODIFIED'], active_mode_settings.get('project_key'))