import os
import pdb
import requests

from stoobly_agent.config.constants.env_vars import HTTP_PROXY, HTTPS_PROXY
from stoobly_agent.app.settings import Settings

class Api():

    def without_proxy(self, handler):
      current = self.set_proxy('')

      res = handler()

      for key, val in current.items():
        if not val:
          continue
        
        os.environ[key] = val

      return res

    def with_proxy(self, handler):
      settings = Settings.instance()
      proxy_url = settings.proxy.url
      current = self.set_proxy(proxy_url)

      res = handler()

      for key, val in current.items():
        os.environ[key] = val

      return res

    def set_proxy(self, val):
      current = {}

      current[HTTP_PROXY] = os.environ.get(HTTP_PROXY)
      os.environ[HTTP_PROXY] = val

      current[HTTPS_PROXY] = os.environ.get(HTTPS_PROXY)
      os.environ[HTTPS_PROXY] = val

      current[HTTP_PROXY.lower()] = os.environ.get(HTTP_PROXY.lower())
      os.environ[HTTP_PROXY.lower()] = val

      current[HTTPS_PROXY.lower()] = os.environ.get(HTTPS_PROXY.lower())
      os.environ[HTTPS_PROXY.lower()] = val

      return current

    def get(self, url, **kwargs):
      handler = lambda: requests.get(url, **kwargs)
      return self.without_proxy(handler)

    def post(self, url, **kwargs):
      handler = lambda: requests.post(url, **kwargs)
      return self.without_proxy(handler)
