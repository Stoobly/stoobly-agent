import pdb

from mitmproxy.http import HTTPFlow as MitmproxyHTTPFlow

from stoobly_agent.app.proxy.replay.body_parser_service import encode_response
from stoobly_agent.app.proxy.replay.context import ReplayContext
from stoobly_agent.app.proxy.utils.request_handler import build_response
from stoobly_agent.app.proxy.utils.response_handler import disable_transfer_encoding
from stoobly_agent.app.settings import Settings
from stoobly_agent.config.constants import custom_headers, lifecycle_hooks, request_origin
from stoobly_agent.lib.api.endpoints_resource import EndpointsResource
from stoobly_agent.lib.api.interfaces.tests import TestShowResponse
from stoobly_agent.lib.logger import Logger

from .handle_mock_service import handle_request_mock_generic
from .handle_replay_service import handle_request_replay
from .mock.context import MockContext
from .test.helpers.test_results_builder import TestResultsBuilder
from .test.helpers.upload_test_service import inject_upload_test
from .test.context_abc import TestContextABC as TestContext
from .test.test_service import test

LOG_ID = 'HandleTest'

def handle_request_test(context: ReplayContext) -> None:
    handle_request_replay(context)

###
#
# Mock and Test modes share the same policies
#
def handle_response_test(context: ReplayContext) -> None:
    from .test.context import TestContext

    flow: MitmproxyHTTPFlow = context.flow
    intercept_settings = context.intercept_settings

    disable_transfer_encoding(flow.response)

    # At this point, the request may already been rewritten during replay
    # Request will be rewritten again for mocking purposes

    handle_request_mock_generic(
        MockContext(flow, intercept_settings),
        failure=lambda mock_context: __handle_mock_failure(TestContext(context, mock_context)),
        #infer=intercept_settings.test_strategy == test_strategy.FUZZY, # For fuzzy testing we can use an inferred response
        success=lambda mock_context: __handle_mock_success(TestContext(context, mock_context))
    )

def __decorate_test_id(flow: MitmproxyHTTPFlow, test_response: TestShowResponse):
    if test_response.get('id'):
        flow.response.headers[custom_headers.TEST_ID] = str(test_response['id'])

def __handle_mock_success(test_context: TestContext) -> None:
    flow: MitmproxyHTTPFlow = test_context.flow
    settings = Settings.instance()

    test_context.with_endpoints_resource(EndpointsResource(settings.remote.api_url, settings.remote.api_key))

    __test_hook(lifecycle_hooks.BEFORE_TEST, test_context)

    intercept_settings = test_context.intercept_settings
    if intercept_settings.test_skip:
        passed, log = (False, '')
        skipped = True
    else: 
        # Run test
        passed, log = test(test_context)
        skipped = False

    request_id = test_context.mock_request_id
    if request_id:
        expected = test_context.cached_rewritten_expected_response_content
        upload_test_data = {
            'log': log,
            'passed': passed,
            'request_id': request_id,
            'skipped': skipped,
            'status': flow.response.status_code,
            'strategy': test_context.strategy
        }

        is_cli = intercept_settings.request_origin == request_origin.CLI
        if not is_cli or test_context.save:
            # Re-serialize expected response since it was rewritten
            upload_test_data['expected_response'] = encode_response(expected, test_context.expected_response.content_type)
            upload_test = inject_upload_test(None, intercept_settings)

            # Commit test to API
            res = upload_test(
                flow,
                **upload_test_data
            )

            if is_cli:
                # If the origin was from a CLI, send test ID in response header
                if res.ok:
                    __decorate_test_id(flow, res.json())
                else:
                    # If we failed to upload test results, provide a local response
                    Logger.instance().warn(f"{LOG_ID}:TestStatus: Failed to upload results")
                    test_context.save = False

        if is_cli and not test_context.save:
            # No serialization is needed since TestResultsBuilder will serialize
            upload_test_data['expected_response'] = expected
            received = test_context.decoded_response_content

            builder = TestResultsBuilder(
                **{ 
                    'expected_latency': test_context.expected_latency,
                    'expected_status_code': test_context.expected_status_code,
                    'received_response': received
                },
                **upload_test_data
            )

            __override_response(flow, builder.serialize())

    __test_hook(lifecycle_hooks.AFTER_TEST, test_context)
    
    return flow.response

def __handle_mock_failure(test_context: TestContext) -> None:
    Logger.instance().warn(f"{LOG_ID}:TestStatus: No test found")

    intercept_settings = test_context.intercept_settings

    if intercept_settings.request_origin == request_origin.CLI:
        return build_response(False, 'No test found')

def __override_response(flow: MitmproxyHTTPFlow, content: bytes):
    headers = { 'Content-Type': 'text/plain' }
    headers[custom_headers.CONTENT_TYPE] = custom_headers.CONTENT_TYPE_TEST_RESULTS
    flow.response.headers = headers
    flow.response.set_content(content)
    flow.response.status_code = 200

def __test_hook(hook: str, context: TestContext):
    intercept_settings = context.intercept_settings
    lifecycle_hooks_module = intercept_settings.lifecycle_hooks

    if hook in lifecycle_hooks_module:
        lifecycle_hooks_module[hook](context)