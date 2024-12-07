import pdb

from .app import App
from .app_command import AppCommand

class AppValidateCommand(AppCommand):
  def __init__(self, app: App, **kwargs):
    super().__init__(app)

  @property
  def app_name(self):
    return self.app.name

  def validate(self):
    workflows = ["ci", "record"]
    for workflow in workflows:
      self.validate_core_components()

      # validate_workflow.validate()

      # services = []
      # for service in services:
      #   self.validate_service(service)

    return True

