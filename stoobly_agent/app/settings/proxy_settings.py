from nis import match
import os

from stoobly_agent.config.constants import env_vars

from .data_settings import DataSettings
from .firewall_settings import FirewallSettings
from .intercept_settings import InterceptSettings
from .match_settings import MatchSettings
from .rewrite_settings import RewriteSettings
from .types.proxy_settings import ProxySettings as IProxySettings

class ProxySettings:

  def __init__(self, proxy_settings: IProxySettings):
    self.__proxy_settings = proxy_settings or {}

    self.__data = DataSettings(self.__proxy_settings.get('data'))
    self.__firewall = FirewallSettings(self.__proxy_settings.get('firewall'))
    self.__intercept = InterceptSettings(self.__proxy_settings.get('intercept'))
    self.__match = MatchSettings(self.__proxy_settings.get('match'))
    self.__rewrite = RewriteSettings(self.__proxy_settings.get('rewrite')) 
    self.__url = self.__proxy_settings.get('url')

  @property
  def data(self) -> DataSettings:
    return self.__data

  @property
  def rewrite(self) -> RewriteSettings:
    return self.__rewrite

  @property
  def firewall(self) -> FirewallSettings:
    return self.__firewall

  @property
  def intercept(self) -> InterceptSettings:
    return self.__intercept

  @property
  def match(self) -> MatchSettings:
    return self.__match

  @property
  def url(self) -> str:
    if os.environ.get(env_vars.AGENT_PROXY_URL):
        return os.environ[env_vars.AGENT_PROXY_URL]

    return self.__url or ''

  @url.setter
  def url(self, v):
    self.__url = v

  def to_dict(self) -> IProxySettings:
    _dict = {
      'data': self.__data.to_dict(),
      'firewall': self.__firewall.to_dict(),
      'intercept': self.__intercept.to_dict(),
      'match': self.__match.to_dict(),
      'rewrite': self.__rewrite.to_dict(),
    }

    if self.__url:
      _dict['url'] = self.__url

    return _dict