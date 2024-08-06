import os

class App():

  def __init__(self, path: str):
    self.__path = path or os.getcwd()

  @property
  def exists(self):
    return os.path.exists(self.path)

  @property
  def path(self):
    return self.__path