import pdb
import requests

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
        
        request: requests.Request = BodyModel(Settings.instance()).mock(context.params.get('requestId'))

        if request == None:
            return context.render(
                plain = '',
                status = 404
            )

        # Extract content-type header
        headers = {}

        for header, val in request.headers.items():
            decoded_header = header.decode()
            if decoded_header.lower() == 'content-type':
                headers[decoded_header] = val.decode()
                break

        context.render(
            data = request.data,
            headers = headers,
            status = 200
        )