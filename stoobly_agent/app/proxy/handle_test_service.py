import pdb

from mitmproxy.http import HTTPFlow as MitmproxyHTTPFlow

from stoobly_agent.app.proxy.intercept_settings import InterceptSettings
from stoobly_agent.app.proxy.utils.request_handler import build_response
from stoobly_agent.app.proxy.utils.response_handler import disable_transfer_encoding
from stoobly_agent.app.settings import Settings
from stoobly_agent.config.constants import custom_headers, request_origin
from stoobly_agent.lib.api.endpoints_resource import EndpointsResource
from stoobly_agent.lib.api.interfaces.tests import TestShowResponse
from stoobly_agent.lib.logger import Logger

from .handle_mock_service import handle_request_mock_generic
from .mitmproxy.request_facade import MitmproxyRequestFacade
from .mock.context import MockContext
from .test.context import TestContext
from .test.test_service import test
from .upload.upload_test_service import inject_upload_test
from .utils.filter_rules_to_ignored_components_service import filter_rules_to_ignored_components

LOG_ID = 'HandleTest'

###
#
# Mock and Test modes share the same policies
#
def handle_response_test(flow: MitmproxyHTTPFlow, intercept_settings: InterceptSettings) -> None:
    disable_transfer_encoding(flow.response)

    ignored_components = []

    # If ignore rules are set, then ignore specified request parameters
    ignore_rules = intercept_settings.ignore_rules
    if len(ignore_rules) > 0:
        request = MitmproxyRequestFacade(flow.request)
        ignore_rules = request.select_parameter_rules(ignore_rules)
        ignored_components = filter_rules_to_ignored_components(ignore_rules)

    context = MockContext(flow)

    handle_request_mock_generic(
        context,
        intercept_settings,
        failure=lambda context: __handle_mock_failure(context, intercept_settings),
        ignored_components=ignored_components,
        #infer=intercept_settings.test_strategy == test_strategy.FUZZY, # For fuzzy testing we can use an inferred response
        success=lambda context: __handle_mock_success(context, intercept_settings)
    )

def __decorate_test_id(flow: MitmproxyHTTPFlow, test_response: TestShowResponse):
    if test_response.get('id'):
        flow.response.headers[custom_headers.TEST_ID] = str(test_response['id'])

def __handle_mock_success(mock_context: MockContext, intercept_settings: InterceptSettings) -> None:
    # Build TestContext
    test_context = TestContext(mock_context)
    test_strategy = intercept_settings.test_strategy
    test_context.strategy = test_strategy
    settings = Settings.instance()
    test_context.with_response_param_names(EndpointsResource(settings.remote.api_url, settings.remote.api_key))
    
    # Run test
    passed, log = test(test_context)

    flow = mock_context.flow
    request_id = test_context.mock_request_id
    if request_id:
        upload_test = inject_upload_test(None, intercept_settings)

        # Commit test to API
        res = upload_test(
            flow,
            log=log,
            passed=passed,
            request_id=request_id,
            status=flow.response.status_code,
            strategy=test_strategy
        )

        # If the origin was from a CLI, send test ID in response header
        if intercept_settings.request_origin == request_origin.CLI and res.ok:
            __decorate_test_id(flow, res.json())
    
    return flow.response

def __handle_mock_failure(context: MockContext, intercept_settings: InterceptSettings) -> None:
    Logger.instance().warn(f"{LOG_ID}:TestStatus: No test found")

    if intercept_settings.request_origin == request_origin.CLI:
        return build_response(False, 'No test found')