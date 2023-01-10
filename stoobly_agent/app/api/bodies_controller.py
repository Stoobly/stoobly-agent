import pdb
import requests

from stoobly_agent.app.api.simple_http_request_handler import SimpleHTTPRequestHandler
from stoobly_agent.app.models.body_model import BodyModel
from stoobly_agent.app.settings import Settings

class BodiesController:
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
    def mock(self, context):
        context.parse_path_params({
            'requestId': 1
        })

        body_model = self.__body_model(context)
        request: requests.Request = body_model.mock(context.params.get('requestId'))

        if request == None:
            return context.render(
                plain = '',
                status = 404
            )

        # Extract specific headers
        headers = {}

        accepted_headers = ['content-encoding', 'content-length', 'content-type']
        for header, val in request.headers.items():
            decoded_header = header.decode().lower()

            if decoded_header not in accepted_headers:
                continue 

            headers[decoded_header] = val.decode()

        context.render(
            data = request.data,
            headers = headers,
            status = 200
        )

    def __body_model(self, context: SimpleHTTPRequestHandler):
        body_model = BodyModel(Settings.instance())
        body_model.as_remote() if context.headers.get('access-token') else body_model.as_local()
        return body_model