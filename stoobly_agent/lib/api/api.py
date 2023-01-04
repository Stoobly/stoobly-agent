import os
import pdb
import requests

from stoobly_agent.config.constants.env_vars import HTTP_PROXY, HTTPS_PROXY, NO_PROXY
from stoobly_agent.app.settings import Settings

class Api():

    def without_proxy(self, handler):
      settings = Settings.instance()

      no_proxy = os.environ.get(NO_PROXY)
      os.environ[NO_PROXY] = settings.remote.api_url

      current_proxies = self.set_proxy('')

      res = handler()

      for key, val in current_proxies.items():
        if not val:
          continue
        
        if isinstance(val, str):
          os.environ[key] = val
        
      if isinstance(no_proxy, str): 
        os.environ[NO_PROXY] = no_proxy

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

    def put(self, url, **kwargs):
      handler = lambda: requests.put(url, **kwargs)
      return self.without_proxy(handler)
