import pdb

from stoobly_agent.app.api.simple_http_request_handler import SimpleHTTPRequestHandler
from stoobly_agent.app.models.query_param_model import QueryParamModel
from stoobly_agent.app.settings import Settings

class QueryParamsController:
    _instance = None

    def __init__(self):
        if self._instance:
            raise RuntimeError('Call instance() instead')
        else:
            self.data = {}

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()

        return cls._instance

    # GET /requests/:requestId/query_params
    def index(self, context):
        context.parse_path_params({
            'requestId': 1
        })

        query_param_model = self.__query_param_model(context)
        requests = query_param_model.index(context.params.get('requestId'), **context.params)

        context.render(
            json = requests,
            status = 200
        )

    def __query_param_model(self, context: SimpleHTTPRequestHandler):
        query_param_model = QueryParamModel(Settings.instance())
        query_param_model.as_remote() if context.headers.get('access-token') else query_param_model.as_local()
        return query_param_model