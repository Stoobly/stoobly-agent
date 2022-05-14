import pdb
import threading

from mitmproxy.http import HTTPFlow as MitmproxyHTTPFlow
from mitmproxy.net.http.request import Request as MitmproxyRequest
from mitmproxy.net.http.response import Response as MitmproxyResponse 

from stoobly_agent.app.models.request_model import RequestModel
from stoobly_agent.app.proxy.intercept_settings import InterceptSettings
from stoobly_agent.config.constants import record_policy
from stoobly_agent.lib.logger import Logger

from .constants import custom_response_codes
from .mock.eval_request_service import inject_eval_request
from .upload.upload_request_service import inject_upload_request
from .utils.allowed_request_service import allowed_request
from .utils.request_handler import reverse_proxy
from .utils.response_handler import bad_request, disable_transfer_encoding 

LOG_ID = 'HandleRecord'

def handle_request_record(request: MitmproxyRequest, intercept_settings: InterceptSettings):
    upstream_url = intercept_settings.upstream_url

    #
    # Try forwarding the request to the service specified by Settings.service_url
    #
    if not upstream_url:
        raise Exception('config service_url is not set')

    Logger.instance().debug(f"{LOG_ID}:ReverseProxy:UpstreamUrl: {upstream_url}")

    reverse_proxy(request, upstream_url, {})

def handle_response_record(flow: MitmproxyHTTPFlow, intercept_settings: InterceptSettings):
    request: MitmproxyRequest = flow.request

    disable_transfer_encoding(flow.response)

    request_model = RequestModel(intercept_settings.settings)

    active_record_policy = __get_record_policy(request, intercept_settings)
    Logger.instance().debug(f"{LOG_ID}:RecordPolicy: {active_record_policy}")

    if active_record_policy == record_policy.ALL:
        __record_request(request_model, intercept_settings, flow)
    elif active_record_policy == record_policy.FOUND:
        res = inject_eval_request(request_model, intercept_settings)(request, [])

        if res.status_code != custom_response_codes.NOT_FOUND:
            __record_request(request_model, intercept_settings, flow)
    elif active_record_policy == record_policy.NOT_FOUND:
        res = inject_eval_request(request_model, intercept_settings)(request, [])

        if res.status_code == custom_response_codes.NOT_FOUND:
            __record_request(request_model, intercept_settings, flow)
    else:
        if active_record_policy != record_policy.NONE:
            return bad_request(
                flow,
                "Valid env RECORD_POLICY: %s, %s, %s, Got: %s" %
                [record_policy.ALL, record_policy.FOUND, record_policy.NOT_FOUND, active_record_policy]
            )

def __record_request(request_model: RequestModel, intercept_settings: InterceptSettings, flow: MitmproxyHTTPFlow):
    thread = threading.Thread(
        target=inject_upload_request(request_model, intercept_settings), 
        args=[flow]
    )
    thread.start()

def __get_record_policy(request: MitmproxyRequest, intercept_settings: InterceptSettings):
    if intercept_settings.active and allowed_request(intercept_settings, request):
        return intercept_settings.policy
    else:
        # If the request path does not match accepted paths, do not record
        return record_policy.NONE