from difflib import Match
import os
import pdb

from runpy import run_path
from typing import Union

from stoobly_agent.config.constants import test_strategy

from .iterable_matches import dict_fuzzy_matches, dict_matches, list_fuzzy_matches, list_matches
from ..test.context import TestContext

FuzzyContent = Union[dict, list, str]

class MatchHandlers():
    def __init__(self):
        self.dict_matches_handler = None
        self.list_matches_handler = None
        self.value_matches_handler = None

def test(context: TestContext):
    __before_test_hook(context)

    if context.skipped:
        return None, ''

    active_test_strategy = context.strategy

    if active_test_strategy == test_strategy.CUSTOM:
        context.passed, context.log = test_custom(context)
    elif active_test_strategy == test_strategy.DIFF or active_test_strategy == test_strategy.FUZZY:
        match_handlers = MatchHandlers()
        match_handlers.value_matches_handler = __value_matches

        if active_test_strategy == test_strategy.DIFF: 
            match_handlers.dict_matches_handler = dict_matches
            match_handlers.list_matches_handler = list_matches
        else:
            match_handlers.dict_matches_handler = dict_fuzzy_matches
            match_handlers.list_matches_handler = list_fuzzy_matches

        status_code_matches, status_code_log = __test_status_code(context)
        response_matches, log = test_default(context, match_handlers)

        log_lines = []
        if not response_matches:
            log_lines.append(log)

        if not status_code_matches:
            log_lines.append(status_code_log)

        context.passed = status_code_matches and response_matches, 
        context.log = "\n".join(log_lines)
    else:
        test_strategies = ','.join([test_strategy.CUSTOM, test_strategy.DIFF, test_strategy.FUZZY])
        context.passed = False
        context.log = f"Could not find matching test strategy: valid options [{test_strategies}]"

    __after_test_hook(context)

    return context.passed, context.log

#
# Defaults to diff if content is not traversable
#
def test_default(context: TestContext, match_handlers: MatchHandlers):
    response = context.response
    content: FuzzyContent = response.decode_content()

    expected_content: FuzzyContent = context.rewritten_expected_response_content

    if __is_traversable(content) and __is_traversable(expected_content):
        if type(content) != type(expected_content):
            return False, f"Expected types to match: got {type(content)}, expected {type(expected_content)}"
        else:
            if type(content) == dict:
                return match_handlers.dict_matches_handler(expected_content, content, context.response_param_names)
            elif type(content) == list:
                return match_handlers.list_matches_handler(expected_content, content, context.response_param_names)
    else:
        response_matches = match_handlers.value_matches_handler(content, expected_content)
        log_lines = []

        if not response_matches:
            log_lines.append('Response did not match')

        return response_matches, "\n".join(log_lines)

def test_custom(context: TestContext):
    script_path = __lifecycle_hooks_path(context)

    if not script_path:
        return False, f"Lifecycle script path not set"

    if not os.path.isabs(script_path):
        script_path = os.path.join(os.path.abspath('.'), script_path)

    if not os.path.exists(script_path):
        return False, f"Expected {script_path} to exist"

    try:
        module = run_path(script_path)
    except Exception as e:
        return False, f"Exception: {e}"

    if not 'handle_test' in module:
        return False, f"Expected function 'handle_test' to be defined in {script_path}"

    try:
        status, log = module['handle_test'](context)
    except Exception as e:
        return False, f"Exception: {e}"

    if not type(status) is bool or not type(log) is str:
        return False, f"Expected function 'test' to return [bool, str], got [{type(status)}, {type(log)}]"

    return status, log

def __test_status_code(context: TestContext) -> bool:
    response = context.response
    expected_response = context.expected_response

    matches = response.status_code == expected_response.status_code 

    log = ''
    if not matches:
        log = f"Status codes did not match: got {response.status_code} expected {expected_response.status_code}"

    return matches, log

def __value_matches(content: FuzzyContent, expected_content: FuzzyContent) -> bool:
    return content == expected_content

def __is_traversable(content: FuzzyContent):
    return type(content) is dict or type(content) is list

def __lifecycle_hooks_path(context: TestContext):
    if not context.lifecycle_hooks:
        return

    script_path = context.lifecycle_hooks_script_path

    if not os.path.isabs(script_path):
        script_path = os.path.join(os.path.abspath('.'), script_path)

    return script_path

def __after_test_hook(context: TestContext):
    lifecycle_hooks = context.lifecycle_hooks 

    if not 'handle_after_test' in lifecycle_hooks:
        return

    lifecycle_hooks['handle_after_test'](context)

def __before_test_hook(context: TestContext):
    lifecycle_hooks = context.lifecycle_hooks 

    if not 'handle_after_test' in lifecycle_hooks:
        return

    lifecycle_hooks['handle_before_test'](context)