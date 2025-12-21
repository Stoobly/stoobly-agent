import os
import pdb
import threading

from http.server import HTTPServer

from stoobly_agent.lib.logger import Logger

from .application_http_request_handler import ApplicationHTTPRequestHandler

LOG_ID = 'UI'

def start_server(host, port):
    httpd = HTTPServer((host, port), ApplicationHTTPRequestHandler)
    httpd.serve_forever()

def run(**kwargs):
    Logger.instance(LOG_ID).info(f"starting and listening at {kwargs['ui_host']}:{kwargs['ui_port']}")
    thread = threading.Thread(target=start_server, args=(kwargs['ui_host'], kwargs['ui_port']))
    return thread.start()