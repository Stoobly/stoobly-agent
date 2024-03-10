import pdb
import pytest

from click.testing import CliRunner

from stoobly_agent.app.models.factories.resource.local_db.request_adapter import (
  LocalDBRequestAdapter,
)
from stoobly_agent.app.models.schemas.request import Request as RequestSchema
from stoobly_agent.app.proxy.replay.trace_context import TraceContext
from stoobly_agent.cli import record
from stoobly_agent.config.constants import alias_resolve_strategy
from stoobly_agent.lib.orm.request import Request
from stoobly_agent.lib.orm.trace_alias import TraceAlias
from stoobly_agent.test.test_helper import DETERMINISTIC_GET_REQUEST_URL, reset

@pytest.fixture(scope='module')
def runner():
    return CliRunner()

class TestTraceContext():

    @pytest.fixture(scope='class', autouse=True)
    def settings(self):
        return reset()

    @pytest.fixture(scope='class')
    def request_show_response(self, runner: CliRunner):
      record_result = runner.invoke(record, [DETERMINISTIC_GET_REQUEST_URL])
      assert record_result.exit_code == 0
      request = Request.last()
      adapter = LocalDBRequestAdapter()
      return adapter.show(request.id, **{
        'body': True,
        'headers': True,
        'query_params': True
      })[0]


    @pytest.fixture(scope='class')
    def endpoint_show_response(self):
      return {
        'aliases': [],
        'body_param_names': [],
        'header_names': [],
        'path_segment_names': [],
        'query_param_names': [],
      }

    class TestWhenFifoStrategy():

      @pytest.fixture(scope='class')
      def trace_context(self):
        context = TraceContext(None, None)
        context.alias_resolve_strategy = alias_resolve_strategy.FIFO
        return context

      @pytest.fixture(scope='class')
      def request_schema(self, request_show_response):
        return RequestSchema(request_show_response)

      class TestWhenHeader():

        @pytest.fixture(scope='class')
        def accept_encodings(self):
          return ['gzip; deflate', 'br']

        @pytest.fixture(scope='class')
        def access_token(self):
          return 'abc123'

        @pytest.fixture(scope='class')
        def aliases(self):
          return [
            {
              'id': 1,
              'name': ':acceptEncoding'
            },
            {
              'id': 2,
              'name': ':accessToken'
            }
          ]

        @pytest.fixture(scope='class')
        def header_names(self, aliases):
          accept_encoding_alias = aliases[0]
          access_token_alias = aliases[1]
          return [
            {
              'alias_id': accept_encoding_alias['id'],
              'id': 1,
              'name': 'Accept-Encoding'
            },
            {
              'alias_id': access_token_alias['id'],
              'id': 2,
              'name': 'Access-Token'
            }
          ]

        @pytest.fixture(scope='class')
        def decorated_endpoint_show_response(self, endpoint_show_response, aliases, header_names):
          endpoint_show_response['aliases'] = aliases
          endpoint_show_response['header_names'] = header_names
          return endpoint_show_response

        @pytest.fixture(scope='class')
        def decorated_request_schema(self, request_schema: RequestSchema, accept_encodings, access_token):
          headers = request_schema.headers
          headers.add('Accept-Encoding', accept_encodings[0])
          headers.add('Accept-Encoding', accept_encodings[1])
          headers.add('Access-Token', access_token)
          request_schema.headers = headers
          return request_schema

        @pytest.fixture(scope='class')
        def accept_encoding_trace_alias(self, trace_context: TraceContext, aliases):
          accept_encoding_alias = aliases[0]
          return trace_context.create_trace_alias(accept_encoding_alias['name'], '1')

        @pytest.fixture(scope='class')
        def access_token_trace_alias(self, trace_context: TraceContext, aliases):
          access_token_alias = aliases[1]
          return trace_context.create_trace_alias(access_token_alias['name'], '1')

        def test_it_resolves_accept_encoding(
          self, 
          trace_context: TraceContext,
          decorated_request_schema: RequestSchema,
          decorated_endpoint_show_response,
          accept_encoding_trace_alias: TraceAlias,
          accept_encodings,
        ):
          trace_context.rewrite_request(decorated_request_schema, decorated_endpoint_show_response)
          trace_alias = TraceAlias.find_by(id=accept_encoding_trace_alias.id)

          assert trace_alias.assigned_to == ','.join(accept_encodings)

        def test_it_resolves_access_token(
          self, 
          trace_context: TraceContext,
          decorated_request_schema: RequestSchema,
          decorated_endpoint_show_response,
          access_token_trace_alias: TraceAlias,
          access_token,
        ):
          trace_context.rewrite_request(decorated_request_schema, decorated_endpoint_show_response)
          trace_alias = TraceAlias.find_by(id=access_token_trace_alias.id)

          assert trace_alias.assigned_to == access_token

      class TestWhenQueryParam():

        @pytest.fixture(scope='class')
        def filter(self):
          return ['1', '2']

        @pytest.fixture(scope='class')
        def page(self):
          return '0'

        @pytest.fixture(scope='class')
        def aliases(self):
          return [
            {
              'id': 1,
              'name': ':filter'
            },
            {
              'id': 2,
              'name': ':page'
            }
          ]

        @pytest.fixture(scope='class')
        def query_param_names(self, aliases):
          filter_alias = aliases[0]
          page_alias = aliases[1]
          return [
            {
              'alias_id': filter_alias['id'],
              'id': 1,
              'name': 'filter'
            },
            {
              'alias_id': page_alias['id'],
              'id': 2,
              'name': 'page'
            }
          ]

        @pytest.fixture(scope='class')
        def decorated_endpoint_show_response(self, endpoint_show_response, aliases, query_param_names):
          endpoint_show_response['aliases'] = aliases
          endpoint_show_response['query_param_names'] = query_param_names
          return endpoint_show_response

        @pytest.fixture(scope='class')
        def decorated_request_schema(self, request_schema: RequestSchema, filter, page):
          query_params = request_schema.query_params

          for v in filter:
            query_params.add('filter', v)
          query_params.add('page', page)
          request_schema.query_params = query_params

          return request_schema

        @pytest.fixture(scope='class')
        def filter_trace_alias(self, trace_context: TraceContext, aliases):
          filter_alias = aliases[0]
          return trace_context.create_trace_alias(filter_alias['name'], '1')

        @pytest.fixture(scope='class')
        def page_trace_alias(self, trace_context: TraceContext, aliases):
          page_alias = aliases[1]
          return trace_context.create_trace_alias(page_alias['name'], '1')

        def test_it_resolves_filter(
          self, 
          trace_context: TraceContext,
          decorated_request_schema: RequestSchema,
          decorated_endpoint_show_response,
          filter_trace_alias: TraceAlias,
          filter
        ):
          trace_context.rewrite_request(decorated_request_schema, decorated_endpoint_show_response)
          trace_alias = TraceAlias.find_by(id=filter_trace_alias.id)

          assert trace_alias.assigned_to == ','.join(filter)

        def test_it_resolves_page(
          self, 
          trace_context: TraceContext,
          decorated_request_schema: RequestSchema,
          decorated_endpoint_show_response,
          page_trace_alias: TraceAlias,
          page,
        ):
          trace_context.rewrite_request(decorated_request_schema, decorated_endpoint_show_response)
          trace_alias = TraceAlias.find_by(id=page_trace_alias.id)

          assert trace_alias.assigned_to == page

      class TestWhenQueryParam():

        @pytest.fixture(scope='class')
        def filter(self):
          return ['1', '2']

        @pytest.fixture(scope='class')
        def page(self):
          return '0'

        @pytest.fixture(scope='class')
        def aliases(self):
          return [
            {
              'id': 1,
              'name': ':filter'
            },
            {
              'id': 2,
              'name': ':page'
            }
          ]

        @pytest.fixture(scope='class')
        def query_param_names(self, aliases):
          filter_alias = aliases[0]
          page_alias = aliases[1]
          return [
            {
              'alias_id': filter_alias['id'],
              'id': 1,
              'name': 'filter'
            },
            {
              'alias_id': page_alias['id'],
              'id': 2,
              'name': 'page'
            }
          ]

        @pytest.fixture(scope='class')
        def decorated_endpoint_show_response(self, endpoint_show_response, aliases, query_param_names):
          endpoint_show_response['aliases'] = aliases
          endpoint_show_response['query_param_names'] = query_param_names
          return endpoint_show_response

        @pytest.fixture(scope='class')
        def decorated_request_schema(self, request_schema: RequestSchema, filter, page):
          query_params = request_schema.query_params

          for v in filter:
            query_params.add('filter', v)
          query_params.add('page', page)
          request_schema.query_params = query_params

          return request_schema

        @pytest.fixture(scope='class')
        def filter_trace_alias(self, trace_context: TraceContext, aliases):
          filter_alias = aliases[0]
          return trace_context.create_trace_alias(filter_alias['name'], '1')

        @pytest.fixture(scope='class')
        def page_trace_alias(self, trace_context: TraceContext, aliases):
          page_alias = aliases[1]
          return trace_context.create_trace_alias(page_alias['name'], '1')

        def test_it_resolves_filter(
          self, 
          trace_context: TraceContext,
          decorated_request_schema: RequestSchema,
          decorated_endpoint_show_response,
          filter_trace_alias: TraceAlias,
          filter
        ):
          trace_context.rewrite_request(decorated_request_schema, decorated_endpoint_show_response)
          trace_alias = TraceAlias.find_by(id=filter_trace_alias.id)

          assert trace_alias.assigned_to == ','.join(filter)

        def test_it_resolves_page(
          self, 
          trace_context: TraceContext,
          decorated_request_schema: RequestSchema,
          decorated_endpoint_show_response,
          page_trace_alias: TraceAlias,
          page,
        ):
          trace_context.rewrite_request(decorated_request_schema, decorated_endpoint_show_response)
          trace_alias = TraceAlias.find_by(id=page_trace_alias.id)

          assert trace_alias.assigned_to == page

      class TestWhenBodyParam():

        @pytest.fixture(scope='class')
        def email(self):
          return 'test@stoobly.com'

        @pytest.fixture(scope='class')
        def aliases(self):
          return [
            {
              'id': 1,
              'name': ':email'
            },
          ]

        @pytest.fixture(scope='class')
        def body_param_names(self, aliases):
          email_alias = aliases[0]
          return [
            {
              'alias_id': email_alias['id'],
              'id': 1,
              'name': 'email',
            }
          ]

        @pytest.fixture(scope='class')
        def decorated_endpoint_show_response(self, endpoint_show_response, aliases, body_param_names):
          endpoint_show_response['aliases'] = aliases
          endpoint_show_response['body_param_names'] = body_param_names
          return endpoint_show_response

        @pytest.fixture(scope='class')
        def decorated_request_schema(self, request_schema: RequestSchema, email):
          headers = request_schema.headers
          headers['content-type'] = 'application/json'
          request_schema.headers = headers
          request_schema.body_params = { 'email': email }
          return request_schema

        @pytest.fixture(scope='class')
        def email_trace_alias(self, trace_context: TraceContext, aliases):
          filter_alias = aliases[0]
          return trace_context.create_trace_alias(filter_alias['name'], '1')

        def test_it_resolves_filter(
          self, 
          trace_context: TraceContext,
          decorated_request_schema: RequestSchema,
          decorated_endpoint_show_response,
          email_trace_alias: TraceAlias,
          email
        ):
          trace_context.rewrite_request(decorated_request_schema, decorated_endpoint_show_response)
          trace_alias = TraceAlias.find_by(id=email_trace_alias.id)

          assert trace_alias.assigned_to == email