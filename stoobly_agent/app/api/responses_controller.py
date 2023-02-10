import pdb
import requests

from stoobly_agent.app.api.simple_http_request_handler import SimpleHTTPRequestHandler
from stoobly_agent.app.models.response_model import ResponseModel
from stoobly_agent.app.settings import Settings
from stoobly_agent.config.constants import custom_headers

class ResponsesController:
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

    # GET /requests/:requestId/responses/mock
    def mock(self, context: SimpleHTTPRequestHandler):
        context.parse_path_params({
            'requestId': 1
        })

        response_model = self.__response_model(context) 
        response: requests.Response = response_model.mock(context.params.get('requestId'))

        return self.__render_response(context, response)

    def __response_model(self, context: SimpleHTTPRequestHandler):
        response_model = ResponseModel(Settings.instance())
        response_model.as_remote() if context.headers.get('access-token') else response_model.as_local()
        return response_model

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