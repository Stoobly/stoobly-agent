import os

from stoobly_agent.config.constants import env_vars

from .types.remote_settings import RemoteSettings as IRemoteSettings

class RemoteSettings:

  def __init__(self, remote_settings: IRemoteSettings):
    self.__remote_settings = remote_settings

    self.__api_key = self.api_key_before_change
    self.__api_url = self.api_url_before_change

  @property
  def api_key_before_change(self):
    return self.__remote_settings.get('api_key')

  @property
  def api_key(self):
    if self.__api_key != self.api_key_before_change:
      return self.__api_key

    if os.environ.get(env_vars.API_KEY):
      return os.environ[env_vars.API_KEY]

    return self.__api_key

  @property
  def api_url_before_change(self):
    return self.__remote_settings.get('api_url')

  @property
  def api_url(self):
    if self.__api_url != self.api_url_before_change:
      return self.__api_url

    if os.environ.get(env_vars.API_URL):
      return os.environ[env_vars.API_URL]

    return self.__api_url

  @api_url.setter
  def api_url(self, v):
    self.__api_url = v

  def to_dict(self) -> IRemoteSettings:
    return {
      'api_key': self.__api_key,
      'api_url': self.__api_url,
    }