import pdb

from mitmproxy.http import HTTPFlow as MitmproxyHTTPFlow
from mitmproxy.net.http.request import Request as MitmproxyRequest
from mitmproxy.net.http.response import Response as MitmproxyResponse 
from requests import Response

from ..logger import Logger
from ..settings import Settings, IProjectTestSettings
from ..stoobly_api import StooblyApi

from .custom_headers import CUSTOM_HEADERS
from .handle_mock_service import handle_request_mock_generic
from .test_service import test
from .upload_test_service import upload_test

LOG_ID = 'HandleTest'

###
#
# Mock and Test modes share the same policies
#
# @param request [mitmproxy.net.http.request.Request]
# @param settings [Dict]
#
def handle_request_test(flow: MitmproxyHTTPFlow, settings: Settings) -> None:
    __disable_transfer_encoding(flow.response)

    active_mode_settings: IProjectTestSettings = settings.active_mode_settings
    api = StooblyApi(settings.api_url, settings.api_key)

    handle_request_mock_generic(
        flow, api, active_mode_settings,
        failure=__handle_mock_failure,
        success=lambda req, res: __handle_mock_success(res, flow, api, active_mode_settings)
    )

def __handle_mock_success(
    expected_response: Response, 
    flow: MitmproxyHTTPFlow, 
    api: StooblyApi, 
    active_mode_settings: IProjectTestSettings
) -> None:
    response: MitmproxyResponse = flow.response
    test_strategy = active_mode_settings.get('strategy')
    passed, log = test(flow, expected_response, test_strategy)

    res = upload_test(
        flow, api, active_mode_settings,
        log=log,
        passed=passed,
        request_id=expected_response.headers.get(CUSTOM_HEADERS['MOCK_REQUEST_ID']),
        status=response.status_code,
        strategy=test_strategy
    )

def __handle_mock_failure(res: Response) -> None:
    Logger.instance().info(f"{LOG_ID}:TestStatus: No test found")

# Without deleting this header, causes parsing issues when reading response
def __disable_transfer_encoding(response: MitmproxyResponse) -> None:
    header_name = 'Transfer-Encoding'
    if header_name in response.headers and response.headers[header_name] == 'chunked':
        del response.headers['Transfer-Encoding']
