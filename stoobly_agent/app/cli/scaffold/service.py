from .app import App

class Service():

  def __init__(self, service_name: str, app: App):
    self.__app = app
    self.__service_name = service_name

  @property
  def app(self):
    return self.__app

  @property
  def service_name(self):
    return self.__service_name