from ..mitmproxy.request_facade import MitmproxyRequestFacade

class ProxyRequest:
    def __init__(self, request: MitmproxyRequestFacade, upstream_url: str):
        self.request = request

        self.upstream_url = upstream_url

    def url(self):
        url = self.request.url

        return url.replace(self.request.base_url, self.upstream_url)
