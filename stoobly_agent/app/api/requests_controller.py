import json
import pdb

from datetime import datetime
from urllib.parse import urlparse

from stoobly_agent.app.api.simple_http_request_handler import SimpleHTTPRequestHandler
from stoobly_agent.app.cli.helpers.context import ReplayContext
from stoobly_agent.app.models.adapters import JoinedRequestAdapter, RawHttpRequestAdapter, RawHttpResponseAdapter
from stoobly_agent.app.models.adapters.orm import JoinedRequestStringAdapter
from stoobly_agent.app.models.adapters.python import PythonRequestAdapterFactory, PythonResponseAdapterFactory
from stoobly_agent.app.models.request_model import RequestModel
from stoobly_agent.app.models.schemas.request import Request
from stoobly_agent.app.proxy.replay.replay_request_service import replay
from stoobly_agent.app.proxy.upload.upload_request_service import upload_staged_request
from stoobly_agent.app.settings import Settings
from stoobly_agent.config.constants import mode
from stoobly_agent.lib.orm.request import Request as OrmRequest

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

    def create(self, context: SimpleHTTPRequestHandler):
        body_params = context.params
        if not context.required_params(body_params, ['requests']):
            return

        raw_requests = body_params.get('requests') 
        payloads_delimitter = body_params.get('payloads_delimitter') or '🐵🙈🙉'

        toks = raw_requests.split(payloads_delimitter)
        if len(toks) != 2:
            return context.bad_request('Invalid requests format')

        try:
            joined_request = JoinedRequestAdapter(raw_requests, payloads_delimitter).adapt()
        except Exception as e:
            return context.bad_request('Could not parse requests')

        request_adapter = RawHttpRequestAdapter(joined_request.request_string.get())
        response_adapter = RawHttpResponseAdapter(joined_request.response_string.get())

        mitmproxy_request = PythonRequestAdapterFactory(request_adapter.to_request()).mitmproxy_request(request_adapter.protocol)
        mitmproxy_response = PythonResponseAdapterFactory(response_adapter.to_response()).mitmproxy_response()

        class MitmproxyFlowMock():
            def __init__(self, request, response):
                self.request = request
                self.response = response

        mitmproxy_flow_mock = MitmproxyFlowMock(mitmproxy_request, mitmproxy_response)

        request_model = self.__request_model(context)
        request = request_model.create(**{
            'flow': mitmproxy_flow_mock,
            'joined_request': joined_request,
            'scenario_id': body_params.get('scenario_id'),
        })

        if not request:
            return context.internal_error()

        #from stoobly_agent.lib.api.keys.project_key import LOCAL_PROJECT_ID
        #from stoobly_agent.app.proxy.utils.publish_change_service import publish_requests_modified
        #publish_requests_modified(body_params.get('project_id') or LOCAL_PROJECT_ID, sync=True)

        context.render(
            json = request,
            status = 200
        )


    # GET /requests
    def index(self, context: SimpleHTTPRequestHandler):
        request_model = self.__request_model(context)
        requests = request_model.index(**context.params)

        if not requests:
            return context.not_found()

        context.render(
            json = requests,
            status = 200
        )

    # GET /requests/:id
    def get(self, context: SimpleHTTPRequestHandler):
        context.parse_path_params({
            'id': 1
        })

        request_model = self.__request_model(context)
        request = request_model.show(context.params.get('id'))

        if not request:
            return context.not_found()
        
        context.render(
            json = request,
            status = 200
        )

    # POST /requests/:id/upload
    def upload(self, context: SimpleHTTPRequestHandler):
        context.parse_path_params({
            'id': 1,
        })

        body_params = context.params

        if not context.required_params(body_params, ['project_key']):
            return

        request = OrmRequest.find_by(id=body_params.get('id'))

        if not request:
            return context.not_found(f"Could not find request {body_params.get('id')}")

        request_model = RequestModel(Settings.instance())
        request_model.as_remote()
        res = upload_staged_request(
            request, 
            request_model, 
            body_params.get('project_key'),
            body_params.get('scenario_key')
        )

        if not res: 
            return context.internal_error()

        request.update(committed_at = datetime.now())
        request_model.as_local()
        request = request_model.show(request.id)

        context.render(
            json = request,
            status = 200
        )

    # PUT /requests/:id
    def update(self, context: SimpleHTTPRequestHandler):
        context.parse_path_params({
            'id': 1
        })

        request_id = context.params.get('id')

        request_model = self.__request_model(context)
        request = request_model.update(request_id, **context.params.get('request'))

        if not request:
            return context.not_found()
            
        context.render(
            json = request,
            status = 200
        )

    # DELETE /requests/:id
    def destroy(self, context: SimpleHTTPRequestHandler):
        context.parse_path_params({
            'id': 1
        })

        request_id = context.params.get('id')

        request_model = self.__request_model(context)
        request = request_model.destroy(request_id)

        if not request:
           return context.not_found()

        context.render(
            plain = '',
            status = 200
        )

    # GET /requests/:id/replay
    def replay(self, context: SimpleHTTPRequestHandler):
        context.parse_path_params({
            'id': 1
        })
        project_id = int(context.params.get('project_id'))
        request_id = int(context.params.get('id'))

        request_model = self.__request_model(context)
        request_response = request_model.show(request_id, **{
            'body': True,
            'headers': True,
            'project_id': project_id,
            'query_params': True,
        })
        if not request_response:
            return context.bad_request(f"Could not find request {request_id}")

        replay_context = ReplayContext(Request(request_response))
        self.__replay(context, replay_context)

    # PUT /requests/send
    def send(self, context: SimpleHTTPRequestHandler):
        headers = []

        try:
            headers = json.load(context.params.get('headers'))
        except Exception as e:
            pass

        url = urlparse(context.params.get('url'))
        request_response = {
            'body': context.params.get('body'),
            'headers': headers,
            'method': context.params.get('method'),
            'path': url.path,
            'password': url.password,
            'port': url.port,
            'query': url.query,
            'url': url.geturl(),
            'username': url.username,
        }

        replay_context = ReplayContext(Request(request_response))
        self.__send(context, replay_context)

    def download(self, context: SimpleHTTPRequestHandler):
        context.parse_path_params({
            'id': 1
        })
        request_id = int(context.params.get('id'))
        format = context.params.get('format')
        request = OrmRequest.find(request_id)

        if not request:
            return context.not_found()
        if format == 'gor':
            filename = f"REQUEST-{int(datetime.now().timestamp())}.gor"
            text = JoinedRequestStringAdapter(request).adapt()

            context.render(
                plain = b"\n".join([filename.encode(), text]),
                status = 200
            )
        else:
            return context.bad_request('Invalid format')

    def __request_model(self, context: SimpleHTTPRequestHandler):
        request_model = RequestModel(Settings.instance())
        request_model.as_remote() if context.headers.get('access-token') else request_model.as_local()
        return request_model

    def __replay(self, context: SimpleHTTPRequestHandler, replay_context: ReplayContext):
        options = {}
        if bool(context.params.get('save')):
            options['save'] = True

        self.__send(context, replay_context, **options) 

    def __send(self, context: SimpleHTTPRequestHandler, replay_context: ReplayContext, **replay_options):
        res = replay(replay_context, { **replay_options, 'mode': mode.REPLAY })

        context.render(
            data = res.raw.data if hasattr(res, 'raw') else res.content,
            headers = res.headers,
            status = res.status_code
        )