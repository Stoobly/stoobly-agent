import os
import shutil

from stoobly_agent.config.data_dir import DataDir, DATA_DIR_NAME

class App():

  def __init__(self, path: str, namespace: str, **kwargs):
    path = path or os.getcwd()
    data_dir: DataDir = DataDir.instance(path) 

    self.__scaffold_dir_path = data_dir.path
    self.__certs_dir_path = os.path.join(data_dir.tmp_dir_path, 'certs')
    self.__context_dir_path = data_dir.context_dir_path
    self.__dir_path = path
    self.__name = os.path.basename(self.__dir_path)
    self.__network = os.path.basename(self.__dir_path)
    self.__namespace = namespace
    self.__skip_validate_path = not not kwargs.get('skip_validate_path')

  @property
  def certs_dir_path(self):
    return self.__certs_dir_path

  @certs_dir_path.setter
  def certs_dir_path(self, v: str):
    self.__validate_path(v)
    self.__certs_dir_path = v

  @property
  def context_dir_path(self):
    return self.__context_dir_path

  @context_dir_path.setter
  def context_dir_path(self, v: str):
    self.__validate_path(v)
    self.__context_dir_path = v 

  @property
  def data_dir_path(self):
    return os.path.join(self.context_dir_path, DATA_DIR_NAME)

  @property
  def exists(self):
    return os.path.exists(self.dir_path)

  @property
  def name(self):
    return self.__name

  @name.setter
  def name(self, v: str):
    self.__name = v

  @property
  def network(self):
    return self.__network

  @network.setter
  def network(self, v: str):
    self.__network = v

  @property
  def namespace(self):
    return self.__namespace

  @property
  def namespace_path(self):
    return os.path.join(self.data_dir_path, self.namespace)

  @property
  def dir_path(self):
    return self.__dir_path

  @property
  def scaffold_dir_path(self):
    return self.__scaffold_dir_path

  @property
  def scaffold_namespace_path(self):
    return os.path.join(self.scaffold_dir_path, self.namespace)

  def copy_folders_and_hidden_files(self, src, dst):
      os.makedirs(dst, exist_ok=True)

      # Walk through the source directory
      for root, dirs, files in os.walk(src):
          # Copy hidden files only
          for file_name in files:
              src_file_path = os.path.join(root, file_name)
              dst_file_path = os.path.join(dst, os.path.relpath(root, src), file_name)

              if not file_name.startswith('.'):
                  if os.path.exists(dst_file_path):
                      continue

              os.makedirs(os.path.dirname(dst_file_path), exist_ok=True)  # Create directories in destination
              shutil.copy2(src_file_path, dst_file_path)

  def __validate_path(self, v: str):
    if not isinstance(v, str):
      raise TypeError('Expected a str')

    if not self.__skip_validate_path:
      if not os.path.exists(v):
        raise ValueError(f"{v} does not exist")