import os
import pdb

from runpy import run_path
from typing import Union

from stoobly_agent.config.constants import test_strategy
from stoobly_agent.config.constants.env_vars import TEST_SCRIPT

from .iterable_matches import dict_matches, list_matches
from ..test.context import TestContext

FuzzyContent = Union[dict, list, str]

def test(context: TestContext):
    active_test_strategy = context.strategy

    if active_test_strategy == test_strategy.CUSTOM:
        return __test_custom(context)
    elif active_test_strategy == test_strategy.DIFF:
        status_code_matches, status_code_log = __test_status_code(context)
        response_matches = test_diff(context)

        log_lines = []
        if not response_matches:
            log_lines.append('Response did not match: please check diff')

        if not status_code_matches:
            log_lines.append(status_code_log)

        return status_code_matches and response_matches, "\n".join(log_lines)
    elif active_test_strategy == test_strategy.FUZZY:
        status_code_matches, status_code_log = __test_status_code(context)
        fuzzy_matches, log = test_fuzzy(context)

        log_lines = []
        if not fuzzy_matches:
            log_lines.append(log)

        if not status_code_matches:
            log_lines.append(status_code_log)

        return status_code_matches and fuzzy_matches, "\n".join(log_lines)
    else:
        test_strategies = ','.join([test_strategy.CUSTOM, test_strategy.DIFF, test_strategy.FUZZY])
        return False, f"Could not find matching test strategy: valid options [{test_strategies}]"

def test_diff(context: TestContext):
    response = context.response
    content: FuzzyContent = response.content
    expected_response = context.expected_response
    expected_content: FuzzyContent = expected_response.content
    return __test_diff(content, expected_content)

def test_fuzzy(context: TestContext):
    response = context.response
    expected_response = context.expected_response
    return __test_fuzzy(response.decode_content(), expected_response.decode_content())

def __test_status_code(context: TestContext) -> bool:
    response = context.response
    expected_response = context.expected_response

    matches = response.status_code == expected_response.status_code 

    log = ''
    if not matches:
        log = f"Status codes did not match: got {response.status_code} expected {expected_response.status_code}"

    return matches, log

def __test_diff(content: FuzzyContent, expected_content: FuzzyContent) -> bool:
    return content == expected_content

#
# Defaults to diff if content is not traversable
#
def __test_fuzzy(content: FuzzyContent, expected_content: FuzzyContent):
    if __is_traversable(content) and __is_traversable(expected_content):
        if type(content) != type(expected_content):
            return False, f"Expected types to match: got {type(content)}, expected {type(expected_content)}"
        else:
            if type(content) == dict:
                return dict_matches(expected_content, content, '')
            elif type(content) == list:
                return list_matches(expected_content, content, '')
    else:
        response_matches = __test_diff(content, expected_content)
        log_lines = []

        if not response_matches:
            log_lines.append('Response did not match')

        return response_matches, "\n".join(log_lines)

def __test_custom(context: TestContext):
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
