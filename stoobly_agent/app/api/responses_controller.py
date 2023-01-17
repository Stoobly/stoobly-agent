import pdb
import requests

from stoobly_agent.app.api.simple_http_request_handler import SimpleHTTPRequestHandler
from stoobly_agent.app.models.response_model import ResponseModel
from stoobly_agent.app.settings import Settings

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

    # GET /requests/:requestId/bodies/mock
    def mock(self, context: SimpleHTTPRequestHandler):
        context.parse_path_params({
            'requestId': 1
        })

        response_model = self.__response_model(context) 
        response: requests.Response = response_model.mock(context.params.get('requestId'))

        if response == None:
            return context.render(
                plain = '',
                status = 404
            )

        # Extract specific headers
        headers = {}

        accepted_headers = ['content-type']
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

    def __response_model(self, context: SimpleHTTPRequestHandler):
        response_model = ResponseModel(Settings.instance())
        response_model.as_remote() if context.headers.get('access-token') else response_model.as_local()
        return response_model