import pdb

from stoobly_agent.app.proxy.replay.body_parser_service import decode_response, normalize_header

from stoobly_agent.config.constants import test_strategy

from .context import TestContext
from .matchers.custom import matches as custom_matches
from .matchers.contract import matches as contract_matches
from .matchers.diff import matches as diff_matches
from .matchers.fuzzy import matches as fuzzy_matches

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
    response_matches, log = __test_response(context) 

    __after_test_hook(context)

    # Format test results
    log_lines = []

    if not contract_matches:
        log_lines.append(f"\n=== Contract Test ===")
        log_lines.append(contract_log)

    if not status_code_matches:
        log_lines.append(f"\n=== Status Code Test ===")
        log_lines.append(status_code_log)

    if not response_matches:
        log_lines.append(f"\n=== Response Test ===")
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

# Tests

def __test_request_contract(context: TestContext):
    endpoint = context.endpoint

    if not endpoint:
        return True, ''
 
    request = context.flow.request

    headers = context.request_headers
    normalized_headers = {k.lower(): v for k, v in headers.items()} # Headers are case insensitive
    header_names_facade = endpoint.header_names
    matches, log = contract_matches(context, header_names_facade, normalized_headers)
    if not matches:
        return matches, f"{log} in headers"

    query_params = request.query
    query_param_names_facade = endpoint.query_param_names
    matches, log = contract_matches(context, query_param_names_facade, query_params, strict=True)
    if not matches:
        return matches, f"{log} in query params" 

    body_params = decode_response(request.content, headers.get('content-type'))
    body_param_names_facade = endpoint.body_param_names
    matches, log = contract_matches(context, body_param_names_facade, body_params, strict=True)
    if not matches:
        return matches, f"{log} in body params" 

    return True, ''

# TODO
def __test_response_headers(context):
    return True, ''

def __test_response(context: TestContext):
    active_test_strategy = context.strategy
    content = context.decoded_response_content
    expected_content = context.rewritten_expected_response_content
    response_param_names_facade = context.response_param_names

    if active_test_strategy == test_strategy.DIFF: 
        return diff_matches(context, response_param_names_facade, expected_content, content)
    elif active_test_strategy == test_strategy.FUZZY:
        return fuzzy_matches(context, response_param_names_facade, expected_content, content)
    elif active_test_strategy == test_strategy.CUSTOM:
        return custom_matches(context)
    elif active_test_strategy == test_strategy.CONTRACT:
        return contract_matches(context, response_param_names_facade, content)
    else:
        raise 'Setting Error: missing test test strategy'

def __test_status_code(context: TestContext) -> bool:
    response = context.response
    expected_response = context.expected_response

    matches = response.status_code == expected_response.status_code 

    log = ''
    if not matches:
        log = f"Status codes did not match: got {response.status_code} expected {expected_response.status_code}"

    return matches, log

# Hooks

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