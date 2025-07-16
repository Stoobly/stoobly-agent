from .app import App

class Command():

  def __init__(self, app: App):
    self.__app = app
    self.__scaffold_namespace = app.scaffold_namespace

  @property
  def app(self):
    return self.__app

  @property
  def scaffold_namespace(self):
    return self.__scaffold_namespace