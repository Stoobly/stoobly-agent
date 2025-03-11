import os
import shutil

from stoobly_agent.config.data_dir import DataDir, DATA_DIR_NAME

class App():

  def __init__(self, path: str, scaffold_namespace: str, **kwargs):
    path = os.path.abspath(path) or os.getcwd()
    data_dir: DataDir = DataDir.instance(path) 

    self.__data_dir_path = data_dir.path
    self.__ca_certs_dir_path = kwargs.get('ca_certs_dir_path') or data_dir.mitmproxy_conf_dir_path
    self.__certs_dir_path = kwargs.get('certs_dir_path') or data_dir.certs_dir_path
    self.__context_dir_path = kwargs.get('context_dir_path') or data_dir.context_dir_path
    self.__data_dir = data_dir
    self.__dir_path = path
    self.__scaffold_namespace = scaffold_namespace
    self.__skip_validate_path = not not kwargs.get('dry_run')

  @property
  def ca_certs_dir_path(self):
    return self.__ca_certs_dir_path

  @ca_certs_dir_path.setter
  def ca_certs_dir_path(self, v: str):
    self.__validate_path(v)
    self.__certs_dir_path = v

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
  def data_dir(self):
    return self.__data_dir

  @property
  def data_dir_path(self):
    return os.path.join(self.context_dir_path, DATA_DIR_NAME)

  @property
  def valid(self):
    return os.path.exists(self.scaffold_namespace_path)

  @property
  def scaffold_namespace(self):
    return self.__scaffold_namespace

  @property
  def scaffold_namespace_path(self):
    return os.path.join(self.data_dir_path, self.scaffold_namespace)

  @property
  def dir_path(self):
    return self.__dir_path

  @property
  def data_dir_path(self):
    return self.__data_dir_path

  @property
  def scaffold_namespace_path(self):
    return os.path.join(self.data_dir_path, self.scaffold_namespace)

  @property
  def services(self):
    return list(map(lambda path: os.path.basename(path), self.service_paths))

  @property
  def service_paths(self):
    services_dir = os.path.join(self.data_dir_path, self.scaffold_namespace)

    services = []
    for filename in os.listdir(services_dir):
      path = os.path.join(services_dir, filename)
      if not os.path.isdir(path):
        continue
      
      services.append(path)

    return services

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