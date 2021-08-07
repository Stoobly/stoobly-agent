import pdb

from ..lib.cache import Cache

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

    # GET /api/v1/admin/statuses/:id
    def get_status(self, context):
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
            cache.delete(context.params.get('id'))
            context.render(
                plain = status,
                status = 200
            )

    # PUT /api/v1/admin/statuses/:id
    def put_status(self, context):
        context.parse_path_params({
            'id': 4
        })

        cache = Cache.instance()
        cache.write(context.params.get('id'), context.parse_body())

        context.render(
            plain = '',
            status = 200
        )

