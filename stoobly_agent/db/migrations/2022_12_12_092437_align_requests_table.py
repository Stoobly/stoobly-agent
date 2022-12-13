import pdb
import requests

from orator.migrations import Migration
from urllib.parse import urlparse

from stoobly_agent.app.models.adapters.raw_http_request_adapter import RawHttpRequestAdapter
from stoobly_agent.app.models.adapters.raw_http_response_adapter import RawHttpResponseAdapter
from stoobly_agent.lib.orm.request import Request
from stoobly_agent.app.proxy.upload.response_string_control import ResponseStringControl

class AlignRequestsTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.table('requests') as table:
            table.integer('latency').default(0)
            table.string('password').nullable()
            table.string('query').nullable()
            table.integer('status').nullable()
            table.string('user').nullable()

            for request in Request.all():
                _request: requests.Request = RawHttpRequestAdapter(request.raw)

                parsed_url = urlparse(_request.url)
                request.path = parsed_url.path.decode()
                request.query = parsed_url.query.decode()

                if parsed_url.username:
                    request.user = parsed_url.username.decode()

                if parsed_url.password:
                    request.password = parsed_url.password.decode()

                response = request.response
                if response:
                    response_control = ResponseStringControl()
                    response_control.parse(response.control.decode())

                    request.latency = response_control.latency

                    _response = RawHttpResponseAdapter(response.raw)
                    request.status = int(_response.status)

                request.update()

    def down(self):
        """
        Revert the migrations.
        """
        with self.schema.table('requests') as table:
            table.drop_column('latency', 'password', 'query', 'status', 'user')
