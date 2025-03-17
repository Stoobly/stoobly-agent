import os
import pdb

from mitmproxy.http import HTTPFlow as MitmproxyHTTPFlow
from mitmproxy.http import Headers, Request as MitmproxyRequest

from stoobly_agent.app.proxy.context import InterceptContext
from stoobly_agent.app.proxy.handle_mock_service import handle_request_mock, handle_response_mock
from stoobly_agent.app.proxy.handle_replay_service import handle_request_replay, handle_response_replay
from stoobly_agent.app.proxy.handle_record_service import handle_response_record
from stoobly_agent.app.proxy.handle_test_service import handle_request_test, handle_response_test
from stoobly_agent.app.proxy.intercept_settings import InterceptSettings
from stoobly_agent.app.proxy.mock.context import MockContext
from stoobly_agent.app.proxy.replay.context import ReplayContext
from stoobly_agent.app.proxy.record.context import RecordContext
from stoobly_agent.app.proxy.utils.response_handler import bad_request
from stoobly_agent.app.settings import Settings
from stoobly_agent.config.constants import lifecycle_hooks, mode
from stoobly_agent.lib.logger import Logger

# Disable proxy settings in urllib
os.environ['no_proxy'] = '*'

LOG_ID = 'Intercept'

def request(flow: MitmproxyHTTPFlow):
    request: MitmproxyRequest = flow.request

    __patch_cookie(request)

    intercept_settings = InterceptSettings(Settings.instance(), request)

    if not intercept_settings.active:
        return

    __disable_web_cache(request)
    __intercept_hook(lifecycle_hooks.BEFORE_REQUEST, flow, intercept_settings)

    active_mode = intercept_settings.mode
    Logger.instance(LOG_ID).debug(f"ProxyMode: {active_mode}")

    if active_mode == mode.MOCK:
        context = MockContext(flow, intercept_settings)
        handle_request_mock(context)
    elif active_mode == mode.RECORD:
        pass
    elif active_mode == mode.REPLAY:
        context = ReplayContext(flow, intercept_settings)
        handle_request_replay(context)
    elif active_mode == mode.TEST:
        context = ReplayContext(flow, intercept_settings)
        handle_request_test(context)
    else:
        if active_mode != mode.NONE:
            bad_request(
                flow,
                "Valid env MODES: %s, Got: %s" % ([mode.MOCK, mode.RECORD, mode.REPLAY, mode.TEST], active_mode)
            )

def response(flow: MitmproxyHTTPFlow):
    request: MitmproxyRequest = flow.request

    intercept_settings = InterceptSettings(Settings.instance(), request)
    intercept_settings.for_response()

    if not intercept_settings.active:
        return

    active_mode = intercept_settings.mode

    if active_mode == mode.MOCK:
        context = MockContext(flow, intercept_settings)
        handle_response_mock(context)
    elif active_mode == mode.RECORD:
        context = RecordContext(flow, intercept_settings)
        handle_response_record(context)
    elif active_mode == mode.REPLAY:
        context = ReplayContext(flow, intercept_settings)
        handle_response_replay(context)
    elif active_mode == mode.TEST:
        context = ReplayContext(flow, intercept_settings)
        handle_response_test(context)

    __intercept_hook(lifecycle_hooks.BEFORE_RESPONSE, flow, intercept_settings)

### PRIVATE

# Prevent 304 status
# Because this header will get recorded, should add during mocking as well in the case where headers are used for matching
def __disable_web_cache(request: MitmproxyRequest) -> None:
    request.headers['Cache-Control'] = 'no-cache, no-store'

# Fix issue where multi-value cookies become comma separated
def __patch_cookie(request: MitmproxyRequest):
    header_name = 'cookie'

    if len(request.headers.get_all(header_name)) > 1:
        __combine_header(request.headers, header_name, '; ')
        
def __combine_header(headers: Headers, header_name: str, delimitter: str):
    values = headers.get_all(header_name)
    headers[header_name] = delimitter.join(values)

def __intercept_hook(hook: str, flow: MitmproxyHTTPFlow, intercept_settings: InterceptSettings):
    lifecycle_hooks_module = intercept_settings.lifecycle_hooks

    if hook in lifecycle_hooks_module:
        lifecycle_hooks_module[hook](InterceptContext(flow, intercept_settings))