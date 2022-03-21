import os
import pdb

from mitmproxy.http import HTTPFlow as MitmproxyHTTPFlow
from mitmproxy.net.http.request import Request as MitmproxyRequest

from stoobly_agent.lib.logger import Logger
from stoobly_agent.app.settings import Settings

from stoobly_agent.app.proxy.handle_mock_service import handle_request_mock
from stoobly_agent.app.proxy.handle_record_service import handle_request_record, handle_response_record
from stoobly_agent.app.proxy.handle_test_service import handle_request_test
from stoobly_agent.config.constants import mode
from stoobly_agent.app.proxy.utils.response_handler import bad_request
from stoobly_agent.app.proxy.settings import get_proxy_mode

# Disable proxy settings in urllib
os.environ['no_proxy'] = '*'

# Observe config for changes
Settings.instance().observe_config()

LOG_ID = 'InterceptHandler'

def request(flow: MitmproxyHTTPFlow):
    request: MitmproxyRequest = flow.request

    __disable_web_cache(request)

    settings = Settings.instance()
    active_mode = get_proxy_mode(request.headers, settings)

    Logger.instance().debug(f"{LOG_ID}:ProxyMode: {mode}")

    if active_mode == mode.MOCK:
        handle_request_mock(flow, settings)
    elif active_mode == mode.NONE:
        pass
    elif active_mode == mode.RECORD:
        handle_request_record(request, settings)
    elif active_mode == mode.TEST:
        pass
    else:
        return bad_request(
            flow,
            "Valid env MODES: %s, Got: %s" % ([mode.RECORD, mode.MOCK, mode.TEST], active_mode)
        )

def response(flow: MitmproxyHTTPFlow):
    request: MitmproxyRequest = flow.request
    settings = Settings.instance()

    active_mode = get_proxy_mode(request.headers, settings)

    if active_mode == mode.RECORD:
        return handle_response_record(flow, settings)
    elif active_mode == mode.TEST:
        return handle_request_test(flow, settings)
    else:
        return False

### PRIVATE

def __disable_web_cache(request: MitmproxyRequest) -> None:
    request.headers['CACHE-CONTROL'] = 'no-cache'

    if 'IF-NONE-MATCH' in request.headers:
        del request.headers['IF-NONE-MATCH']

