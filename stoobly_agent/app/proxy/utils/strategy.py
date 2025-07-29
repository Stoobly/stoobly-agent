import pdb

from stoobly_agent.app.proxy.intercept_settings import InterceptSettings
from stoobly_agent.app.settings.constants import intercept_mode
from stoobly_agent.config.constants import request_origin


def get_active_mode_strategy(intercept_settings: InterceptSettings) -> str:
    strategy = ""

    if intercept_settings.mode == intercept_mode.RECORD:
        strategy = intercept_settings.record_strategy
    elif intercept_settings.mode == intercept_mode.TEST:
        strategy = intercept_settings.test_strategy

    return strategy
