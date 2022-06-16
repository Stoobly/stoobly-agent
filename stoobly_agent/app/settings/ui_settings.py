import os

from stoobly_agent.config.constants import env_vars

from .types.ui_settings import UISettings as IUISettings

class UISettings:

  def __init__(self, ui_settings: IUISettings):
    self.__ui_settings = ui_settings

    self.__active = self.active_before_change
    self.__url = self.url_before_change

  @property
  def active_before_change(self) -> bool:
    return self.__ui_settings.get('active')

  @property
  def active(self) -> bool:
    if self.__active != self.active_before_change:
      return self.__active

    if os.environ.get(env_vars.AGENT_IS_HEADLESS):
        return True

    return self.__active or False

  @active.setter
  def active(self, v):
    self.__active = v

  @property
  def url_before_change(self) -> str:
    return self.__ui_settings.get('url')

  @property
  def url(self) -> str:
    if self.__url != self.url_before_change:
        return self.__url

    if os.environ.get(env_vars.AGENT_URL):
        return os.environ[env_vars.AGENT_URL]

    return self.__url or ''

  @url.setter
  def url(self, v):
    self.__url = v

  def to_dict(self):
    return {
      'active': self.__active,
      'url': self.__url,
    }