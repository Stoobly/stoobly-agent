import threading

from mitmproxy.http import HTTPFlow as MitmproxyHTTPFlow
from mitmproxy.net.http.request import Request as MitmproxyRequest
from mitmproxy.net.http.response import Response as MitmproxyResponse 

from ..logger import Logger
from ..settings import IProjectRecordSettings, Settings
from ..stoobly_api import StooblyApi
from .allowed_request_service import allowed_request
from .constants.record_policy import RECORD_POLICY
from .constants.custom_response_codes import CUSTOM_RESPONSE_CODES
from .eval_request_service import eval_request
from .response_handler import bad_request, reverse_proxy
from .settings import get_record_policy, get_service_url
from .upload.upload_request_service import upload_request

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

    request: MitmproxyRequest = flow.request

    active_mode_settings: IProjectRecordSettings = settings.active_mode_settings

    api = StooblyApi(settings.api_url, settings.api_key)

    if active_mode_settings.get('enabled') and allowed_request(active_mode_settings, request):
        upload_policy = get_record_policy(request.headers, active_mode_settings)
    else:
        # If the request path does not match accepted paths, do not record
        upload_policy = RECORD_POLICY['NONE']

    Logger.instance().debug(f"{LOG_ID}:UploadPolicy: {upload_policy}")

    if upload_policy == RECORD_POLICY['ALL']:
        thread = threading.Thread(target=upload_request, args=(flow, api, settings))
        thread.start()
        #upload_request(flow, api, settings)
    elif upload_policy == RECORD_POLICY['NOT_FOUND']:
        res = eval_request(request, api, active_mode_settings)

        if res.status_code == CUSTOM_RESPONSE_CODES['NOT_FOUND']:
            thread = threading.Thread(target=upload_request, args=(flow, api, settings))
            thread.start()
            #upload_request(flow, api, settings)
    elif upload_policy == RECORD_POLICY['NONE']:
        pass
    else:
        return bad_request(
            flow,
            "Valid env RECORD_POLICY: %s, %s, %s, Got: %s" %
            [RECORD_POLICY['ALL'], RECORD_POLICY['NOT_FOUND'], RECORD_POLICY['NONE'], upload_policy]
        )

def __disable_transfer_encoding(response: MitmproxyResponse):
    header_name = 'Transfer-Encoding'
    if header_name in response.headers and response.headers[header_name] == 'chunked':
        # Without deleting this header, causes caller to stall
        del response.headers['Transfer-Encoding']
