import errno
import os
import pdb
import time
import tempfile

from mitmproxy.http import HTTPFlow as MitmproxyHTTPFlow
from mitmproxy.net.http.request import Request as MitmproxyRequest

from stoobly_agent.app.models.request_model import RequestModel
from stoobly_agent.app.proxy.intercept_settings import InterceptSettings
from stoobly_agent.app.settings import Settings
from stoobly_agent.lib.api.param_builder import ParamBuilder
from stoobly_agent.lib.logger import Logger

from ..utils.publish_change_service import publish_change
from .join_request_service import join_redacted_request

AGENT_STATUSES = {
    'REQUESTS_MODIFIED': 'requests-modified'
}

LOG_ID = 'UploadRequest'
NAMESPACE_FOLDER = 'stoobly'

def inject_upload_request(request_model: RequestModel, intercept_settings: InterceptSettings):
    settings = Settings.instance()

    if not request_model:
        request_model = RequestModel(settings)

    if not intercept_settings:
        intercept_settings = InterceptSettings(settings)

    return lambda flow: upload_request(request_model, intercept_settings, flow)

###
#
# Upon receiving a response, create the request in API for future use
#
# @param request_model [StooblyApi]
# @param settings [Settings.mode.mock | Settings.mode.record]
# @param res [Net::HTTP::Response]
#
def upload_request(
    request_model: RequestModel, intercept_settings: InterceptSettings, flow: MitmproxyHTTPFlow
):
    joined_request = join_redacted_request(flow, intercept_settings)

    Logger.instance().info(f"Uploading {joined_request.proxy_request.url()}")

    if intercept_settings.settings.is_debug():
        __debug_request(flow.request, joined_request.build())

    body_params = ParamBuilder({ 'flow': flow, 'joined_request': joined_request })
    body_params.with_resource_scoping(intercept_settings)

    #try:
    request = request_model.create(**body_params.build())
    #except Exception as e:
        # If anything bad happens, just log it
    #    Logger.instance().error(e)
    #    return None

    if request:
        publish_change(AGENT_STATUSES['REQUESTS_MODIFIED'])

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

