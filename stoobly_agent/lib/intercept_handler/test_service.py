import os
import pdb

from mitmproxy.http import HTTPFlow as MitmproxyHTTPFlow
from requests import Response
from runpy import run_path
from typing import NewType, Union

from ..env_vars import TEST_SCRIPT
from .iterable_matches import dict_matches, list_matches

TEST_STRATEGIES = {
    'CUSTOM': 'custom',
    'DIFF': 'diff',
    'FUZZY': 'fuzzy',
}

FuzzyContent = Union[dict, list, str]

def test(flow: MitmproxyHTTPFlow, expected_res: Response, test_strategy):
    expected_content = expected_res.content

    response = flow.response
    content = response.content

    if test_strategy == TEST_STRATEGIES['CUSTOM']:
        return __test_custom(flow, expected_res)
    elif test_strategy == TEST_STRATEGIES['DIFF']:
        return __test_diff(content, expected_content)
    elif test_strategy == TEST_STRATEGIES['FUZZY']:
        return __test_fuzzy(content, expected_content)

def __test_diff(content: FuzzyContent, expected_content: FuzzyContent):
    matches = content == expected_content
    return matches, ''

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

def __test_custom(flow: MitmproxyHTTPFlow, expected_res: Response):
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
        status, log = module['test'](flow, expected_res)
    except Exception as e:
        return False, f"Exception: {e}"

    if not type(status) is bool or not type(log) is str:
        return False, f"Expected function 'test' to return [bool, str], got [{type(status)}, {type(log)}]"

    return status, log

def __is_traversable(content: FuzzyContent):
    return type(content) is dict or type(content) is list