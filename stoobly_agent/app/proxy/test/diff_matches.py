import pdb

from typing import Tuple

from stoobly_agent.app.proxy.test.helpers.errors import length_match_error, param_name_missing_error, type_match_error, value_match_error

from .match_context import MatchContext

def dict_matches(parent_context: MatchContext, expected: dict, actual: dict) -> Tuple[bool, str]:
    if type(actual) != dict:
        return type_match_error(parent_context.path_key, dict, type(actual))

    for key, expected_value in expected.items():
        context = MatchContext(parent_context.to_dict())
        context.visit_dict(key)
        path_key = context.path_key

        # Check if key exists in actual
        if not context.param_name_exists(key, actual):
            if not context.selected() or not context.required():
                continue

            return param_name_missing_error(path_key)

        # Check if types match 
        actual_value = actual[key]
        if not context.value_fuzzy_matches(expected_value, actual_value):
            if context.ignored(expected_value, actual_value):
                continue

            return type_match_error(path_key, type(expected_value), type(actual_value))

        if type(actual_value) is dict:
            matches, log = dict_matches(context, expected_value, actual_value)
            if not matches:
                return matches, log
        elif type(actual_value) is list:
            matches, log = list_matches(context, expected_value, actual_value)
            if not matches:
                return matches, log
        else:
            # Check if value matches
            if not context.value_matches(expected_value, actual_value):
                if context.ignored(expected_value, actual_value) or not context.deterministic():
                    continue

                return value_match_error(path_key, expected_value, actual_value)

    return True, ''

def list_matches(parent_context: MatchContext, expected: list, actual: list) -> Tuple[bool, str]:
    if type(actual) != list:
        return type_match_error(parent_context.path_key, list, type(actual))

    if not parent_context.length_matches(expected, actual):
        if parent_context.deterministic() and parent_context.selected():
            return length_match_error(parent_context.path_key, expected, actual)
    
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

            return type_match_error(path_key, type(expected_value), type(actual_value))

        if type(actual_value) is dict:
            matches, log = dict_matches(context, expected_value, actual_value)
            if not matches:
                return matches, log
        elif type(actual_value) is list:
            matches, log = list_matches(context, expected_value, actual_value)
            if not matches:
                return matches, log
        else:
            if not context.value_matches(actual_value, expected_value):
                if context.ignored(expected_value, actual_value) or not context.deterministic():
                    continue

                return value_match_error(path_key, expected_value, actual_value)

    return True, ''