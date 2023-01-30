import json
import os
import pdb

from mitmproxy.options import Options
from mitmproxy.tools.dump import DumpMaster

from stoobly_agent.config.data_dir import DataDir
from stoobly_agent.lib.logger import Logger

class MitmproxyConfig():
  MITMPROXY_DIR_NAME = '.mitmproxy'
  MITMPROXY_OPTIONS_FILE_NAME = 'options.json'

  __instance = None
  __master = None

  def __init__(self, master: DumpMaster):
    if self.__instance:
        raise RuntimeError('Call instance() instead')
    else:
        self.__master = master 

        self.__mitmproxy_dir_path = os.path.join(os.path.expanduser('~'), self.MITMPROXY_DIR_NAME)

        if not os.path.exists(self.__mitmproxy_dir_path):
            os.mkdir(self.__mitmproxy_dir_path)

  @classmethod
  def instance(cls, master = None):
      if cls.__instance is None:
        cls.__instance = cls(master)

      return cls.__instance

  @property
  def ca_cert_pem_path(self):
      path = os.path.join(self.__mitmproxy_dir_path, 'mitmproxy-ca-cert.pem')

      if not os.path.exists(path):
          return ''

      return path

  def with_master(self, master: DumpMaster):
    self.__master = master

  def get(self, key: str):
    if not self.__master:
      try:
        fp = open(self.options_json_path, 'r')
        contents = fp.read()
        fp.close()
        options = json.loads(contents)
        return options.get(key)
      except Exception as e:
        pass
    else:
      options: Options = self.__master.options

      if key in options:
        for k, val in options.items():
          if key == k:
            return val.current()

  def set(self, option: str):
    if self.__master:
      Logger.instance().debug(f"Setting proxy option {option}")
      self.__master.options.set(option)

  @property
  def options_json_path(self):
    return os.path.join(DataDir.instance().tmp_dir_path, self.MITMPROXY_OPTIONS_FILE_NAME)

  def dump(self):
    if not self.__master:
      return

    options = {}
    for k, v in self.__master.options.items():
      options[k] = v.current()

    fp = open(self.options_json_path, 'w')
    fp.write(json.dumps(options, indent=2, sort_keys=True))
    fp.close()