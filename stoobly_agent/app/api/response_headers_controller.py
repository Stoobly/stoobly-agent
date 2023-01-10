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

    # GET /requests/:requestId/headers
    def index(self, context):
        context.parse_path_params({
            'requestId': 1
        })

        response_header_model = self.__response_header_model(context)
        requests = response_header_model.index(context.params.get('requestId'), **context.params)

        context.render(
            json = requests,
            status = 200
        )

    def __response_header_model(self, context: SimpleHTTPRequestHandler):
        response_header_model = ResponseHeaderModel(Settings.instance())
        response_header_model.as_remote() if context.headers.get('access-token') else response_header_model.as_local()
        return response_header_model