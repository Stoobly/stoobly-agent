from ..mitmproxy.request_facade import MitmproxyRequestFacade

class ProxyRequest:
    def __init__(self, request: MitmproxyRequestFacade, upstream_url: str = None):
        self._id = None
        self.request = request

        self.upstream_url = upstream_url

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, v):
        self._id = v

    def url(self):
        url = self.request.url

        if not self.upstream_url:
            return url

        return url.replace(self.request.base_url, self.upstream_url)
