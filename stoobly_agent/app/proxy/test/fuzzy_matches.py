import pdb

from typing import Tuple
from stoobly_agent.app.proxy.test.context import TestContext
from stoobly_agent.app.proxy.test.contract_matches import dict_matches, list_matches

from stoobly_agent.app.proxy.test.helpers.errors import param_name_missing_error, type_match_error, valid_type_error
from stoobly_agent.app.proxy.test.helpers.request_component_names_facade import RequestComponentNamesFacade

from .match_context import MatchContext, build_match_context

def matches(context: TestContext, facade: RequestComponentNamesFacade, expected, actual):
    match_context = build_match_context(context, facade)

    if type(expected) != type(actual):
        return type_match_error(match_context.path_key, expected, actual)

    if isinstance(actual, dict) and isinstance(actual, dict):
        return dict_matches(match_context, expected, actual)
    elif isinstance(actual, list):
        return list_matches(match_context, expected, actual)
    else:
        return value_matches(match_context, expected, actual)

def value_matches(parent_context: MatchContext, expected, actual):
    if not parent_context.value_fuzzy_matches(expected, actual):
        return type_match_error(parent_context.path_key, type(expected), (actual))
    return True, ''

def dict_matches(parent_context: MatchContext, expected: dict, actual: dict) -> Tuple[bool, str]:
    if type(actual) != dict:
        return type_match_error(parent_context.path_key, dict, type(actual))

    for key, expected_value in expected.items():
        context = MatchContext(parent_context.to_dict())
        context.visit_dict(key)
        path_key = context.path_key

        if not context.param_name_exists(key, actual):
            if not context.selected() or not context.required():
                continue 

            return param_name_missing_error(path_key)

        actual_value = actual[key]
        if not context.value_fuzzy_matches(actual_value, expected_value):
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

    return True, ''

###
#
# For list matching, look for all types in expected list
# Expect tested list to have a type that exists in expected list
#
# If list value is traversable, traverse
#
def list_matches(parent_context: MatchContext, expected: list, actual: list) -> Tuple[bool, str]:
    if type(actual) != list:
        return type_match_error(parent_context.path_key, list, type(actual))

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

            return valid_type_error(path_key, value, valid_types)

        if type(value) is dict:
            matches, log = dict_matches(context, type_examples[dict], value)
            if not matches:
                return matches, log
        elif type(value) is list:
            matches, log = list_matches(context, type_examples[list], value)
            if not matches:
                return matches, log

    return True, ''