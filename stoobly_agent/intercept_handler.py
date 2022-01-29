import importlib
import os
import pdb

import lib

from lib.intercept_handler.handle_mock_service import handle_request_mock
from lib.intercept_handler.handle_record_service import handle_request_record, handle_response_record
from lib.intercept_handler.handle_test_service import handle_request_test
from lib.intercept_handler.modes import MODES
from lib.intercept_handler.response_handler import bad_request
from lib.intercept_handler.settings import get_proxy_mode
from lib.logger import Logger
from lib.settings import Settings

# mitmproxy only hot reloads the main script, manually hot reload lib
importlib.reload(lib.intercept_handler)
importlib.reload(lib.logger)
importlib.reload(lib.settings)
importlib.reload(lib.stoobly_api)

# Disable proxy settings in urllib
os.environ['no_proxy'] = '*'

# Observe config for changes
Settings.instance().observe_config()

LOG_ID = 'InterceptHandler'

def request(flow):
    request = flow.request

    __disable_web_cache(request)

    settings = Settings.instance()
    mode = get_proxy_mode(request.headers, settings)

    Logger.instance().debug(f"{LOG_ID}:ProxyMode: {mode}")

    if mode == MODES['MOCK']:
        handle_request_mock(flow, settings)
    elif mode == MODES['NONE']:
        pass
    elif mode == MODES['RECORD']:
        handle_request_record(request, settings)
    elif mode == MODES['TEST']:
        pass
    else:
        return bad_request(
            flow,
            "Valid env MODES: %s, Got: %s" % ([MODES['RECORD'], MODES['MOCK'], MODES['TEST']], mode)
        )

def response(flow):
    request = flow.request
    settings = Settings.instance()

    mode = get_proxy_mode(request.headers, settings)

    if mode == MODES['RECORD']:
        return handle_response_record(flow, settings)
    elif mode == MODES['TEST']:
        return handle_request_test(flow, settings)
    else:
        return False

### PRIVATE

def __disable_web_cache(request):
    request.headers['CACHE-CONTROL'] = 'no-cache'

    if 'IF-NONE-MATCH' in request.headers:
        del request.headers['IF-NONE-MATCH']

