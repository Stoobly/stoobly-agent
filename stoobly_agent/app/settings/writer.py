from . import Settings

from stoobly_agent.config.constants import mode

class SettingsWriter():
  __settings = None

  def __init__(self, settings: Settings):
    self.__settings = settings

  def write_active_mode(self, value) -> None:
    if value in [mode.MOCK, mode.NONE, mode.RECORD, mode.TEST]:
      config = self.__settings.to_hash()
      config['mode']['active'] = value
      self.__settings.update(config)

  def write_proxy_url(self, value) -> None:
    config = self.__settings.to_hash()
    config['proxy_url'] = value
    self.__settings.update(config)

  def write_remote_enabled(self, value: bool) -> None:
    if type(value) == bool:
      config = self.__settings.to_hash()
      config['remote_enabled'] = value
      self.__settings.update(config)