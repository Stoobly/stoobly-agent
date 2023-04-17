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

    # POST /requests/:requestId/query_params
    def create(self, context: SimpleHTTPRequestHandler):
        context.parse_path_params({
            'requestId': 1,
            'queryParamId': 3,
        })

        if not context.params.get('name'):
            return context.bad_request('Missing name')

        if not context.params.get('value'):
            return context.bad_request('Missing value')

        query_param_model = self.__query_param_model(context)
        query_param = query_param_model.create(context.params.get('requestId'), **{
            'name': context.params['name'],
            'value': context.params['value'],
        })

        context.render(
            json = query_param,
            status = 200
        )

    # GET /requests/:requestId/query_params
    def index(self, context: SimpleHTTPRequestHandler):
        context.parse_path_params({
            'requestId': 1
        })

        query_param_model = self.__query_param_model(context)
        query_params = query_param_model.index(context.params.get('requestId'), **context.params)

        context.render(
            json = query_params,
            status = 200
        )

    # PUT /requests/:requestId/query_params/:queryParamId
    def update(self, context: SimpleHTTPRequestHandler):
        context.parse_path_params({
            'requestId': 1,
            'queryParamId': 3,
        })

        if not context.params.get('name'):
            return context.bad_request('Missing name')

        if not context.params.get('value'):
            return context.bad_request('Missing value')

        query_param_model = self.__query_param_model(context)
        query_param = query_param_model.update(context.params.get('requestId'), context.params.get('queryParamId'), **{
            'name': context.params['name'],
            'value': context.params['value'],
        })

        context.render(
            json = query_param,
            status = 200
        )

    # DELETE /requests/:requestId/query_params/:queryParamId
    def destroy(self, context: SimpleHTTPRequestHandler):
        context.parse_path_params({
            'requestId': 1,
            'queryParamId': 3,
        })

        query_param_model = self.__query_param_model(context)
        query_param = query_param_model.destroy(context.params.get('requestId'), context.params.get('queryParamId'))

        if not query_param:
            context.internal_error()
        else:
            context.render(
                plain = '',
                status = 200
            )

    def __query_param_model(self, context: SimpleHTTPRequestHandler):
        query_param_model = QueryParamModel(Settings.instance())
        query_param_model.as_remote() if context.headers.get('access-token') else query_param_model.as_local()
        return query_param_model