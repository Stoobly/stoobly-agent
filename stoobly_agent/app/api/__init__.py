import os
import pdb
import threading

from http.server import HTTPServer

from stoobly_agent.config.constants import env_vars

from .application_http_request_handler import ApplicationHTTPRequestHandler

def start_server(host, port):
    httpd = HTTPServer((host, port), ApplicationHTTPRequestHandler)
    httpd.serve_forever()

def run(**kwargs):
    ui_host = kwargs['ui_host']
    ui_port = kwargs['ui_port']

    os.environ[env_vars.AGENT_URL] = f"http://{kwargs['ui_host']}:{kwargs['ui_port']}"

    print(f"UI server listening at http://{ui_host}:{ui_port}\n")

    thread = threading.Thread(target=start_server, args=(ui_host, ui_port))
    thread.start()
