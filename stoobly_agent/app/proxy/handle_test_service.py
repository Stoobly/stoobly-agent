import json
import pdb

from mitmproxy.http import HTTPFlow as MitmproxyHTTPFlow
from mitmproxy.net.http.response import Response as MitmproxyResponse

from stoobly_agent.app.models.request_model import RequestModel
from stoobly_agent.app.proxy.intercept_settings import InterceptSettings
from stoobly_agent.config.constants import custom_headers, test_origin
from stoobly_agent.lib.logger import Logger
from stoobly_agent.lib.orm.utils.requests_response_builder import RequestsResponseBuilder

from .handle_mock_service import handle_request_mock_generic
from .mitmproxy.request_facade import MitmproxyRequestFacade
from .mock.context import MockContext
from .test.context import TestContext
from .test.mitmproxy_response_adapter import MitmproxyResponseAdapter
from .test.requests_response_adapter import RequestsResponseAdapter
from .test.test_service import test
from .upload.upload_test_service import inject_upload_test
from .utils.filter_rules_to_ignored_components_service import filter_rules_to_ignored_components

LOG_ID = 'HandleTest'

###
#
# Mock and Test modes share the same policies
#
# @param request [mitmproxy.net.http.request.Request]
# @param settings [Dict]
#
def handle_response_test(flow: MitmproxyHTTPFlow, intercept_settings: InterceptSettings) -> None:
    __disable_transfer_encoding(flow.response)

    ignored_components = []

    # If ignore rules are set, then ignore specified request parameters
    ignore_rules = intercept_settings.ignore_rules
    if len(ignore_rules) > 0:
        request = MitmproxyRequestFacade(flow.request)
        ignore_rules = request.select_parameter_rules(ignore_rules)
        ignored_components = filter_rules_to_ignored_components(ignore_rules)

    request_model = RequestModel(intercept_settings.settings)
    context = MockContext(flow, intercept_settings).with_model(request_model)

    handle_request_mock_generic(
        context,
        failure=__handle_mock_failure,
        ignored_components=ignored_components,
        success=__handle_mock_success
    )

def __handle_mock_success(context: MockContext) -> None:
    expected_response = context.response
    intercept_settings = context.intercept_settings
    flow = context.flow

    # Build TestContext
    response = MitmproxyResponseAdapter(flow.response).adapt() 
    test_strategy = intercept_settings.test_strategy
        
    test_context = TestContext(test_strategy)
    test_context.start_time = context.start_time
    
    test_context.with_expected_response(RequestsResponseAdapter(expected_response).adapt())
    test_context.with_response(response)

    # Run test
    passed, log = test(test_context)

    request_id = expected_response.headers.get(custom_headers.MOCK_REQUEST_ID)
    if request_id:
        # Commit test to API
        upload_test = inject_upload_test(None, intercept_settings)
        upload_test(
            flow,
            log=log,
            passed=passed,
            request_id=request_id,
            status=response.status_code,
            strategy=test_strategy
        )

    # If the origin was from a CLI, send a JSON response
    # Testing via browser for example, requires the actual response to be returned
    if intercept_settings.test_origin == test_origin.CLI:
        return __build_response(passed, log)

def __build_response(passed, log):
    body = json.dumps({
        'log': log,
        'passed': passed,
    }).encode()
 
    builder = RequestsResponseBuilder()
    builder.with_header('content-type', 'application/json')
    builder.with_body(body)
    builder.with_status_code(200)

    return builder.build()

def __handle_mock_failure(context: MockContext) -> None:
    Logger.instance().warn(f"{LOG_ID}:TestStatus: No test found")

    intercept_settings = context.intercept_settings
    if intercept_settings.test_origin == test_origin.CLI:
        return __build_response(False, 'No test found')

# Without deleting this header, causes parsing issues when reading response
def __disable_transfer_encoding(response: MitmproxyResponse) -> None:
    header_name = 'Transfer-Encoding'
    if header_name in response.headers and response.headers[header_name] == 'chunked':
        del response.headers['Transfer-Encoding']
