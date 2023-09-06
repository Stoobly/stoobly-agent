import requests
import pdb

from stoobly_orator.migrations import Migration

from stoobly_agent.app.models.adapters.raw_http_response_adapter import RawHttpResponseAdapter
from stoobly_agent.lib.orm.request import Request
from stoobly_agent.app.proxy.mock.request_hasher import RequestHasher

class AlignRequests(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.table('requests') as table:
            table.string('response_hash').default('')
            table.string('response_headers_hash').default('')

        for request in Request.all():
            response = request.response
            if not response:
                continue

            _response: requests.Response = RawHttpResponseAdapter(response.raw).to_response()
            response_hash = RequestHasher.instance().hash_text(_response.content)
            response_headers_hash = RequestHasher.instance().hash_params(_response.headers)

            request.update(response_hash=response_hash, response_headers_hash=response_headers_hash)

    def down(self):
        """
        Revert the migrations.
        """
        with self.schema.table('requests') as table:
            table.drop_column('response_hash', 'response_headers_hash')


