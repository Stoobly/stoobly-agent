import os
import pdb

from mitmproxy.http import HTTPFlow as MitmproxyHTTPFlow
from mitmproxy.net.http.request import Request as MitmproxyRequest
from stoobly_agent.app.proxy.handle_replay_service import handle_request_replay

from stoobly_agent.lib.logger import Logger
from stoobly_agent.app.settings import Settings

from stoobly_agent.app.proxy.handle_mock_service import handle_request_mock
from stoobly_agent.app.proxy.handle_record_service import handle_request_record, handle_response_record
from stoobly_agent.app.proxy.handle_test_service import handle_response_test
from stoobly_agent.config.constants import mode
from stoobly_agent.app.proxy.utils.response_handler import bad_request

from stoobly_agent.app.proxy.intercept_settings import InterceptSettings

# Disable proxy settings in urllib
os.environ['no_proxy'] = '*'

# Observe config for changes
Settings.instance().watch()

LOG_ID = 'InterceptHandler'

def request(flow: MitmproxyHTTPFlow):
    request: MitmproxyRequest = flow.request

    intercept_settings = InterceptSettings(Settings.instance(), request)

    active_mode = intercept_settings.mode
    Logger.instance().debug(f"{LOG_ID}:ProxyMode: {active_mode}")

    if active_mode == mode.MOCK:
        handle_request_mock(flow, intercept_settings)
    elif active_mode == mode.NONE:
        pass
    elif active_mode == mode.RECORD:
        __disable_web_cache(request)
        handle_request_record(request, intercept_settings)
    elif active_mode == mode.REPLAY or active_mode == mode.TEST:
        handle_request_replay(request, intercept_settings)
    else:
        return bad_request(
            flow,
            "Valid env MODES: %s, Got: %s" % ([mode.MOCK, mode.RECORD, mode.REPLAY, mode.TEST], active_mode)
        )

def response(flow: MitmproxyHTTPFlow):
    request: MitmproxyRequest = flow.request

    intercept_settings = InterceptSettings(Settings.instance(), request)

    active_mode = intercept_settings.mode

    if active_mode == mode.RECORD:
        return handle_response_record(flow, intercept_settings)
    elif active_mode == mode.TEST:
        return handle_response_test(flow, intercept_settings)

### PRIVATE

def __disable_web_cache(request: MitmproxyRequest) -> None:
    request.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    request.headers['Expires'] = '0'
    request.headers['Pragma'] = 'no-cache'

    if 'IF-NONE-MATCH' in request.headers:
        del request.headers['IF-NONE-MATCH']

    if 'IF-MODIFIED-SINCE' in request.headers:
        del request.headers['IF-MODIFIED-SINCE']


