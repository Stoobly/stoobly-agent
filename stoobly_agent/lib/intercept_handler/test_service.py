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
        status_matches = __test_status_code(flow, expected_res)
        response_matches = __test_diff(content, expected_content)
        score = status_score + latency_score + diff_score

        log_lines = []
        if not response_matches:
            log_lines.append('Response did not match')

        if not status_matches:
            log_lines.append('Status did not match')

        return status_matches and response_matches, "\n".join(log_lines)
    elif test_strategy == TEST_STRATEGIES['FUZZY']:
        status_matches = __test_status_code(flow, expected_res)
        fuzzy_matches, log = __test_fuzzy(content, expected_content)

        return status_matches and fuzzy_matches, log

def __test_status_code(flow: MitmproxyHTTPFlow, expected_res: Response) -> boolean:
    return flow.response.status_code == expected_res.status_code

def __test_diff(content: FuzzyContent, expected_content: FuzzyContent) -> boolean:
    return content == expected_content

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
