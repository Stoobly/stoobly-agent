import pdb

from datetime import datetime
from urllib.parse import parse_qs

from stoobly_agent.app.models.adapters.joined_request_adapter import JoinedRequestAdapter
from stoobly_agent.app.models.adapters.mitmproxy_request_adapter import MitmproxyRequestAdapter
from stoobly_agent.app.models.adapters.mitmproxy_response_adapter import MitmproxyResponseAdapter
from stoobly_agent.app.models.adapters.raw_http_request_adapter import RawHttpRequestAdapter
from stoobly_agent.app.models.adapters.raw_http_response_adapter import RawHttpResponseAdapter
from stoobly_agent.app.models.request_model import RequestModel
from stoobly_agent.app.proxy.upload.upload_request_service import upload_staged_request
from stoobly_agent.app.settings import Settings
from stoobly_agent.lib.orm.request import Request

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

    def create(self, context):
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

        request = RequestModel(Settings.instance()).create(**{
            'flow': mitmproxy_flow_mock,
            'joined_request': joined_request,
        })

        if not request:
            context.render(
                plain = '',
                status = 500
            )
        
            return None
        else:
            context.render(
                json = request,
                status = 200
            )


    # GET /requests
    def index(self, context):
        requests = RequestModel(Settings.instance()).index(**context.params)

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
        
            return None
        else:
            context.render(
                json = request,
                status = 200
            )

    # POST /requests/:id/upload
    def upload(self, context):
        context.parse_path_params({
            'id': 1,
        })

        request = Request.find_by(id=context.params.get('id'))

        if not request:
            return

        body_params = context.params

        if not context.required_params(body_params, ['project_key']):
            return

        request_model = RequestModel(Settings.instance())
        request_model.as_remote()
        res = upload_staged_request(
            request, 
            request_model, 
            body_params.get('project_key'),
            body_params.get('scenario_key')
        )

        if not res: 
            context.internal_error()
        else:
            request.update(committed_at = datetime.now())
            request = RequestModel(Settings.instance()).show(request.id)

            context.render(
                json = request,
                status = 200
            )

    # PUT /requests/:id
    def update(self, context):
        context.parse_path_params({
            'id': 1
        })

        request_id = context.params.get('id')
        request = RequestModel(Settings.instance()).update(request_id, **context.params.get('request'))

        if not request:
            context.render(
                plain = '',
                status = 404
            )
        
            return None
        else:
            context.render(
                json = request,
                status = 200
            )

    # DELETE /requests/:id
    def destroy(self, context):
        context.parse_path_params({
            'id': 1
        })

        request_id = context.params.get('id')

        request = RequestModel(Settings.instance()).destroy(request_id)

        if not request:
            context.render(
                plain = '',
                status = 404
            )
        
            return None
        else:
            context.render(
                json = request,
                status = 200
            )