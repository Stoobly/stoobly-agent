import pdb
import time

from mitmproxy.http import HTTPFlow as MitmproxyHTTPFlow
from mitmproxy.net.http.request import Request as MitmproxyRequest
from mitmproxy.net.http.response import Response as MitmproxyResponse
from requests import Response

from ..logger import Logger
from ..settings import Settings, IProjectTestSettings
from ..stoobly_api import StooblyApi

from ..mitmproxy_request_adapter import MitmproxyRequestAdapter
from .constants.custom_headers import CUSTOM_HEADERS
from .filters_to_ignored_components_service import filters_to_ignored_components
from .handle_mock_service import handle_request_mock_generic
from .mock_context import MockContext
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

    # If rewrite rules are set, then rewrite the request
    ignored_components = []
    if active_mode_settings.get('rewrite_rules'):
        request = MitmproxyRequestAdapter(flow.request)
        request.rewrite(active_mode_settings.get('rewrite_rules'))

        rewrite_rules = request.relevant_rewrites
        ignored_components = filters_to_ignored_components(rewrite_rules)

    api = StooblyApi(settings.api_url, settings.api_key)
    context = MockContext(flow, active_mode_settings).with_api(api)

    handle_request_mock_generic(
        context,
        failure=__handle_mock_failure,
        ignored_components=ignored_components,
        success=__handle_mock_success
    )

def __handle_mock_success(context: MockContext) -> None:
    expected_response = context.response
    request_id = expected_response.headers.get(CUSTOM_HEADERS['MOCK_REQUEST_ID'])

    if request_id:
        active_mode_settings = context.active_mode_settings
        api = context.api
        flow = context.flow
        response: MitmproxyResponse = flow.response
        test_strategy = active_mode_settings.get('strategy')
        passed, log = test(test_strategy, context)

        upload_test(
            flow, api, active_mode_settings,
            log=log,
            passed=passed,
            request_id=request_id,
            status=response.status_code,
            strategy=test_strategy
        )

def __handle_mock_failure(context: MockContext) -> None:
    Logger.instance().info(f"{LOG_ID}:TestStatus: No test found")

# Without deleting this header, causes parsing issues when reading response
def __disable_transfer_encoding(response: MitmproxyResponse) -> None:
    header_name = 'Transfer-Encoding'
    if header_name in response.headers and response.headers[header_name] == 'chunked':
        del response.headers['Transfer-Encoding']
