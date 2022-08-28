import pdb

from typing import List, Tuple, TypedDict

from .match_context import MatchContext
from .response_param_names_facade import ResponseParamNamesFacade

def dict_fuzzy_matches(expected: dict, actual: dict, response_param_names_facade: ResponseParamNamesFacade):
    context = MatchContext({ 'path_key': '', 'query': '', 'response_param_names_facade': response_param_names_facade })
    return __dict_fuzzy_matches(expected, actual, context)

def __dict_fuzzy_matches(expected: dict, actual: dict, parent_context: MatchContext) -> Tuple[bool, str]:
    for key, expected_value in expected.items():
        context = MatchContext(parent_context.to_dict())
        context.visit_dict(key)
        path_key = context.path_key

        if not __param_name_exists(key, actual):
            if not context.selected() or not context.required():
                continue 

            return __param_name_exists_error(path_key)

        actual_value = actual[key]
        if not __value_fuzzy_matches(actual_value, expected_value):
            if context.ignored(expected_value, actual_value):
                continue

            return __type_match_error(path_key, expected_value, actual_value)

        if type(actual_value) is dict:
            __dict_fuzzy_matches(expected_value, actual_value, context)
            continue

        if type(actual_value) is list:
            __list_fuzzy_matches(expected_value, actual_value, context)
            continue

    return True, ''

def list_fuzzy_matches(expected: dict, actual: dict, response_param_names_facade: ResponseParamNamesFacade):
    context = MatchContext({ 'path_key': '', 'query': '', 'response_param_names_facade': response_param_names_facade })
    return __list_fuzzy_matches(expected, actual, context)

###
#
# For list matching, look for all types in expected list
# Expect tested list to have a type that exists in expected list
#
# If list value is traversable, traverse
#
def __list_fuzzy_matches(expected: list, actual: list, parent_context: MatchContext) -> Tuple[bool, str]:
    valid_types = []
    type_examples = {}
    for i, value in enumerate(expected):
        valid_types.append(type(value))

        if type(value) is dict and str(dict) not in type_examples:
            type_examples[dict] = value
        elif type(value) is list and str(list) not in type_examples:
            type_examples[list] = value

    for i, value in enumerate(actual):
        context = MatchContext(parent_context.to_dict())
        context.visit_list(i)
        path_key = context.path_key

        if not __valid_value_type(value, valid_types):
            if not context.selected() or not context.required():
                continue

            return __valid_type_error(path_key, value, valid_types)

        if type(value) is dict:
            __dict_fuzzy_matches(type_examples[dict], value, context)
            continue

        if type(value) is list:
            __list_fuzzy_matches(type_examples[list], value, context)
            continue

    return True, ''

def dict_matches(expected: dict, actual: dict, response_param_names_facade: ResponseParamNamesFacade) -> Tuple[bool, str]:
    context = MatchContext({ 'path_key': '', 'query': '', 'response_param_names_facade': response_param_names_facade })
    return __dict_matches(expected, actual, context)

def __dict_matches(expected: dict, actual: dict, parent_context: MatchContext) -> Tuple[bool, str]:
    for key, expected_value in expected.items():
        context = MatchContext(parent_context.to_dict())
        context.visit_dict(key)
        path_key = context.path_key

        # Check if key exists in actual
        if not __param_name_exists(key, actual):
            if not context.selected() or not context.required():
                continue

            return __param_name_exists_error(path_key)

        # Check if types match 
        actual_value = actual[key]
        if not __value_fuzzy_matches(expected_value, actual_value):
            if context.ignored(expected_value, actual_value):
                continue

            return __type_match_error(path_key, expected_value, actual_value)

        if type(actual_value) is dict:
            __dict_matches(expected_value, actual_value, context)
            continue

        if type(actual_value) is list:
            __list_matches(expected_value, actual_value, context)
            continue

        # Check if value matches
        if not __value_matches(expected_value, actual_value):
            if context.ignored(expected_value, actual_value) or not context.deterministic():
                continue

            return __value_match_error(path_key, expected_value, actual_value)

    return True, ''

def list_matches(expected: dict, actual: dict, response_param_names_facade: ResponseParamNamesFacade) -> Tuple[bool, str]:
    context = MatchContext({ 'path_key': '', 'query': '', 'response_param_names_facade': response_param_names_facade })
    return __list_matches(expected, actual, context)

def __list_matches(expected: list, actual: list, parent_context: MatchContext) -> Tuple[bool, str]:
    if not __length_matches(expected, actual):
        if parent_context.deterministic() and parent_context.selected():
            return __length_match_error(parent_context.path_key, expected, actual)

    for i, expected_value in enumerate(expected):
        if i >= len(actual):
            break

        context = MatchContext(parent_context.to_dict())
        context.visit_list(i)
        path_key = context.path_key

        actual_value = actual[i]

        if not __value_fuzzy_matches(expected_value, actual_value):
            if context.ignored(expected_value, actual_value):
                continue

            return __type_match_error(path_key, expected_value, actual_value)

        if type(actual_value) is dict:
            __dict_matches(expected_value, actual_value, context)
            continue

        if type(actual_value) is list:
            __list_matches(expected_value, actual_value, context)
            continue

        if not __value_matches(actual_value, expected_value):
            if context.ignored(expected_value, actual_value) or not context.deterministic():
                continue

            return __value_match_error(path_key, expected_value, actual_value)

    return True, ''

### Matchers

def __length_matches(v1, v2):
    return len(v1) == len(v2)

def __param_name_exists(key, actual):
    return key in actual

def __value_fuzzy_matches(v1, v2):
    return type(v1) == type(v2)

def __value_matches(v1, v2):
    return v1 == v2

def __valid_value_type(value, valid_types: list):
    return type(value) in valid_types

### Match Errors

def __length_match_error(path_key, expected_value, actual_value):
    return False, f"Key '{path_key}' length did not match: got {len(actual_value)}, expected {len(expected_value)}"

def __param_name_exists_error(path_key):
    return False, f"Missing key: expected {path_key} to exist"

def __type_match_error(path_key, expected_value, actual_value):
    return False, f"Key '{path_key}' type did not match: got {type(actual_value)}, expected {type(expected_value)}"

def __valid_type_error(path_key, value, valid_types):
    return False, f"Key '{path_key}' type did not match: got {type(value)}, expected valid types {', '.join(valid_types)}"

def __value_match_error(path_key, expected_value, actual_value):
    return False, f"Key '{path_key}' did not match: got {actual_value}, expected {expected_value}"