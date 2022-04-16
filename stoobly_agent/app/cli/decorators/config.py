import pdb

from stoobly_agent.app.settings import Settings

class ConfigDecorator():
  __main = None
  __settings = None
  __setting = None # e.g. features.remote

  def __init__(self, main, settings: Settings, setting: str):
    self.__main = main
    self.__settings = settings
    self.__setting = setting

  def decorate(self):
    self.__with_enable()
    self.__with_disable()
    self.__with_show()
    return self.__main

  def __with_enable(self):
    @self.__main.command()
    def enable():
      settings_hash = self.__settings.to_dict()
      self.__resolve(settings_hash, self.__setting, value=True)
      self.__settings.write(settings_hash)
      print(f"{self.__setting} enabled")

  def __with_disable(self):
    @self.__main.command()
    def disable():
      settings_hash = self.__settings.to_dict()
      self.__resolve(settings_hash, self.__setting, value=False)
      self.__settings.write(settings_hash)
      print(f"{self.__setting} disabled")

  def __with_show(self):
    @self.__main.command()
    def show():
      settings_hash = self.__settings.to_dict()
      print(self.__resolve(settings_hash, self.__setting))

  def __resolve(self, settings_hash, setting: str, **kwargs):
    keys = setting.split('.')
    length = len(keys)

    i = 0
    t = settings_hash
    for key in keys:
      if type(t) == dict:
        if i == length - 1 and 'value' in kwargs:
          t[key] = kwargs['value']

        t = t.get(key) 
      elif type(t) == list:
        if i == length - 1 and 'value' in kwargs:
          t[key] = kwargs['value']

        t = t[key]
      else:
        return None

      if not t:
        break

      i += 1

    return t
