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
    def index(self, context: SimpleHTTPRequestHandler):
        context.parse_path_params({
            'request_id': 1,
            'replayed_response_id': 3,
        })

        replayed_response_model = self.__replayed_response_model(context)
        raw, status = replayed_response_model.raw(context.params.get('replayed_response_id'))

        if context.filter_response(raw, status):
            return

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
        access_token = context.headers.get('access-token')
        replayed_response_model = ReplayedResponseModel(Settings.instance(), access_token=access_token)
        return replayed_response_model