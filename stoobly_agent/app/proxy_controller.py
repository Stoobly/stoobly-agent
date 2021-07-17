import pdb
import requests

from http.cookies import SimpleCookie

from ..lib import headers

class ProxyController:
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

    def do_DELETE(self, context):
        self.__proxy(context, requests.delete)

    def do_GET(self, context):
        self.__proxy(context, requests.get)

    def do_HEAD(self, context):
        self.__proxy(context, requests.head)

    def do_OPTIONS(self, context):
        self.__proxy(context, requests.options)

    def do_PATCH(self, context):
        self.__proxy(context, requests.patch)

    def do_POST(self, context):
        self.__proxy(context, requests.post)

    def do_PUT(self, context):
        self.__proxy(context, requests.put)

    def __proxy(self, context, method):
        url = self.__get_url(context)
        if not url:
            return
        pdb.set_trace()
        res = method(
            url,
            cookies = self.__get_cookies(context),
            data = self.__get_body(context),
            headers = dict(context.headers),
            params = context.params
        )

        context.render(
            headers = res.headers,
            data = res.content,
            status = res.status_code,
        )

    def __get_url(self, context):
        service_url = context.headers.get(headers.SERVICE_URL)

        if not service_url:
            context.render(
                plain = f"Invalid {headers.SERVICE_URL} header {service_url}",
                status = 400
            )
            return None

        request_path = context.headers.get(headers.REQUEST_PATH)

        if not request_path:
            context.render(
                plain = f"Invalid {headers.REQUEST_PATH} header {service_url}",
                status = 400
            )
            return None

        return f"{service_url}{request_path}"

    def __get_cookies(self, context):
        return SimpleCookie(context.headers.get('Cookie'))

    def __get_body(self, context):
        content_length = context.headers.get('Content-Length')
        if content_length:
            return context.rfile.read(content_length)


