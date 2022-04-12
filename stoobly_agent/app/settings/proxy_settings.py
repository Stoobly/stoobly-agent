import os

from stoobly_agent.config.constants import env_vars

from .data_settings import DataSettings
from .filter_settings import FilterSettings
from .firewall_settings import FirewallSettings
from .intercept_settings import InterceptSettings
from .types.proxy_settings import ProxySettings as IProxySettings

class ProxySettings:

  def __init__(self, proxy_settings: IProxySettings):
    self.__proxy_settings = proxy_settings or {}

    self.__data = DataSettings(self.__proxy_settings.get('data'))
    self.__filter = FilterSettings(self.__proxy_settings.get('filter')) 
    self.__firewall = FirewallSettings(self.__proxy_settings.get('firewall'))
    self.__intercept = InterceptSettings(self.__proxy_settings.get('intercept'))
    self.__url = self.__proxy_settings.get('url')

  @property
  def data(self) -> DataSettings:
    return self.__data

  @property
  def filter(self) -> FilterSettings:
    return self.__filter

  @property
  def firewall(self) -> FirewallSettings:
    return self.__firewall

  @property
  def intercept(self) -> InterceptSettings:
    return self.__intercept

  @property
  def url(self) -> str:
    if os.environ.get(env_vars.AGENT_PROXY_URL):
        return os.environ[env_vars.AGENT_PROXY_URL]

    return self.__url or ''

  @url.setter
  def url(self, v):
    self.__url = v

  def to_dict(self) -> IProxySettings:
    return {
      'data': self.__data.to_dict(),
      'filter': self.__filter.to_dict(),
      'firewall': self.__firewall.to_dict(),
      'intercept': self.__intercept.to_dict(),
      'url': self.__url,
    }