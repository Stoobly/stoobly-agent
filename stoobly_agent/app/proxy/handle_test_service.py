import pdb

from threading import local
from typing import TYPE_CHECKING, Union

from stoobly_agent.app.cli.helpers.feature_flags import local as is_local
from stoobly_agent.app.settings import Settings

if TYPE_CHECKING:
    from mitmproxy.http import HTTPFlow as MitmproxyHTTPFlow

from stoobly_agent.app.proxy.context import InterceptContext
from stoobly_agent.app.proxy.intercept_settings import InterceptSettings
from stoobly_agent.app.proxy.record.context import RecordContext
from stoobly_agent.app.proxy.replay.body_parser_service import encode_response
from stoobly_agent.app.proxy.replay.context import ReplayContext
from stoobly_agent.app.proxy.utils.request_handler import build_response
from stoobly_agent.app.proxy.utils.response_handler import bad_request, disable_transfer_encoding, pass_on
from stoobly_agent.config.constants import custom_headers, lifecycle_hooks, mock_policy, request_origin, test_policy
from stoobly_agent.lib.logger import Logger, bcolors

from .handle_mock_service import (
    handle_mock_failure as handle_mock_failure_service,
    handle_mock_success as handle_mock_success_service,
    handle_request_mock,
    handle_request_mock_generic,
    handle_response_mock,
)
from .handle_replay_service import handle_request_replay, handle_response_replay
from .mock.context import MockContext
from .test.helpers.test_results_builder import TestResultsBuilder
from .test.helpers.upload_test_service import inject_upload_test
from .test.context_abc import TestContextABC as TestContext
from .test.test_service import test
from .utils.rewrite import rewrite_request, rewrite_response, rewrite_request_response

LOG_ID = 'Test'

###
#
# 1. BEFORE_REPLAY gets triggered
#
def handle_request_test(context: ReplayContext) -> None:
    if context.intercept_settings.policy == test_policy.FOUND:
        # To differentiate test rewrite rules, outbound request uses replay rules
        # Test rules are applied to the request and its response 
        handle_request_replay(context)
    else:
        if context.intercept_settings.policy != test_policy.NONE:
            return __handle_invalid_policy(context)

        handle_request_mock(MockContext(context.flow, context.intercept_settings))

###
#
# 1.  AFTER_REPLAY gets triggered
# 2.  BEFORE_MOCK gets triggered
# 3.  AFTER_MOCK gets triggered
# 4.  Rewrites test request and response (response from live service) to obtain expected test results
# 5.  BEFORE_TEST gets triggered
# 6.  Tests against rewritten test response and mock response (expected response)
# 7.  AFTER_TEST gets triggered 
# 8.  BEFORE_RECORD gets triggered (if not from CLI)
# 9.  AFTER_RECORD gets triggered (if not from CLI)
#
def handle_response_test(context: ReplayContext) -> None:
    # Lazy import for runtime usage
    from .test.context import TestContext

    flow: 'MitmproxyHTTPFlow' = context.flow
    intercept_settings: InterceptSettings = context.intercept_settings

    if intercept_settings.test_policy == test_policy.FOUND:
        disable_transfer_encoding(flow.response)
        handle_response_replay(context)

        # If mock policy is NONE, we return live request response
        # To achieve this, copy the flow to prevent modifications from persisting
        mock_flow = flow.copy() if intercept_settings.mock_policy == mock_policy.NONE else flow

        # Because we are testing, we the mock to deterine expected response
        # Therefore, we set mock policy to ALL
        mock_flow.request.headers[custom_headers.MOCK_POLICY] = mock_policy.ALL

        test_context: TestContext = None
        def build_test_context(mock_context: MockContext):
            nonlocal test_context  # Bind to outer scope variable so modifications are visible after callback execution
            # Deep copy flow to prevent modifications from persisting
            test_context = TestContext(ReplayContext(flow.copy(), intercept_settings), mock_context)
            return test_context

        def handle_mock_error(mock_context: MockContext):
            return __handle_mock_error(build_test_context(mock_context))

        def handle_mock_failure(mock_context: MockContext):
            handle_mock_failure_service(mock_context)
            return __handle_mock_failure(build_test_context(mock_context))

        def handle_mock_success(mock_context: MockContext):
            handle_mock_success_service(mock_context)
            handle_response_mock(mock_context)
            return __handle_mock_success(build_test_context(mock_context))

        handle_request_mock_generic(
            MockContext(mock_flow, context.intercept_settings),
            error=handle_mock_error,
            failure=handle_mock_failure,
            success=handle_mock_success
            #infer=intercept_settings.test_strategy == test_strategy.FUZZY, # For fuzzy testing we can use an inferred response
        )

        # If test context was built, and it has test results, override response with test results
        if test_context:
            if test_context.test_results:
                __override_response(flow, test_context.test_results.serialize())

            # Apply test ID from flow.copy() to the original flow that will returned to the client
            if test_context.test_id:
                __decorate_test_id(flow, test_context.test_id)
    else:
        handle_response_mock(MockContext(flow, intercept_settings))

def __decorate_test_id(flow: 'MitmproxyHTTPFlow', test_id: Union[str, None]):
    if test_id:
        flow.response.headers[custom_headers.TEST_ID] = str(test_id)

def __handle_mock_error(test_context: TestContext):
    intercept_settings = test_context.intercept_settings

    if intercept_settings.request_origin == request_origin.CLI:
        return build_response(False, 'No test found')

def __handle_mock_failure(test_context: TestContext) -> None:
    intercept_settings = test_context.intercept_settings

    if intercept_settings.request_origin == request_origin.CLI:
        return build_response(False, 'No test found')

def __handle_mock_success(test_context: TestContext) -> None:
    flow: 'MitmproxyHTTPFlow' = test_context.flow
    intercept_settings = test_context.intercept_settings
    mock_response = test_context.mock_context.response
    request_key = mock_response.headers.get(custom_headers.MOCK_REQUEST_KEY) if mock_response else None

    if request_key:
        Logger.instance(LOG_ID).info(f"{bcolors.OKBLUE}Testing{bcolors.ENDC} {request_key} from {intercept_settings.request_origin}")

    __rewrite_request(test_context.replay_context)
    __rewrite_response(test_context.replay_context)
    __test_hook(lifecycle_hooks.BEFORE_TEST, test_context)


    if intercept_settings.test_skip:
        passed, log = (False, '')
        skipped = True
    else:
        # Run test
        passed, log = test(test_context)
        skipped = False

    __test_hook(lifecycle_hooks.AFTER_TEST, test_context)

    request_id = test_context.mock_request_id
    if request_id:
        is_cli = intercept_settings.request_origin == request_origin.CLI
        expected = test_context.cached_rewritten_expected_response_content
        upload_test_data = {
            'log': log,
            'passed': passed,
            'request_id': request_id,
            'skipped': skipped,
            'status': flow.response.status_code,
            'strategy': test_context.strategy
        }
        settings = Settings.instance()

        # Upload handling
        if not is_local(settings):
            # Upload for every non-CLI request, or for CLI when save is enabled.
            if test_context.save or not is_cli:
                # Re-serialize expected response since it was rewritten
                upload_test_data['expected_response'] = encode_response(expected, test_context.expected_response.content_type)

                res = __record_handler(test_context, upload_test_data)

                if is_cli:
                    # This CLI path implies save was on; record success as test id, or clear save intent after a failed upload.
                    if res.ok:
                        response = res.json()
                        test_context.with_test_id(response.get('id'))
                    else:
                        Logger.instance().warning(f"{LOG_ID}:TestStatus: Failed to upload results")
                        test_context.save = False

        # Response handling
        if is_cli:
            # Always attach TestResultsBuilder for the response body 
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

            test_context.with_test_results(builder)

def __handle_invalid_policy(context: InterceptContext):
    return bad_request(
        context.flow,
        "Valid test policies: %s, Got: %s" %
        ([test_policy.FOUND, test_policy.NONE], context.intercept_settings.policy)
    )
 
def __override_response(flow: 'MitmproxyHTTPFlow', content: bytes):
    headers = { 'Content-Type': 'text/plain' }
    headers[custom_headers.CONTENT_TYPE] = custom_headers.CONTENT_TYPE_TEST_RESULTS
    flow.response.headers = headers
    flow.response.set_content(content)
    flow.response.status_code = 200

def __record_handler(context: TestContext, upload_test_data):
    flow = context.flow.copy() # Deep copy flow to prevent response modifications from persisting
    intercept_settings = context.intercept_settings
    record_context = RecordContext(flow, intercept_settings)

    # Since we are "uploading" the request, use record_write_rules
    rewrite_request_response(record_context.flow, intercept_settings.record_rewrite_rules)
    __test_hook(lifecycle_hooks.BEFORE_RECORD, record_context)

    # Commit test to API
    upload_test = inject_upload_test(None, intercept_settings)
    res = upload_test(
        record_context.flow, **upload_test_data
    )

    __test_hook(lifecycle_hooks.AFTER_RECORD, record_context)

    return res

def __rewrite_request(context: ReplayContext):
    """
    Before replaying a request, see if the request needs to be rewritten
    """
    intercept_settings: InterceptSettings = context.intercept_settings
    rewrite_rules = intercept_settings.test_rewrite_rules

    if len(rewrite_rules) > 0:
        rewrite_request(context.flow, rewrite_rules)

def __rewrite_response(context: ReplayContext):
    """
    After replaying a request, see if the request response needs to be rewritten
    """
    intercept_settings: InterceptSettings = context.intercept_settings
    rewrite_rules = intercept_settings.test_rewrite_rules

    if len(rewrite_rules) > 0:
        rewrite_response(context.flow, rewrite_rules)

def __test_hook(hook: str, context: TestContext):
    intercept_settings = context.intercept_settings
    lifecycle_hooks_module = intercept_settings.lifecycle_hooks

    if hook in lifecycle_hooks_module:
        lifecycle_hooks_module[hook](context)