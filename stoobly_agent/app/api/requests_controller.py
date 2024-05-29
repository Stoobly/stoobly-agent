import json
import pdb
import uuid

from datetime import datetime
from urllib.parse import urlparse

from stoobly_agent.app.api.simple_http_request_handler import SimpleHTTPRequestHandler
from stoobly_agent.app.cli.helpers.context import ReplayContext
from stoobly_agent.app.models.adapters.orm import JoinedRequestStringAdapter
from stoobly_agent.app.models.helpers.create_request_params_service import build_params
from stoobly_agent.app.models.request_model import RequestModel
from stoobly_agent.app.models.schemas.request import Request
from stoobly_agent.app.proxy.replay.replay_request_service import replay
from stoobly_agent.app.proxy.record import REQUEST_DELIMITTER
from stoobly_agent.app.proxy.record.upload_request_service import upload_staged_request
from stoobly_agent.app.settings import Settings
from stoobly_agent.config.constants import mode
from stoobly_agent.lib.orm.request import Request as OrmRequest
from stoobly_agent.lib.utils.decode import decode

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
        payloads_delimitter = body_params.get('payloads_delimitter') or REQUEST_DELIMITTER
        toks = raw_requests.split(payloads_delimitter)

        if len(toks) % 2 != 0:
            return context.bad_request('Invalid requests format')

        scenario_id = body_params.get('scenario_id')
        scenario_id = int(body_params.get('scenario_id')) if scenario_id else None
        created_requests = []

        for i in range(0, len(toks), 2):
            raw_request = payloads_delimitter.join([toks[i], toks[i + 1]])
            create_params = build_params(raw_request, payloads_delimitter)

            if not create_params:
                # Rollback
                return context.bad_request('Could not parse requests')

            request_model = self.__request_model(context)
            request, status = request_model.create(**{
                **create_params,
                'scenario_id': scenario_id,
                'uuid': str(uuid.uuid4()),
            })

            if context.filter_response(request, status):
                # Rollback
                pass

            created_requests.append(request['list'][0])

        context.render(
            json = {
                'list': created_requests,
                'total': len(created_requests),
            },
            status = 200
        )

    # GET /requests
    def index(self, context: SimpleHTTPRequestHandler):
        request_model = self.__request_model(context)
        requests, status = request_model.index(**context.params)

        if context.filter_response(requests, status):
            return

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
        request, status = request_model.show(context.params.get('id'))

        if context.filter_response(request, status):
            return

        context.render(
            json = request,
            status = 200
        )

    # POST /requests/:id/push
    def push(self, context: SimpleHTTPRequestHandler):
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

        request.update(pushed_at = datetime.now())
        request_model.as_local()
        request, status = request_model.show(request.id)

        if context.filter_response(request, status):
            return

        # This can error out if res is not properly formatted
        # The request has a local ID (the ID of the request that was pushed)
        # and a remote ID (the ID of the request that was created)
        try:
            if len(res['list']):
                request['remote_id'] = res['list'][0]['id']
        except Exception:
            pass

        context.render(
            json = request,
            status = 200
        )

    # PUT /requests/:id
    def update(self, context: SimpleHTTPRequestHandler):
        context.parse_path_params({
            'id': 1
        })

        request_params = context.params.get('request')
        if request_params.get('scenario_id') == -1:
            request_params['scenario_id'] = None

        request_id = context.params.get('id')
        request_model = self.__request_model(context)
        request, status = request_model.update(request_id, **request_params)

        if context.filter_response(request, status):
            return

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
        request, status = request_model.destroy(request_id)

        if context.filter_response(request, status):
            return

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
        request_response, status = request_model.show(request_id, **{
            'body': True,
            'headers': True,
            'project_id': project_id,
            'query_params': True,
        })

        if context.filter_response(request_response, status):
            return

        replay_context = ReplayContext(Request(request_response))
        self.__replay(context, replay_context)

    # PUT /requests/send
    def send(self, context: SimpleHTTPRequestHandler):
        body_params = context.params

        headers = []
        try:
            headers = json.load(decode(body_params.get('headers')))
        except Exception as e:
            pass

        url = urlparse(decode(body_params.get('url')))
        request_response = {
            'body': decode(body_params.get('body')),
            'headers': headers,
            'method': decode(body_params.get('method')),
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
                download = text,
                filename = filename,
                status = 200
            )
        else:
            return context.bad_request('Invalid format')

    def __request_model(self, context: SimpleHTTPRequestHandler):
        access_token = context.headers.get('access-token')
        request_model = RequestModel(Settings.instance(), access_token=access_token)
        return request_model

    def __replay(self, context: SimpleHTTPRequestHandler, replay_context: ReplayContext):
        options = {}
        if bool(context.params.get('save')):
            options['save'] = True

        self.__send(context, replay_context, **options)

    def __send(self, context: SimpleHTTPRequestHandler, replay_context: ReplayContext, **replay_options):
        res = replay(replay_context, { **replay_options, 'mode': mode.REPLAY })

        if 'Access-Control-Allow-Origin' in res.headers:
            del res.headers['Access-Control-Allow-Origin']

        context.render(
            data = res.raw.data if hasattr(res, 'raw') else res.content,
            headers = res.headers,
            status = res.status_code
        )
