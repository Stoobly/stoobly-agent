import pdb

from stoobly_agent.app.api.simple_http_request_handler import SimpleHTTPRequestHandler
from stoobly_agent.app.models.adapters.raw_http_response_adapter import RawHttpResponseAdapter
from stoobly_agent.app.models.replayed_response_model import ReplayedResponseModel
from stoobly_agent.app.settings import Settings

class ReplayedResponseHeadersController:
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

    # GET /requests/:requestId/replayed_response/:replayedResponseId/headers
    def index(self, context):
        context.parse_path_params({
            'request_id': 1,
            'replayed_response_id': 3,
        })

        replayed_response_model = self.__replayed_response_model(context)
        raw = replayed_response_model.raw(context.params.get('replayed_response_id'))

        response = RawHttpResponseAdapter(raw).to_response()

        headers = []
        for key, val in response.headers.items():
            headers.append({
                'name': key,
                'value': val,
            })

        context.render(
            json = headers,
            status = 200
        )

    def __replayed_response_model(self, context: SimpleHTTPRequestHandler):
        replayed_response_model = ReplayedResponseModel(Settings.instance())
        replayed_response_model.as_remote() if context.headers.get('access-token') else replayed_response_model.as_local()
        return replayed_response_model