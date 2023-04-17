import pdb

from stoobly_agent.app.api.simple_http_request_handler import SimpleHTTPRequestHandler
from stoobly_agent.app.models.response_header_model import ResponseHeaderModel
from stoobly_agent.app.settings import Settings

class ResponseHeadersController:
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

    # POST /requests/:requestId/response_headers
    def create(self, context: SimpleHTTPRequestHandler):
        context.parse_path_params({
            'requestId': 1
        })

        response_header_model = self.__response_header_model(context)
        header = response_header_model.create(context.params.get('requestId'), **context.params)
        
        context.render(
            json = header,
            status = 200
        )

    # GET /requests/:requestId/headers
    def index(self, context):
        context.parse_path_params({
            'requestId': 1
        })

        response_header_model = self.__response_header_model(context)
        response_headers = response_header_model.index(context.params.get('requestId'), **context.params)

        context.render(
            json = response_headers,
            status = 200
        )

    # PUT /requests/:requestId/response_headers/:headerId
    def update(self, context: SimpleHTTPRequestHandler):
        context.parse_path_params({
            'requestId': 1
        })

        response_header_model = self.__response_header_model(context)
        header = response_header_model.update(context.params.get('requestId'), **context.params)
        
        context.render(
            json = header,
            status = 200
        )

    # PUT /requests/:requestId/response_headers/:responseHeaderId
    def destroy(self, context: SimpleHTTPRequestHandler):
        context.parse_path_params({
            'requestId': 1,
            'responseHeaderId': 3,
        })

        response_header_model = self.__response_header_model(context)
        header = response_header_model.destroy(context.params.get('requestId'), context.params.get('responseHeaderId'))

        if not header: 
            context.internal_error()
        else:
            context.render(
                plain = '',
                status = 200
            )

    def __response_header_model(self, context: SimpleHTTPRequestHandler):
        response_header_model = ResponseHeaderModel(Settings.instance())
        response_header_model.as_remote() if context.headers.get('access-token') else response_header_model.as_local()
        return response_header_model