import pdb

from typing import TypedDict

from stoobly_agent.lib.logger import DEBUG

from .app import App
from .constants import WORKFLOW_CONTAINER_TEMPLATE
from .workflow_command import WorkflowCommand

class WorkflowLogCommand(TypedDict):
  container: str
  follow: bool
  namespace: str

class WorkflowLogCommand(WorkflowCommand):
  def __init__(self, app: App, **kwargs):
    super().__init__(app, **kwargs)

  def build(self, **options: WorkflowLogCommand):
    commands = []
    containers = self.containers
    allowed_containers = list(
      map(
        lambda container: WORKFLOW_CONTAINER_TEMPLATE.format(
          container=container, service_name=self.service_name
        ), options.get('containers') or []
      )
    )

    for index, container in enumerate(containers):
      if container not in allowed_containers:
        continue

      container_name = self.container_name(container, options.get('namespace'))
      commands.append(f"echo \"=== Logging {container_name}\"")
      if options.get('follow') and index == len(containers) - 1:
        command = ['docker', 'logs', '--follow', container_name]
      else:
        command = ['docker', 'logs', container_name]
      commands.append(' '.join(command))

    return commands

  def container_name(self, container, namespace=None):
    return f"{namespace or self.workflow_name}-{container}-1"