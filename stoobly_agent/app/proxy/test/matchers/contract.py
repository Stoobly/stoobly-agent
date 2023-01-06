import pdb

from typing import List, Tuple, TypedDict, Union

from stoobly_agent.app.proxy.test.helpers.request_component_names_facade import RequestComponentNamesFacade
from stoobly_agent.lib.api.interfaces.endpoints import RequestComponentName

from ..context import TestContext
from .context import MatchContext, build_match_context
from .errors import length_match_error, param_name_exists_error, param_name_missing_error, type_match_error, valid_type_error

class Options(TypedDict):
    strict: bool

def matches(test_context: TestContext, facade: RequestComponentNamesFacade, actual, **options: Options):
    context = build_match_context(test_context, facade)

    if context.value_is_dict(actual):
        return dict_matches(context, actual, **options)
    elif context.value_is_list(actual):
        return list_matches(context, actual, **options)
    else:
        # TODO: handle non-traversible content
        return True, ''

def dict_matches(parent_context: MatchContext, actual: dict, **options: Options) -> Tuple[bool, str]:
    if not parent_context.value_is_dict(actual):
        return type_match_error(parent_context.path_key, dict, type(actual))

    index = parent_context.request_component_names_query_index
    component_names = parent_context.children

    for key, actual_value in actual.items():
        context = MatchContext(parent_context.to_dict())
        context.visit_dict(key)

        path_key = context.path_key
        query = context.query

        if query not in index:
            if not options.get('strict'):
                continue
            else:
                return param_name_exists_error(path_key)
        
        contracts = index[query]
        if not context.value_contract_matches(actual_value, contracts):
            if context.ignored(actual_value, actual_value): # Might look weird, but expected_value == actual_value is fine here
                continue
            
            valid_types = __build_valid_types(contracts)
            return valid_type_error(path_key, actual_value, valid_types)

        if context.value_is_dict(actual_value):
            matches, log = dict_matches(context, actual_value, **options)
            if not matches:
                return matches, log
        elif context.value_is_list(actual_value):
            matches, log = list_matches(context, actual_value, **options)
            if not matches:
                return matches, log

    # Check all properties required by contract exist
    for component_name in component_names:
        key = component_name['name']
        if not key in actual:
            context = MatchContext(parent_context.to_dict())
            context.visit_dict(key)
            return param_name_missing_error(context.path_key)

    return True, ''

###
#
# For list matching, look for all types in expected list
# Expect tested list to have a type that exists in expected list
#
# If list value is traversable, traverse
#
def list_matches(parent_context: MatchContext, actual: list, **options: Options) -> Tuple[bool, str]:
    parent_path_key = f"{parent_context.path_key}[*]"
    if not parent_context.value_is_list(actual):
        return type_match_error(parent_path_key, list, type(actual))

    index = parent_context.request_component_names_query_index
    contracts: List[RequestComponentName] = index.get(parent_path_key) or []

    # If required, make sure not empty 
    if parent_context.required and len(actual) == 0 and len(contracts) > 0:
        return length_match_error(parent_path_key, None, actual) 

    valid_types = __build_valid_types(contracts)

    for i, value in enumerate(actual):
        context = MatchContext(parent_context.to_dict())
        context.visit_list(i)
        path_key = context.path_key

        if not context.value_contract_matches(value, contracts):
            if not context.selected() or not context.required():
                continue

            return valid_type_error(path_key, value, valid_types)

        if context.value_is_dict(value):
            matches, log = dict_matches(context, value, **options)
            if not matches:
                return matches, log
        elif context.value_is_list(value):
            matches, log = list_matches(context, value, **options)
            if not matches:
                return matches, log

    return True, ''

def __build_valid_types(contracts: Union[None, RequestComponentName, List[RequestComponentName]]):
    valid_types = []
    if contracts:
        if not isinstance(contracts, list):
            contracts = [contracts]

        valid_types = list(map(lambda contract: contract.get('inferred_type'), contracts))
    return valid_types