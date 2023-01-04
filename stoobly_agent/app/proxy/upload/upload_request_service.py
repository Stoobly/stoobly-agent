import errno
import os
import pdb
import time
import tempfile

from mitmproxy.http import HTTPFlow as MitmproxyHTTPFlow
from mitmproxy.http import Request as MitmproxyRequest

from stoobly_agent.app.models.request_model import RequestModel
from stoobly_agent.app.proxy.intercept_settings import InterceptSettings
from stoobly_agent.app.proxy.upload import JoinedRequest, RequestString, ResponseString
from stoobly_agent.app.settings import Settings
from stoobly_agent.lib.api.param_builder import ParamBuilder
from stoobly_agent.lib.logger import Logger, bcolors

from ..utils.publish_change_service import publish_change
from .join_request_service import join_rewritten_request

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
    request_model: RequestModel, intercept_settings: InterceptSettings, flow: MitmproxyHTTPFlow = None
):
    joined_request = join_rewritten_request(flow, intercept_settings)

    if flow and intercept_settings.settings.is_debug():
        __debug_request(flow.request, joined_request.build())

    project_key = intercept_settings.project_key
    scenario_key = intercept_settings.scenario_key
    body_params = __build_body_params(
        project_key,
        joined_request, 
        flow=flow,
        scenario_key=scenario_key
    )

    return __upload_request_with_body_params(request_model, body_params)

def upload_staged_request(
    request, request_model: RequestModel, project_key: str, scenario_key: str = None
):
    response = request.response

    if not response:
        return

    request_string = RequestString(None)
    request_string.set(request.raw)
    request_string.control = request.control

    response_string = ResponseString(None, None)
    response_string.set(response.raw)
    response_string.control = response.control

    joined_request = JoinedRequest()
    joined_request.request_string = request_string
    joined_request.response_string = response_string

    body_params =__build_body_params(
        project_key,
        joined_request,
        scenario_key=scenario_key
    )

    return __upload_request_with_body_params(request_model, body_params)

def __upload_request_with_body_params(request_model: RequestModel, body_params: dict):
    joined_request: JoinedRequest = body_params.get('joined_request')

    if joined_request.proxy_request:
        Logger.instance().info(f"{bcolors.OKCYAN}Uploading{bcolors.ENDC} {joined_request.proxy_request.url()}")

    #try:
    request = request_model.create(**body_params)
    #except Exception as e:
        # If anything bad happens, just log it
    #    Logger.instance().error(e)
    #    return None

    if request:
        publish_change(AGENT_STATUSES['REQUESTS_MODIFIED'])

    return request

def __build_body_params(project_key: str, joined_request: JoinedRequest, **kwargs):
    flow: MitmproxyHTTPFlow = kwargs.get('flow')
    scenario_key = kwargs.get('scenario_key')

    body_params = ParamBuilder({ 'flow': flow, 'joined_request': joined_request })
    body_params.with_resource_scoping(project_key, scenario_key)

    return body_params.build()

# Write the request to a file to help debug
def __debug_request(request: MitmproxyRequest, raw_requests: bytes):
    # Build file path, replace slashes with underscores
    request_path = request.path.replace('/', '_')
    if len(request_path) > os.pathconf('/', 'PC_NAME_MAX'):
        request_path = f"{request_path[0:252]}..."

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