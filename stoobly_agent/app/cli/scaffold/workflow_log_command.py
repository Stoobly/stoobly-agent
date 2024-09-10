import os
import pdb
import yaml

from .app import App
from .workflow_command import WorkflowCommand

class WorkflowLogCommand(WorkflowCommand):
  def __init__(self, app: App, **kwargs):
    super().__init__(app, **kwargs)

  def all(self):
    commands = []
    containers = self.containers

    for container in containers:
      command = ['docker', 'logs', container]

      commands.append(' '.join(command))

    return commands
