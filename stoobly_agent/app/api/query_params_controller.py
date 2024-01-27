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
        query_param, status = query_param_model.create(context.params.get('requestId'), **{
            'name': context.params['name'],
            'value': context.params['value'],
        })

        if context.filter_response(query_param, status):
            return

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
        query_params, status = query_param_model.index(context.params.get('requestId'), **context.params)

        if context.filter_response(query_params, status):
            return

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
        query_param, status = query_param_model.update(context.params.get('requestId'), context.params.get('queryParamId'), **{
            'name': context.params['name'],
            'value': context.params['value'],
        })

        if context.filter_response(query_param, status):
            return

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
        query_param, status = query_param_model.destroy(context.params.get('requestId'), context.params.get('queryParamId'))

        if context.filter_response(query_param, status):
            return
        
        context.render(
            plain = query_param,
            status = status
        )

    def __query_param_model(self, context: SimpleHTTPRequestHandler):
        access_token = context.headers.get('access-token')
        query_param_model = QueryParamModel(Settings.instance(), access_token=access_token)
        return query_param_model