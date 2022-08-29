import pdb

from typing import List, Tuple, TypedDict

from .context import TestContext
from .match_context import MatchContext

def dict_fuzzy_matches(context: TestContext, expected: dict, actual: dict):
    match_context = __initialize_match_context(context)

    return __dict_fuzzy_matches(match_context, expected, actual)

def __dict_fuzzy_matches(parent_context: MatchContext, expected: dict, actual: dict) -> Tuple[bool, str]:
    for key, expected_value in expected.items():
        context = MatchContext(parent_context.to_dict())
        context.visit_dict(key)
        path_key = context.path_key

        if not context.param_name_exists(key, actual):
            if not context.selected() or not context.required():
                continue 

            return __param_name_exists_error(path_key)

        actual_value = actual[key]
        if not context.value_fuzzy_matches(actual_value, expected_value):
            if context.ignored(expected_value, actual_value):
                continue

            return __type_match_error(path_key, expected_value, actual_value)

        if type(actual_value) is dict:
            __dict_fuzzy_matches(context, expected_value, actual_value)
            continue

        if type(actual_value) is list:
            __list_fuzzy_matches(context, expected_value, actual_value)
            continue

    return True, ''

def list_fuzzy_matches(context: TestContext, expected: dict, actual: dict):
    match_context = __initialize_match_context(context)

    return __list_fuzzy_matches(expected, actual, match_context)

###
#
# For list matching, look for all types in expected list
# Expect tested list to have a type that exists in expected list
#
# If list value is traversable, traverse
#
def __list_fuzzy_matches(parent_context: MatchContext, expected: list, actual: list) -> Tuple[bool, str]:
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

        if not context.value_type_exists(value, valid_types):
            if not context.selected() or not context.required():
                continue

            return __valid_type_error(path_key, value, valid_types)

        if type(value) is dict:
            __dict_fuzzy_matches(context, type_examples[dict], value)
            continue

        if type(value) is list:
            __list_fuzzy_matches(context, type_examples[list], value)
            continue

    return True, ''

def dict_matches(context: TestContext, expected: dict, actual: dict) -> Tuple[bool, str]:
    match_context = __initialize_match_context(context)

    return __dict_matches(match_context, expected, actual)

def __dict_matches(parent_context: MatchContext, expected: dict, actual: dict) -> Tuple[bool, str]:
    for key, expected_value in expected.items():
        context = MatchContext(parent_context.to_dict())
        context.visit_dict(key)
        path_key = context.path_key

        # Check if key exists in actual
        if not context.param_name_exists(key, actual):
            if not context.selected() or not context.required():
                continue

            return __param_name_exists_error(path_key)

        # Check if types match 
        actual_value = actual[key]
        if not context.value_fuzzy_matches(expected_value, actual_value):
            if context.ignored(expected_value, actual_value):
                continue

            return __type_match_error(path_key, expected_value, actual_value)

        if type(actual_value) is dict:
            __dict_matches(context, expected_value, actual_value)
            continue

        if type(actual_value) is list:
            __list_matches(context, expected_value, actual_value)
            continue

        # Check if value matches
        if not context.value_matches(expected_value, actual_value):
            if context.ignored(expected_value, actual_value) or not context.deterministic():
                continue

            return __value_match_error(path_key, expected_value, actual_value)

    return True, ''

def list_matches(context: TestContext, expected: dict, actual: dict) -> Tuple[bool, str]:
    match_context = __initialize_match_context(context)

    return __list_matches(match_context, expected, actual)

def __list_matches(parent_context: MatchContext, expected: list, actual: list) -> Tuple[bool, str]:
    if not parent_context.length_matches(expected, actual):
        if parent_context.deterministic() and parent_context.selected():
            return __length_match_error(parent_context.path_key, expected, actual)

    for i, expected_value in enumerate(expected):
        if i >= len(actual):
            break

        context = MatchContext(parent_context.to_dict())
        context.visit_list(i)
        path_key = context.path_key

        actual_value = actual[i]

        if not context.value_fuzzy_matches(expected_value, actual_value):
            if context.ignored(expected_value, actual_value):
                continue

            return __type_match_error(path_key, expected_value, actual_value)

        if type(actual_value) is dict:
            __dict_matches(context, expected_value, actual_value)
            continue

        if type(actual_value) is list:
            __list_matches(context, expected_value, actual_value)
            continue

        if not context.value_matches(actual_value, expected_value):
            if context.ignored(expected_value, actual_value) or not context.deterministic():
                continue

            return __value_match_error(path_key, expected_value, actual_value)

    return True, ''

def __initialize_match_context(context: TestContext):
    return MatchContext({ 
        'lifecycle_hooks': context.lifecycle_hooks,
        'path_key': '', 
        'query': '', 
        'response_param_names_facade': context.response_param_names
    })

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