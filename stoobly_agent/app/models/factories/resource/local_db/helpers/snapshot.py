from typing import TypedDict

from stoobly_agent.config.data_dir import DataDir

class Snapshot():

  def __init__(self, uuid: str):
    self.__uuid = uuid
    self.__data_dir = DataDir.instance()

  @property
  def uuid(self):
    return self.__uuid

  @property
  def data_dir(self):
    return self.__data_dir