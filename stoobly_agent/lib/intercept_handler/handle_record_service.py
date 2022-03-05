import threading

from mitmproxy.http import HTTPFlow as MitmproxyHTTPFlow
from mitmproxy.net.http.request import Request as MitmproxyRequest
from mitmproxy.net.http.response import Response as MitmproxyResponse 

from ..api.requests_resource import RequestsResource
from ..logger import Logger
from ..settings import IProjectRecordSettings, Settings
from .constants import custom_response_codes, record_policy
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

    request: MitmproxyRequest = flow.request

    active_mode_settings: IProjectRecordSettings = settings.active_mode_settings

    if active_mode_settings.get('enabled') and allowed_request(active_mode_settings, request):
        upload_policy = get_record_policy(request.headers, active_mode_settings)
    else:
        # If the request path does not match accepted paths, do not record
        upload_policy = record_policy.NONE

    Logger.instance().debug(f"{LOG_ID}:UploadPolicy: {upload_policy}")

    if upload_policy == record_policy.ALL:
        api = RequestsResource(settings.api_url, settings.api_key)
        thread = threading.Thread(target=inject_upload_request(api, settings), args=[flow])
        thread.start()
    elif upload_policy == record_policy.NOT_FOUND:
        api = RequestsResource(settings.api_url, settings.api_key)
        res = inject_eval_request(api, active_mode_settings)(request, [])

        if res.status_code == custom_response_codes.NOT_FOUND:
            thread = threading.Thread(target=inject_upload_request(api, settings), args=[flow])
            thread.start()
    elif upload_policy == record_policy.NONE:
        pass
    else:
        return bad_request(
            flow,
            "Valid env RECORD_POLICY: %s, %s, %s, Got: %s" %
            [record_policy.ALL, record_policy.NOT_FOUND, record_policy.NONE, upload_policy]
        )

def __disable_transfer_encoding(response: MitmproxyResponse):
    header_name = 'Transfer-Encoding'
    if header_name in response.headers and response.headers[header_name] == 'chunked':
        # Without deleting this header, causes caller to stall
        del response.headers['Transfer-Encoding']
