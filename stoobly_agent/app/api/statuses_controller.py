import pdb

from stoobly_agent.lib.cache import Cache
from stoobly_agent.lib.utils.decode import decode

class StatusesController:
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

    def index(self, context):
        version = -1

        try:
            version = int(context.params.get('version'))
        except ValueError as e:
            pass

        cache = Cache.instance()
        statuses = []
        if not version or version != cache.version:
            statuses = cache.read_all()

        context.render(
            json = {
                'statuses': statuses,
                'version': cache.version,
            },
            status = 200
        )

    # GET /statuses/:id
    def get(self, context):
        context.parse_path_params({
            'id': 4
        })

        cache = Cache.instance()
        status = cache.read(context.params.get('id'))

        if not status:
            context.render(
                plain = '',
                status = 204
            )
        else:
            context.render(
                json = {
                    'status': status,
                    'version': cache.version
                },
                status = 200
            )

    # PUT /statuses/:id
    def update(self, context):
        context.parse_path_params({
            'id': 2
        })

        cache = Cache.instance()
        cache.write(context.params.get('id'), decode(context.body))

        context.render(
            plain = '',
            status = 200
        )

