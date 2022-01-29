import threading

from ..logger import Logger
from ..stoobly_api import StooblyApi
from .allowed_request_service import allowed_request
from .custom_response_codes import CUSTOM_RESPONSE_CODES
from .eval_request_service import eval_request
from .response_handler import bad_request, pass_on, reverse_proxy
from .settings import get_record_policy, get_service_url
from .upload_request_service import upload_request


LOG_ID = 'HandleRecord'
RECORD_POLICY = {
    'NONE': 'none',
    'ALL': 'all',
    'NOT_FOUND': 'not_found',
}

def handle_request_record(request, settings):
    active_mode_settings = settings.active_mode_settings

    service_url = get_service_url(request, active_mode_settings)

    #
    # Try forwarding the request to the service specified by Settings.service_url
    #
    if not service_url:
        raise Exception('config service_url is not set')

    Logger.instance().debug(f"{LOG_ID}:ReverseProxy:ServiceUrl: {service_url}")
    reverse_proxy(request, service_url, {})

def handle_response_record(flow, settings):
    __disable_transfer_encoding(flow.response)

    request = flow.request

    active_mode_settings = settings.active_mode_settings

    api = StooblyApi(
      settings.api_url, settings.api_key
    )

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

def __disable_transfer_encoding(response):
    if 'Transfer-Encoding' in response.headers:
        # Without deleting this header, causes caller to stall
        del response.headers['Transfer-Encoding']