import json
import mimetypes
import os
import re
import threading

from http.server import HTTPServer, BaseHTTPRequestHandler
from mergedeep import merge
from urllib.parse import urlparse, parse_qs

from stoobly_agent.config.constants import env_vars, headers

from .configs_controller import ConfigsController
from .proxy_controller import ProxyController
from .statuses_controller import StatusesController

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    ROOT_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..')

    CONFIGS_PATH = '/api/v1/admin/configs'
    PROXY_PATH = '/proxy'
    STATUSES_PATH = '/api/v1/admin/statuses'
    STATUS_PATH = re.compile(f"{STATUSES_PATH}/.*[^/]$")

    @property
    def public_dir(self):
        return os.path.join(self.ROOT_DIR, 'public')

    ### Method handlers

    def do_OPTIONS(self):
        self.render(
            plain = 'OK',
            status = 200
        )

    def do_GET(self):
        self.preprocess()

        if not self.route('GET'):
            path = os.path.join(self.public_dir, self.path[1:] if self.path != '/' else 'index.html')
            if not os.path.exists(path):
                path = os.path.join(self.public_dir, 'index.html')

            self.render(
                file = path,
                status = 200
            )

    def do_PUT(self):
        self.preprocess()

        if not self.route('PUT'):
            self.render(
                plain = 'NOT FOUND',
                status = 404
            )

    ### Helpers

    def enable_cors(self):
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS, POST, PATCH, PUT, DELETE')
        self.send_header('Access-Control-Allow-Origin', '*')

        allowed_headers = ', '.join([
            'Content-Type'.upper(),
            headers.DO_PROXY.upper(),
            headers.PROXY_HEADERS.upper(),
            headers.REQUEST_PATH.upper(),
            headers.SERVICE_URL.upper(),
        ])
        self.send_header('Access-Control-Allow-Headers', allowed_headers)

        self.send_header('Access-Control-Max-Age', '7200')

    def preprocess(self):
        self.uri = urlparse(self.path)

        self.fullpath = self.path
        self.path = self.uri.path
        self.params = {}
        self.parse_query_params()

    def route(self, method):
        for endpoint_handler in self.ROUTES[method]:
            path = endpoint_handler[0]

            matches = isinstance(path, str) and self.path == path
            matches = matches or not isinstance(path, str) and re.match(path, self.path)

            if matches:
                handler = endpoint_handler[1]
                handler(self)
                return True

        return False

    def parse_path_params(self, path_params_map):
        path = self.uri.path
        path_segments = path.split('/')

        if len(path_segments) == 0:
            return

        if path_segments[0] == '':
            path_segments.pop(0)

        for path_param in path_params_map:
            index = path_params_map[path_param]

            try:
                self.params[path_param] = path_segments[index]
            except:
                pass

    def parse_query_params(self):
        merge(self.params, parse_qs(self.uri.query))

    def parse_body(self):
        if not self.headers.get('Content-Length'):
            body = self.rfile.read()
        else:
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)

        if not self.headers['Content-Type']:
            return body

        if self.headers['Content-Type'].lower() == 'application/json':
            return json.loads(body)
        else:
            return body

    def render(self, **kwargs):
        if kwargs.get('file') != None:
            self.render_file(kwargs)
        elif kwargs.get('json') != None:
            self.render_json(kwargs)
        elif kwargs.get('plain') != None:
            self.render_plain(kwargs)
        elif kwargs.get('data') != None:
            self.render_data(kwargs)

    def render_file(self, kwargs):
        if not 'headers' in kwargs:
            kwargs['headers'] = {}

        path = kwargs['file']

        if not os.path.exists(path):
            kwargs['status'] = 404

        mimetype = mimetypes.guess_type(path)[0]
        kwargs['headers']['Content-Type'] = mimetype or 'text/plain'

        fp = open(path, 'rb')
        kwargs['data'] = fp.read()
        self.render_data(kwargs)

    def render_json(self, kwargs):
        if not 'headers' in kwargs:
            kwargs['headers'] = {}

        kwargs['headers']['Content-Type'] = 'application/json'
        kwargs['data'] = json.dumps(kwargs['json'])
        self.render_data(kwargs)

    def render_plain(self, kwargs):
        if not 'headers' in kwargs:
            kwargs['headers'] = {}

        kwargs['headers']['Content-Type'] = 'text/plain'
        kwargs['data'] = kwargs['plain']
        self.render_data(kwargs)

    def render_data(self, kwargs):
        self.send_response(kwargs.get('status') or 200)

        body = b''
        if isinstance(kwargs['data'], str):
            body = kwargs['data'].encode()
        else:
            body = kwargs['data']

        # Send headers
        headers = self.filter_headers(kwargs.get('headers'), {
            'TRANSFER-ENCODING': 'CHUNKED',
        })
        headers['Content-Length'] = len(body)
        self.enable_cors()
        self.render_headers(headers)
        self.end_headers()

        # Send body
        self.wfile.write(body)

    def filter_headers(self, headers, blacklist = {}):
        if not headers:
            return {}

        new_blacklist = {}
        for key, val in blacklist.items():
            new_blacklist[key.upper()] = val

        new_headers = headers.copy()
        for key, val in headers.items():
            if key.upper() in new_blacklist:
                if not new_blacklist[key.upper()]:
                    del new_headers[key.upper()]
                elif val.upper() == new_blacklist[key.upper()]:
                    del new_headers[key.upper()]

        return new_headers

    def render_headers(self, headers):
        if headers:
            for key, val in headers.items():
                self.send_header(key, val)

    ### Routes

    ROUTES = {
        'GET': [
            [CONFIGS_PATH, ConfigsController.instance().get_configs],
            ['/'.join([CONFIGS_PATH, 'summary']), ConfigsController.instance().get_configs_summary],
            ['/'.join([CONFIGS_PATH, 'policies']), ConfigsController.instance().get_configs_policies],
            ['/'.join([PROXY_PATH, 'get']), ProxyController.instance().do_GET],
            [STATUS_PATH, StatusesController.instance().get_status],
        ],
        'POST': [
            ['/'.join([PROXY_PATH, 'post']), ProxyController.instance().do_POST],
        ],
        'PUT': [
            [CONFIGS_PATH, ConfigsController.instance().put_configs],
            ['/'.join([PROXY_PATH, 'put']), ProxyController.instance().do_PUT],
            [STATUS_PATH, StatusesController.instance().put_status],
        ]
    }

def start_server(host, port):
    httpd = HTTPServer((host, port), SimpleHTTPRequestHandler)
    httpd.serve_forever()

def run(**kwargs):
    ui_host = kwargs['ui_host']
    ui_port = kwargs['ui_port']

    os.environ[env_vars.AGENT_URL] = f"http://{kwargs['ui_host']}:{kwargs['ui_port']}"

    print(f"UI server listening at http://{ui_host}:{ui_port}\n")

    thread = threading.Thread(target=start_server, args=(ui_host, ui_port))
    thread.start()
