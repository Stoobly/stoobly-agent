import pdb
import threading

from mitmproxy.http import HTTPFlow as MitmproxyHTTPFlow
from mitmproxy.net.http.request import Request as MitmproxyRequest
from mitmproxy.net.http.response import Response as MitmproxyResponse 

from stoobly_agent.app.models.request_model import RequestModel
from ...config.constants import record_policy
from stoobly_agent.lib.logger import Logger
from stoobly_agent.app.settings import Settings
from stoobly_agent.app.settings.types import IProjectRecordSettings

from .constants import custom_response_codes
from .mock.eval_request_service import inject_eval_request
from .settings import get_record_policy, get_service_url
from .upload.upload_request_service import inject_upload_request
from .utils.allowed_request_service import allowed_request
from .utils.response_handler import bad_request, reverse_proxy

LOG_ID = 'HandleRecord'

def handle_request_record(request: MitmproxyRequest, settings: Settings):
    active_mode_settings: IProjectRecordSettings = settings.active_mode_settings

    service_url = get_service_url(request, active_mode_settings)

    #
    # Try forwarding the request to the service specified by Settings.service_url
    #
    if not service_url:
        raise Exception('config service_url is not set')

    Logger.instance().debug(f"{LOG_ID}:ReverseProxy:ServiceUrl: {service_url}")

    reverse_proxy(request, service_url, {})

def handle_response_record(flow: MitmproxyHTTPFlow, settings: Settings):
    __disable_transfer_encoding(flow.response)

    request_model = RequestModel(settings)
    active_mode_settings: IProjectRecordSettings = settings.active_mode_settings
    request: MitmproxyRequest = flow.request
    upload_policy = __get_upload_policy(request, active_mode_settings)

    Logger.instance().debug(f"{LOG_ID}:UploadPolicy: {upload_policy}")

    if upload_policy == record_policy.ALL:
        __upload_request(request_model, active_mode_settings, flow)
    elif upload_policy == record_policy.NOT_FOUND:
        res = inject_eval_request(request_model, active_mode_settings)(request, [])

        if res.status_code == custom_response_codes.NOT_FOUND:
            __upload_request(request_model, active_mode_settings, flow)
    elif upload_policy == record_policy.NONE:
        pass
    else:
        return bad_request(
            flow,
            "Valid env RECORD_POLICY: %s, %s, %s, Got: %s" %
            [record_policy.ALL, record_policy.NOT_FOUND, record_policy.NONE, upload_policy]
        )

def __upload_request(request_model: RequestModel, active_mode_settings: IProjectRecordSettings, flow: MitmproxyHTTPFlow):
    thread = threading.Thread(
        target=inject_upload_request(request_model, active_mode_settings), 
        args=[flow]
    )
    thread.start()

def __get_upload_policy(request: MitmproxyRequest, active_mode_settings: IProjectRecordSettings):
    if active_mode_settings.get('enabled') and allowed_request(active_mode_settings, request):
        return get_record_policy(request.headers, active_mode_settings)
    else:
        # If the request path does not match accepted paths, do not record
        return record_policy.NONE

def __disable_transfer_encoding(response: MitmproxyResponse):
    header_name = 'Transfer-Encoding'
    if header_name in response.headers and response.headers[header_name] == 'chunked':
        # Without deleting this header, causes caller to stall
        del response.headers['Transfer-Encoding']
