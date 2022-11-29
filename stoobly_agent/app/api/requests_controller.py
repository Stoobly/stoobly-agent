import pdb
from stoobly_agent.app.models.request_model import RequestModel
from stoobly_agent.app.settings import Settings

class RequestsController:
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

    # GET /requests
    def index(self, context):
        requests = RequestModel(Settings.instance()).index()

        context.render(
            json = requests,
            status = 200
        )

    # GET /requests/:id
    def get(self, context):
        context.parse_path_params({
            'id': 1
        })

        request = RequestModel(Settings.instance()).show(context.params.get('id'))

        if not request:
            context.render(
                plain = '',
                status = 404
            )
        else:
            context.render(
                json = request,
                status = 200
            )