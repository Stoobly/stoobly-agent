import pdb

from mitmproxy.http import HTTPFlow as MitmproxyHTTPFlow

from stoobly_agent.app.proxy.replay.context import ReplayContext
from stoobly_agent.app.proxy.utils.request_handler import build_response
from stoobly_agent.app.proxy.utils.response_handler import disable_transfer_encoding
from stoobly_agent.app.settings import Settings
from stoobly_agent.config.constants import custom_headers, request_origin
from stoobly_agent.lib.api.endpoints_resource import EndpointsResource
from stoobly_agent.lib.api.interfaces.tests import TestShowResponse
from stoobly_agent.lib.logger import Logger

from .handle_mock_service import handle_request_mock_generic
from .mock.context import MockContext
from .test.context import TestContext
from .test.test_service import test
from .upload.upload_test_service import inject_upload_test

LOG_ID = 'HandleTest'

###
#
# Mock and Test modes share the same policies
#
def handle_response_test(context: ReplayContext) -> None:
    flow: MitmproxyHTTPFlow = context.flow

    disable_transfer_encoding(flow.response)

    handle_request_mock_generic(
        MockContext(flow, context.intercept_settings),
        failure=lambda mock_context: __handle_mock_failure(TestContext(context, mock_context)),
        #infer=intercept_settings.test_strategy == test_strategy.FUZZY, # For fuzzy testing we can use an inferred response
        success=lambda mock_context: __handle_mock_success(TestContext(context, mock_context))
    )

def __decorate_test_id(flow: MitmproxyHTTPFlow, test_response: TestShowResponse):
    if test_response.get('id'):
        flow.response.headers[custom_headers.TEST_ID] = str(test_response['id'])

def __handle_mock_success(test_context: TestContext) -> None:
    intercept_settings = test_context.intercept_settings

    settings = Settings.instance()
    test_context.with_endpoints_resource(EndpointsResource(settings.remote.api_url, settings.remote.api_key))
    
    # Run test
    passed, log = test(test_context)

    flow = test_context.flow
    request_id = test_context.mock_request_id
    if request_id:
        upload_test = inject_upload_test(None, intercept_settings)

        # Commit test to API
        res = upload_test(
            flow,
            expected_response=test_context.cached_expected_response_content,
            log=log,
            passed=passed,
            request_id=request_id,
            status=flow.response.status_code,
            strategy=intercept_settings.test_strategy
        )

        # If the origin was from a CLI, send test ID in response header
        if intercept_settings.request_origin == request_origin.CLI and res.ok:
            __decorate_test_id(flow, res.json())
    
    return flow.response

def __handle_mock_failure(test_context: TestContext) -> None:
    Logger.instance().warn(f"{LOG_ID}:TestStatus: No test found")

    intercept_settings = test_context.intercept_settings

    if intercept_settings.request_origin == request_origin.CLI:
        return build_response(False, 'No test found')