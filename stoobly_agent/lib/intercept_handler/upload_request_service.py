import errno
import tempfile

from ..agent_api import AgentApi
from ..joined_request import JoinedRequest
from ..logger import Logger
from ..mitmproxy_request_adapter import MitmproxyRequestAdapter
from ..mitmproxy_response_adapter import MitmproxyResponseAdapter
from ..proxy_request import ProxyRequest
from ..settings import Settings
from .settings import get_service_url

AGENT_STATUSES = {
    'REQUESTS_MODIFIED': 'requests-modified'
}

LOG_ID = 'UploadRequest'
NAMESPACE_FOLDER = 'stoobly'

###
#
# Upon receiving a response, create the request in API for future use
#
# @param api [StooblyApi]
# @param settings [Settings.mode.mock | Settings.mode.record]
# @param res [Net::HTTP::Response]
#
def upload_request(flow, api, settings):
    active_mode_settings = settings.active_mode_settings
    param_filters = active_mode_settings.get('filter_patterns')

    # Adapt flow.request
    request = MitmproxyRequestAdapter(flow.request)
    request.with_param_filters(param_filters)

    # Decorate request with service_url
    service_url = get_service_url(flow.request, active_mode_settings)
    proxy_request = ProxyRequest(request, service_url)

    # Adapt flow.response
    response = MitmproxyResponseAdapter(flow.response)
    response.with_param_filters(param_filters)

    # Create JoinedRequest
    joined_request = JoinedRequest(proxy_request).with_response(response)

    Logger.instance().info(f"Uploading {proxy_request.url()}")

    raw_requests = joined_request.build()

    res = api.request_create(
        active_mode_settings.get('project_key'),
        raw_requests,
        {
            'importer': 'gor',
            'scenario_key': active_mode_settings.get('scenario_key'),
        }

    )

    Logger.instance().debug(f"{LOG_ID}:StatusCode:{res.status_code}")

    # Write the request to a file to help debug
    if Settings.instance().is_debug():
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

    if not Settings.instance().is_headless() and res.status_code == 201:
        agent_url = settings.agent_url

        if not agent_url:
            Logger.instance().warn('Settings.agent_url not configured')
        else:
            api = AgentApi(agent_url)
            api.update_status(AGENT_STATUSES['REQUESTS_MODIFIED'], active_mode_settings.get('project_key'))

    return res
