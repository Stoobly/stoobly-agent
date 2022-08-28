from stoobly_agent.app.proxy.test.response_param_names_facade import ResponseParamNamesFacade
from stoobly_agent.lib.api.interfaces.endpoints import ResponseParamName

class IMatchContext(TypedDict):
    path_key: str
    query: str
    response_param_names_facade: ResponseParamNamesFacade

class MatchContext():

    def __init__(self, context: IMatchContext):
        self.path_key = context['path_key']
        self.query = context['query']
        self.__response_param_names_facade = context['response_param_names_facade']

    def to_dict(self) -> IMatchContext:
        return {
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

    def __param_name_matches(query, param_names: List[ResponseParamName]) -> bool:
        for param_name in param_names:
            if param_name['query'] == query:
                return True

        return False

    def __required_matches(v1, v2):
        return v1 == None or v2 == None