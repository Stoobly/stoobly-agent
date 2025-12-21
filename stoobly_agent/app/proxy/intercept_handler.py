import os
import pdb

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mitmproxy.http import HTTPFlow as MitmproxyHTTPFlow
    from mitmproxy.http import Headers, Request as MitmproxyRequest

from stoobly_agent.app.models.scenario_model import ScenarioModel
from stoobly_agent.app.proxy.context import InterceptContext
from stoobly_agent.app.proxy.handle_mock_service import handle_request_mock, handle_response_mock
from stoobly_agent.app.proxy.handle_replay_service import handle_request_replay, handle_response_replay
from stoobly_agent.app.proxy.handle_record_service import handle_request_record, handle_response_record
from stoobly_agent.app.proxy.handle_test_service import handle_request_test, handle_response_test
from stoobly_agent.app.proxy.intercept_settings import InterceptSettings
from stoobly_agent.app.proxy.mock.context import MockContext
from stoobly_agent.app.proxy.replay.context import ReplayContext
from stoobly_agent.app.proxy.record.context import RecordContext
from stoobly_agent.app.proxy.utils.response_handler import bad_request
from stoobly_agent.app.settings import Settings
from stoobly_agent.config.constants import lifecycle_hooks, mode
from stoobly_agent.lib.cache import Cache
from stoobly_agent.lib.logger import Logger

# Disable proxy settings in urllib
os.environ['no_proxy'] = '*'

LOG_ID = 'Intercept'

cache = Cache.instance()
settings = Settings.instance()

scenario_model = ScenarioModel(settings)

def request(flow: 'MitmproxyHTTPFlow'):
    # Lazy import for runtime usage
    request: 'MitmproxyRequest' = flow.request

    __patch_cookie(request)

    intercept_settings = InterceptSettings(settings, request).with_cache(cache).with_scenario_model(scenario_model)
    if not intercept_settings.active:
        return

    __disable_web_cache(request)
    __disable_content_encoding(request)

    __intercept_hook(lifecycle_hooks.BEFORE_REQUEST, flow, intercept_settings)

    active_mode = intercept_settings.mode
    Logger.instance(LOG_ID).debug(f"ProxyMode: {active_mode}")

    if active_mode == mode.MOCK:
        context = MockContext(flow, intercept_settings)
        handle_request_mock(context)
    elif active_mode == mode.RECORD:
        context = ReplayContext(flow, intercept_settings)
        handle_request_record(context)
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

def response(flow: 'MitmproxyHTTPFlow'):
    request: 'MitmproxyRequest' = flow.request

    intercept_settings = InterceptSettings(settings, request).with_cache(cache).with_scenario_model(scenario_model)
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
def __disable_web_cache(request: 'MitmproxyRequest') -> None:
    request.headers['Cache-Control'] = 'no-cache, no-store'

# Disable response body returning as encoded e.g. gzip
def __disable_content_encoding(request: 'MitmproxyRequest') -> None:
    request.headers['Accept-Encoding'] = 'identity'

# Fix issue where multi-value cookies become comma separated
def __patch_cookie(request: 'MitmproxyRequest'):
    header_name = 'cookie'

    if len(request.headers.get_all(header_name)) > 1:
        __combine_header(request.headers, header_name, '; ')
        
def __combine_header(headers: 'Headers', header_name: str, delimitter: str):
    values = headers.get_all(header_name)
    headers[header_name] = delimitter.join(values)

def __intercept_hook(hook: str, flow: 'MitmproxyHTTPFlow', intercept_settings: InterceptSettings):
    lifecycle_hooks_module = intercept_settings.lifecycle_hooks

    if hook in lifecycle_hooks_module:
        lifecycle_hooks_module[hook](InterceptContext(flow, intercept_settings))