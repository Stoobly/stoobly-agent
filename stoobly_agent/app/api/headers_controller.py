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

    # GET /requests/:requestId/headers
    def index(self, context):
        context.parse_path_params({
            'requestId': 1
        })

        header_model = self.__header_model(context) 
        requests = header_model.index(context.params.get('requestId'), **context.params)

        context.render(
            json = requests,
            status = 200
        )

    def __header_model(self, context: SimpleHTTPRequestHandler):
        header_model = HeaderModel(Settings.instance())
        header_model.as_remote() if context.headers.get('access-token') else header_model.as_local()
        return header_model