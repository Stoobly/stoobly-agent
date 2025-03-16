import errno
import os
import pdb
import time
import tempfile

from mitmproxy.http import HTTPFlow as MitmproxyHTTPFlow
from mitmproxy.http import Request as MitmproxyRequest

from stoobly_agent.app.models.request_model import RequestModel
from stoobly_agent.app.proxy.intercept_settings import InterceptSettings
from stoobly_agent.app.proxy.record import JoinedRequest, RequestString, ResponseString
from stoobly_agent.app.settings import Settings
from stoobly_agent.config.constants import request_origin
from stoobly_agent.lib.api.param_builder import ParamBuilder
from stoobly_agent.lib.logger import Logger, bcolors
from stoobly_agent.lib.orm.request import Request

from ..utils.publish_change_service import publish_requests_modified
from .join_request_service import join_request_from_flow

AGENT_STATUSES = {
    'REQUESTS_MODIFIED': 'requests-modified'
}

LOG_ID = 'Record'
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
    Logger.instance(LOG_ID).info(f"{bcolors.OKCYAN}Recording{bcolors.ENDC} {flow.request.url}")

    joined_request = join_request_from_flow(flow, intercept_settings)

    project_key = intercept_settings.project_key
    scenario_key = intercept_settings.scenario_key
    body_params = __build_body_params(
        project_key,
        joined_request, 
        flow=flow,
        scenario_key=scenario_key
    )

    # If request_origin is WEB, then we are in proxy
    # This means that we have access to Cache singleton and do not need send a request to update the status
    sync = intercept_settings.request_origin == request_origin.WEB 
    res = __upload_request_with_body_params(request_model, body_params, sync)
 
    if intercept_settings.settings.is_debug():
        file_path = __debug_request(flow.request, joined_request.build())
        Logger.instance(LOG_ID).debug(f"Writing request to {file_path}")
    elif not res:
        file_path = __debug_request(flow.request, joined_request.build())
        Logger.instance(LOG_ID).error(f"Error: Failed to upload, writing request to {file_path}")

    return res

def upload_staged_request(
    request: Request, request_model: RequestModel, project_key: str, scenario_key: str = None
):
    Logger.instance(LOG_ID).info(f"{bcolors.OKCYAN}Recording{bcolors.ENDC} {request.url}")

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

def __upload_request_with_body_params(request_model: RequestModel, body_params: dict, sync=True):
    request, status = request_model.create(**body_params)

    if status < 400:
        publish_requests_modified(body_params['project_id'], sync=sync)

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

    with open(file_path, 'wb') as f:
        f.write(raw_requests)

    return file_path