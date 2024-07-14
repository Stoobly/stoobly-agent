import os
import shutil

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

  def copy_file(self, src: str, dest_dir: str):
    if not os.path.exists(src):
      return None

    data_dir_parent = os.path.dirname(self.data_dir.path)
    dest_file_path = src.replace(data_dir_parent, dest_dir)
    dest_dir_path = os.path.dirname(dest_file_path)

    if not os.path.exists(dest_dir_path):
      os.makedirs(dest_dir_path, exist_ok=True)

    shutil.copy(src, dest_file_path)

    return dest_file_path