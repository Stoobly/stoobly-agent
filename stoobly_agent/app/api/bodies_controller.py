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

    # PUT /requests/:requestId/bodies/:bodyId
    def update(self, context: SimpleHTTPRequestHandler):
        context.parse_path_params({
            'requestId': 1
        })

        text = context.params.get('text')
        if text == None:
            return context.bad_request('Missing text')

        body_model = self.__body_model(context)
        request, status = body_model.update(context.params.get('requestId'), text)

        if context.filter_response(request, status):
            return

        context.render(
            json = {
                'text': text,
            },
            status = 200 
        )

    # GET /requests/:requestId/bodies/mock
    def mock(self, context: SimpleHTTPRequestHandler):
        context.parse_path_params({
            'requestId': 1
        })

        body_model = self.__body_model(context)
        request, status = body_model.mock(context.params.get('requestId'))

        if context.filter_response(request, status):
            return

        # Extract specific headers
        headers = {}

        accepted_headers = ['content-encoding', 'content-length', 'content-type']
        for header, val in request.headers.items():
            decoded_header = header.lower()

            if decoded_header not in accepted_headers:
                continue 

            headers[decoded_header] = val

        context.render(
            data = request.data,
            headers = headers,
            status = 200
        )

    def __body_model(self, context: SimpleHTTPRequestHandler) -> BodyModel:
        access_token = context.headers.get('access-token')
        body_model = BodyModel(Settings.instance(), access_token=access_token)
        return body_model