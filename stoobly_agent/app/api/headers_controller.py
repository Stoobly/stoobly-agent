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
        header, status = header_model.create(context.params.get('requestId'), **context.params)

        if context.filter_response(header, status):
            return
        
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
        headers, status = header_model.index(context.params.get('requestId'), **context.params)

        if context.filter_response(headers, status):
            return

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
        header, status = header_model.update(context.params.get('requestId'), **context.params)

        if context.filter_response(header, status):
            return
        
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
        header, status = header_model.destroy(context.params.get('requestId'), context.params.get('headerId'))

        if context.filter_response(header, status):
            return

        context.render(
            plain = '',
            status = 200
        )

    def __header_model(self, context: SimpleHTTPRequestHandler):
        access_token=context.headers.get('access-token')
        header_model = HeaderModel(Settings.instance(), access_token=access_token)
        return header_model