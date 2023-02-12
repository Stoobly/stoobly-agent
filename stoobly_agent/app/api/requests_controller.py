import pdb
import requests

from datetime import datetime
from time import time
from urllib.parse import urlparse

from stoobly_agent.app.api.simple_http_request_handler import SimpleHTTPRequestHandler
from stoobly_agent.app.cli.helpers.context import ReplayContext
from stoobly_agent.app.models.adapters.joined_request_adapter import JoinedRequestAdapter
from stoobly_agent.app.models.adapters.mitmproxy_request_adapter import MitmproxyRequestAdapter
from stoobly_agent.app.models.adapters.mitmproxy_response_adapter import MitmproxyResponseAdapter
from stoobly_agent.app.models.adapters.raw_http_request_adapter import RawHttpRequestAdapter
from stoobly_agent.app.models.adapters.raw_http_response_adapter import RawHttpResponseAdapter
from stoobly_agent.app.models.request_model import RequestModel
from stoobly_agent.app.models.schemas.request import Request
from stoobly_agent.app.proxy.replay.replay_request_service import replay_with_rewrite
from stoobly_agent.app.proxy.upload.upload_request_service import upload_staged_request
from stoobly_agent.app.settings import Settings
from stoobly_agent.lib.orm.replayed_response import ReplayedResponse
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
        if not context.required_params(body_params, ['payloads_delimitter', 'requests']):
            return

        raw_requests = body_params.get('requests') 
        payloads_delimitter = body_params.get('payloads_delimitter')

        toks = raw_requests.split(payloads_delimitter)
        if len(toks) != 2:
            return context.bad_request('Invalid requests format')

        joined_request = JoinedRequestAdapter(raw_requests, payloads_delimitter).adapt()

        request_adapter = RawHttpRequestAdapter(joined_request.request_string.get())
        response_adapter = RawHttpResponseAdapter(joined_request.response_string.get())

        mitmproxy_request = MitmproxyRequestAdapter(request_adapter.protocol, request_adapter.to_request()).adapt()
        mitmproxy_response = MitmproxyResponseAdapter(response_adapter.protocol, response_adapter.to_response()).adapt()

        class MitmproxyFlowMock():
            def __init__(self, request, response):
                self.request = request
                self.response = response

        mitmproxy_flow_mock = MitmproxyFlowMock(mitmproxy_request, mitmproxy_response)

        request_model = self.__request_model(context)
        request = request_model.create(**{
            'flow': mitmproxy_flow_mock,
            'joined_request': joined_request,
        })

        if not request:
            return context.internal_error()

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
        url = urlparse(context.params.get('url'))
        request_response = {
            'body': context.params.get('body'),
            'headers': context.params.get('headers'),
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

    def __request_model(self, context: SimpleHTTPRequestHandler):
        request_model = RequestModel(Settings.instance())
        request_model.as_remote() if context.headers.get('access-token') else request_model.as_local()
        return request_model

    def __replay(self, context: SimpleHTTPRequestHandler, replay_context: ReplayContext):
        self.__send(context, replay_context, self.__create_replayed_response) 

    def __send(self, context: SimpleHTTPRequestHandler, replay_context: ReplayContext, callback = None):
        now = time()
        res = replay_with_rewrite(replay_context)
        received_at = time()

        if callback:
            callback(context, res, int((received_at - now) * 1000))

        context.render(
            data = res.raw.data,
            headers = res.headers,
            status = res.status_code
        )

    def __create_replayed_response(self, context: SimpleHTTPRequestHandler, res: requests.Response, latency: int):   
        request_id = int(context.params.get('id'))
        replayed_response = ReplayedResponse()
        replayed_response.request_id = request_id
        replayed_response.with_python_response(res)
        replayed_response.latency = latency # ms
        replayed_response.save()