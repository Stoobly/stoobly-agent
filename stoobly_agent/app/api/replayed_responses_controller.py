import pdb
import requests

from stoobly_agent.app.api.simple_http_request_handler import SimpleHTTPRequestHandler
from stoobly_agent.app.models.replayed_response_model import ReplayedResponseModel
from stoobly_agent.app.settings import Settings
from stoobly_agent.config.constants import custom_headers

class ReplayedResponsesController:
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

    # GET /requests/:requestId/replayed_responses
    def index(self, context: SimpleHTTPRequestHandler):
        context.parse_path_params({
            'request_id': 1
        })
        replayed_response_model = self.__replayed_response_model(context)
        replayed_responses = replayed_response_model.index(**context.params)

        if not replayed_responses:
            return context.not_found()

        context.render(
            json = replayed_responses,
            status = 200
        )

    # GET /requests/:requestId/replayed_responses/:replayedResponseId/mock
    def mock(self, context: SimpleHTTPRequestHandler):
        context.parse_path_params({
            'request_id': 1,
            'replayed_response_id': 3,
        })

        replayed_response_model = self.__replayed_response_model(context) 
        response: requests.Response = replayed_response_model.mock(context.params.get('replayed_response_id'))

        return self.__render_response(context, response)

    def __replayed_response_model(self, context: SimpleHTTPRequestHandler):
        replayed_response_model = ReplayedResponseModel(Settings.instance())
        replayed_response_model.as_remote() if context.headers.get('access-token') else replayed_response_model.as_local()
        return replayed_response_model

    def __render_response(self, context: SimpleHTTPRequestHandler, response: requests.Response):
        if response == None:
            return context.render(
                plain = '',
                status = 404
            )

        # Extract specific headers
        headers = {
            'Access-Control-Expose-Headers': custom_headers.RESPONSE_ID,
        }

        accepted_headers = ['content-type', custom_headers.RESPONSE_ID.lower()]

        for header, val in response.headers.items():
            decoded_header = header.lower()

            if decoded_header not in accepted_headers:
                continue 

            headers[decoded_header] = val

        context.render(
            data = response.content,
            headers = headers,
            status = 200
        )