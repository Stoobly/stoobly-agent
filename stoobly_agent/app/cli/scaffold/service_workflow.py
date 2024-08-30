import os

from .app import App
from .workflow import Workflow

class ServiceWorkflow(Workflow):

  def __init__(self, service_name: str, workflow_name: str, app: App):
    super().__init__(workflow_name, app)
    self._service_name = service_name

  @property
  def path(self):
    return os.path.join(self.app.scaffold_namespace_path, self.service_name, self.workflow_name)

  @property
  def service_name(self):
    return self._service_name