import pdb

from ..logger import Logger
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
def handle_request_test(flow, settings):
    __disable_transfer_encoding(flow.response)

    handle_request_mock_generic(
        flow,
        settings,
        failure=lambda res, start_time: __handle_mock_failure(res, flow, settings),
        success=lambda res, start_time: __handle_mock_success(res, flow, settings)
    )

def __handle_mock_success(res, flow, settings):
    active_mode_settings = settings.active_mode_settings

    response = flow.response
    test_strategy = active_mode_settings.get('strategy')
    passed, log = test(flow, res, test_strategy)

    res = upload_test(
        flow, settings,
        log=log,
        passed=passed,
        request_id=res.headers.get(CUSTOM_HEADERS['MOCK_REQUEST_ID']),
        status=response.status_code,
        strategy=test_strategy
    )


def __handle_mock_failure(res, flow, settings):
    Logger.instance().info(f"{LOG_ID}:TestStatus: No test found")

# Without deleting this header, causes parsing issues when reading response
def __disable_transfer_encoding(response):
    header_name = 'Transfer-Encoding'
    if header_name in response.headers and response.headers[header_name] == 'chunked':
        del response.headers['Transfer-Encoding']
