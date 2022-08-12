import pdb

from typing import Callable, TypedDict

from stoobly_agent.app.settings import Settings
from stoobly_agent.lib.utils.conditional_decorator import ConditionalDecorator

class LifeCycleOptions(TypedDict):
  before_action: Callable[[], None]
  after_action: Callable[[], None]

class CommandOptions(TypedDict):
  disable: LifeCycleOptions
  enable: LifeCycleOptions
  show: LifeCycleOptions

class ConfigDecorator():
  __main = None
  __settings = None
  __setting = None # e.g. features.remote

  def __init__(self, main, settings: Settings, setting: str, options: CommandOptions = {}):
    self.__main = main
    self.__options = options
    self.__settings = settings
    self.__setting = setting

  def decorate(self):
    self.__with_enable()
    self.__with_disable()
    self.__with_show()
    return self.__main

  def __with_enable(self):
    life_cycle_options = self.__options.get('enable') or {}

    @self.__main.command()
    @ConditionalDecorator(life_cycle_options.get('set_options'), bool(life_cycle_options.get('set_options')))
    def enable(**kwargs):
      if life_cycle_options:
        before_action = life_cycle_options['before_action']
        if isinstance(before_action, Callable):
          before_action(**kwargs)

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
