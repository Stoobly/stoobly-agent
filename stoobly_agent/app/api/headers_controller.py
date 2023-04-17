import pdb

from stoobly_agent.app.api.simple_http_request_handler import SimpleHTTPRequestHandler
from stoobly_agent.app.models.header_model import HeaderModel
from stoobly_agent.app.settings import Settings

class HeadersController:
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

    # POST /requests/:requestId/headers
    def create(self, context: SimpleHTTPRequestHandler):
        context.parse_path_params({
            'requestId': 1
        })

        header_model = self.__header_model(context) 
        header = header_model.create(context.params.get('requestId'), **context.params)
        
        context.render(
            json = header,
            status = 200
        )

    # GET /requests/:requestId/headers
    def index(self, context: SimpleHTTPRequestHandler):
        context.parse_path_params({
            'requestId': 1
        })

        header_model = self.__header_model(context) 
        headers = header_model.index(context.params.get('requestId'), **context.params)

        context.render(
            json = headers,
            status = 200
        )

    # PUT /requests/:requestId/headers/:headerId
    def update(self, context: SimpleHTTPRequestHandler):
        context.parse_path_params({
            'requestId': 1
        })

        header_model = self.__header_model(context) 
        header = header_model.update(context.params.get('requestId'), **context.params)
        
        context.render(
            json = header,
            status = 200
        )

    # DELETE /requests/:requestId/headers/:headerId
    def destroy(self, context: SimpleHTTPRequestHandler):
        context.parse_path_params({
            'requestId': 1,
            'headerId': 3,
        })

        header_model = self.__header_model(context) 
        header = header_model.destroy(context.params.get('requestId'), context.params.get('headerId'))

        if not header: 
            context.internal_error()
        else:
            context.render(
                plain = '',
                status = 200
            )

    def __header_model(self, context: SimpleHTTPRequestHandler):
        header_model = HeaderModel(Settings.instance())
        header_model.as_remote() if context.headers.get('access-token') else header_model.as_local()
        return header_model