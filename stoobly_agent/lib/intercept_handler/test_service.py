import math
import os
import pdb
import time

from mitmproxy.http import HTTPFlow as MitmproxyHTTPFlow
from requests import Response
from runpy import run_path
from typing import Union

from ..env_vars import TEST_SCRIPT
from .custom_headers import CUSTOM_HEADERS
from .iterable_matches import dict_matches, list_matches
from .mock_context import MockContext

TEST_STRATEGIES = {
    'CUSTOM': 'custom',
    'DIFF': 'diff',
    'FUZZY': 'fuzzy',
}

FuzzyContent = Union[dict, list, str]

def test(test_strategy: str, context: MockContext):
    flow = context.flow
    expected_res = context.response
    start_time = context.start_time

    response = flow.response
    content: FuzzyContent = response.content
    expected_content: FuzzyContent = expected_res.content

    if test_strategy == TEST_STRATEGIES['CUSTOM']:
        return __test_custom(context)
    elif test_strategy == TEST_STRATEGIES['DIFF']:
        status_score = __test_status_code(flow, expected_res)
        latency_score = __test_latency(start_time, expected_res)
        diff_score, log = __test_diff(content, expected_content)
        score = status_score + latency_score + diff_score
        return score, log
    elif test_strategy == TEST_STRATEGIES['FUZZY']:
        status_score = __test_status_code(flow, expected_res)
        latency_score = __test_latency(start_time, expected_res)
        fuzzy_score, log = __test_fuzzy(content, expected_content)
        score = status_score + latency_score + fuzzy_score
        return score, log

def __test_status_code(flow: MitmproxyHTTPFlow, expected_res: Response):
    status_matches = flow.response.status_code == expected_res.status_code
    if status_matches:
        return 30
    
    return 0

def __test_latency(start_time: float, expected_res: Response):
    latency = time.time() - start_time
    
    expected_latency = expected_res.headers.get(CUSTOM_HEADERS['RESPONSE_LATENCY'])
    if not expected_latency:
        expected_latency = 0
    else:
        expected_latency = float(expected_latency)

    if latency > expected_latency:
        percent_diff = (latency - expected_latency) / expected_latency
        return math.floor(10 * percent_diff)
    else:
        return 10

def __test_diff(content: FuzzyContent, expected_content: FuzzyContent):
    score = 0
    content_matches = content == expected_content
    if content_matches:
        score += 60

    return score, ''

#
# Defaults to diff if content is not traversable
#
def __test_fuzzy(content: FuzzyContent, expected_content: FuzzyContent):
    if __is_traversable(content) and __is_traversable(expected_content):
        if type(content) != type(expected_content):
            return False, f"Expected types to match, got {type(content)}, expected {type(expected_content)}"
        else:
            if type(content) == dict:
                return dict_matches(expected_content, content, '')
            elif type(content) == list:
                return list_matches(expected_content, content, '')
    else:
        return __test_diff(content, expected_content)

def __test_custom(context: MockContext):
    if not TEST_SCRIPT in os.environ:
        return False, f"Please use arg '--test-script <PATH>' when starting the agent"

    script_path = os.environ[TEST_SCRIPT]

    if not os.path.isabs(script_path):
        script_path = os.path.join(os.path.abspath('.'), script_path)

    if not os.path.exists(script_path):
        return False, f"Expected {script_path} to exist"

    try:
        module = run_path(script_path)
    except Exception as e:
        return False, f"Exception: {e}"

    if not 'test' in module:
        return False, f"Expected function 'test' to be defined in {script_path}"

    try:
        status, log = module['test'](context)
    except Exception as e:
        return False, f"Exception: {e}"

    if not type(status) is bool or not type(log) is str:
        return False, f"Expected function 'test' to return [bool, str], got [{type(status)}, {type(log)}]"

    return status, log

def __is_traversable(content: FuzzyContent):
    return type(content) is dict or type(content) is list
