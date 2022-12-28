import pdb

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
        
        requests = ResponseHeaderModel(Settings.instance()).index(context.params.get('requestId'), **context.params)

        context.render(
            json = requests,
            status = 200
        )