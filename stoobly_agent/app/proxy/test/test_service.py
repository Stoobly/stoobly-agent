import os
import pdb

from runpy import run_path
from typing import Callable, Union
from stoobly_agent.app.proxy.replay.body_parser_service import decode_response

from stoobly_agent.config.constants import test_strategy

from .context import TestContext
from .matchers.contract import matches as contract_matches
from .matchers.diff import matches as diff_matches
from .matchers.fuzzy import matches as fuzzy_matches

FuzzyContent = Union[dict, list, str]

def test(context: TestContext):
    __before_test_hook(context)

    if context.skipped:
        return None, ''

    valid_test_strategy, log = __validate_test_strategy(context)
    if not valid_test_strategy:
        __after_test_hook(context)
        return False, log
    
    # Test contract
    contract_matches, contract_log = __test_request_contract(context)

    # Test status code
    status_code_matches, status_code_log = __test_status_code(context)
    
    # Test response
    active_test_strategy = context.strategy
    if active_test_strategy == test_strategy.CUSTOM:
        response_matches, log = __test_custom(context)
    else:
        match_handler = None

        if active_test_strategy == test_strategy.DIFF: 
            match_handler = diff_matches
        elif active_test_strategy == test_strategy.FUZZY:
            match_handler = fuzzy_matches

        response_matches, log = __test_default(context, match_handler)

    __after_test_hook(context)

    # Format test results
    log_lines = []

    if not contract_matches:
        log_lines.append(contract_log)

    if not status_code_matches:
        log_lines.append(status_code_log)

    if not response_matches:
        log_lines.append(log)

    context.log = "\n".join(log_lines)
    context.passed = status_code_matches and contract_matches and response_matches 

    return context.passed, context.log

def __validate_test_strategy(context: TestContext):
    valid_strategies = [test_strategy.CUSTOM, test_strategy.DIFF, test_strategy.FUZZY]
    active_test_strategy = context.strategy

    if active_test_strategy not in valid_strategies:
        test_strategies = ','.join(valid_strategies)
        return False, f"Could not find matching test strategy: valid options [{test_strategies}]"

    return True, ''

def __test_request_contract(context: TestContext):
    endpoint = context.endpoint

    if not endpoint:
        return True, ''

    request = context.flow.request

    headers = request.headers
    header_names_facade = endpoint.header_names
    matches, log = contract_matches(context, header_names_facade, headers)
    if not matches:
        return matches, log

    query_params = request.query
    query_param_names_facade = endpoint.query_param_names
    matches, log = contract_matches(context, query_param_names_facade, query_params)
    if not matches:
        return matches, log

    body_params = decode_response(request.content, headers.get('content-type'))
    body_param_names_facade = endpoint.body_param_names
    matches, log = contract_matches(context, body_param_names_facade, body_params)
    if not matches:
        return matches, log

    return True, ''

def __test_default(context: TestContext, match_handler: Callable):
    response = context.response
    content: FuzzyContent = response.decode_content()
    expected_content: FuzzyContent = context.rewritten_expected_response_content

    return match_handler(context, context.response_param_names, expected_content, content)

def __test_custom(context: TestContext):
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