import pdb

from typing import List, TypedDict

from stoobly_agent.app.proxy.test.response_param_names_facade import ResponseParamNamesFacade
from stoobly_agent.lib.api.interfaces.endpoints import ResponseParamName

class IMatchContext(TypedDict):
    lifecycle_hooks: dict
    path_key: str
    query: str
    response_param_names_facade: ResponseParamNamesFacade

class MatchContext():

    def __init__(self, context: IMatchContext):
        self.path_key = context['path_key']
        self.query = context['query']

        self.__lifecycle_hooks = context.get('lifecycle_hooks') # Optional
        self.__response_param_names_facade = context['response_param_names_facade']

    def to_dict(self) -> IMatchContext:
        return {
            'lifecycle_hooks': self.__lifecycle_hooks,
            'path_key': self.path_key,
            'query': self.query,
            'response_param_names_facade': self.__response_param_names_facade,
        }

    def clone(self):
        return __class__(self.to_dict())

    def visit_list(self, key):
        self.path_key = f"{self.path_key}[{key}]"
        self.query = f"{self.query}[*]"

    def visit_dict(self, key):
        self.path_key = '.'.join([self.path_key, key]) if len(self.path_key) > 0 else key
        self.query = '.'.join([self.query, key]) if len(self.query) > 0 else key

    def selected(self):
        return self.__response_param_names_facade.is_selected(self.query)

    def ignored(self, expected_value, actual_value):
        return not self.selected() or (not self.required() and self.__required_matches(expected_value, actual_value))

    def deterministic(self) -> bool:
        response_param_names_facade: ResponseParamNamesFacade = self.__response_param_names_facade
        if not response_param_names_facade or len(response_param_names_facade.all) == 0:
            return True

        query: str = self.query
        deterministic_param_names: ResponseParamName = response_param_names_facade.deterministic
        return self.__param_name_matches(query, deterministic_param_names)

    def required(self) -> bool:
        response_param_names_facade: ResponseParamNamesFacade = self.__response_param_names_facade
        if not response_param_names_facade or len(response_param_names_facade.all) == 0:
            return True

        query: str = self.query
        required_param_names: ResponseParamName = response_param_names_facade.required
        return self.__param_name_matches(query, required_param_names)

    ### Matchers

    def length_matches(self, v1, v2):
        handle_length_matches = self.__lifecyle_hook('handle_length_matches')

        if handle_length_matches:
            return handle_length_matches(self.clone(), v1, v2)
        else:
            return len(v1) == len(v2)

    def param_name_exists(self, key, actual):
        handle_param_name_exists = self.__lifecyle_hook('handle_param_name_exists')

        if handle_param_name_exists:
            return handle_param_name_exists(self.clone(), key, actual)
        else:
            return key in actual

    def value_fuzzy_matches(self, v1, v2):
        handle_fuzzy_matches = self.__lifecyle_hook('handle_fuzzy_matches')

        if handle_fuzzy_matches:
            return handle_fuzzy_matches(self.clone(), v1, v2)
        else:
            return type(v1) == type(v2)

    def value_matches(self, v1, v2):
        handle_value_matches = self.__lifecyle_hook('handle_value_matches')

        if handle_value_matches:
            return handle_value_matches(self.clone(), v1, v2)
        else:
            return v1 == v2

    def value_type_exists(self, value, valid_types: list):
        handle_type_exists = self.__lifecyle_hook('handle_type_exists')

        if handle_type_exists:
            return handle_type_exists(self.clone(), value, valid_types)
        else:
            return type(value) in valid_types

    def __lifecyle_hook(self, name):
        if not self.__lifecycle_hooks:
            return

        return self.__lifecycle_hooks.get(name)

    def __param_name_matches(self, query, param_names: List[ResponseParamName]) -> bool:
        for param_name in param_names:
            if param_name['query'] == query:
                return True

        return False

    def __required_matches(self, v1, v2):
        return v1 == None or v2 == None