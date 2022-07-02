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
  def api_key(self) -> str:
    def get():
      if self.__api_key != self.api_key_before_change:
        return self.__api_key

      if os.environ.get(env_vars.API_KEY):
        return os.environ[env_vars.API_KEY]

      return self.__api_key
    
    _api_key = get()
    return _api_key.strip() if isinstance(_api_key, str) else ''

  @api_key.setter
  def api_key(self, v: str):
    self.__api_key = v.strip()

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