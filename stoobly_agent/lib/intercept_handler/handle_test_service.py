import pdb
import time

from mitmproxy.http import HTTPFlow as MitmproxyHTTPFlow
from mitmproxy.net.http.response import Response as MitmproxyResponse

from ..api.requests_resource import RequestsResource
from ..logger import Logger
from ..settings import Settings, IProjectTestSettings

from ..constants import custom_headers
from .mitmproxy.request_adapter import MitmproxyRequestAdapter
from .utils.filters_to_ignored_components_service import filters_to_ignored_components
from .handle_mock_service import handle_request_mock_generic
from .mock.context import MockContext
from .test.test_service import test, TEST_STRATEGIES
from .test.context import TestContext
from .test.mitmproxy_response_adapter import MitmproxyResponseAdapter
from .test.requests_response_adapter import RequestsResponseAdapter
from .upload.upload_test_service import inject_upload_test

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

    api = RequestsResource(settings.api_url, settings.api_key)
    context = MockContext(flow, active_mode_settings).with_api(api)

    handle_request_mock_generic(
        context,
        failure=__handle_mock_failure,
        ignored_components=ignored_components,
        success=__handle_mock_success
    )

def __handle_mock_success(context: MockContext) -> None:
    expected_response = context.response
    request_id = expected_response.headers.get(custom_headers.MOCK_REQUEST_ID)

    if request_id:
        active_mode_settings = context.active_mode_settings
        flow = context.flow

        # Build TestContext
        response = MitmproxyResponseAdapter(flow.response).adapt() 
        test_strategy = active_mode_settings.get('strategy') or TEST_STRATEGIES['DIFF']

        test_context = TestContext(test_strategy)
        test_context.start_time = context.start_time
        
        test_context.with_expected_response(RequestsResponseAdapter(expected_response).adapt())
        test_context.with_response(response)

        # Run test
        passed, log = test(test_context)

        # Commit test to API
        upload_test = inject_upload_test(None, active_mode_settings)
        upload_test(
            flow,
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
