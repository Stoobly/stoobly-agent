import glob
import os
import pdb
import shutil

from .app import App
from .service_command import ServiceCommand
from stoobly_agent.lib.logger import Logger


LOG_ID = 'ServiceDeleteCommand'

class ServiceDeleteCommand(ServiceCommand):
  def __init__(self, app: App, **kwargs):
    super().__init__(app, **kwargs)

  def delete(self) -> None:
    Logger.instance(LOG_ID).debug(f"Deleting service: {self.service_name}, path: {self.service_path}")

    # Delete service directory
    shutil.rmtree(self.service_path)

    # Delete certs for that hostname if HTTPS
    if self.service_config.scheme == 'https':
      certs_dir_path_escaped = glob.escape(self.app.certs_dir_path)
      hostname = self.service_config.hostname
      pattern = os.path.join(certs_dir_path_escaped, f"{hostname}*")

      cert_paths = glob.glob(pattern)
      for cert_path in cert_paths:
        Logger.instance(LOG_ID).debug(f"Deleting cert_path: {cert_path}")
        os.remove(cert_path)

    return None

