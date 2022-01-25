from ..logger import Logger
from ..stoobly_api import StooblyApi

from .custom_headers import CUSTOM_HEADERS
from .custom_response_codes import CUSTOM_RESPONSE_CODES
from .handle_mock_service import handle_request_mock_generic

###
#
# Mock and Test modes share the same policies
#
# @param request [mitmproxy.net.http.request.Request]
# @param settings [Dict]
#
def handle_request_test(flow, settings):
    handle_request_mock_generic(flow, settings, lambda res, start_time: __test_callback(res, flow))

def __test_callback(res, flow):
    pass
