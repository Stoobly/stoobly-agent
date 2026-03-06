
class ManagedServicesDockerCompose():
  def __init__(self, namespace: str = None, workflow_name: str = None):
    prefix = namespace if namespace else workflow_name
    self.init_container_name = f"{prefix}-build.init-1"
    self.configure_container_name = f"{prefix}-build.configure-1"
    self.gateway_container_name = f"{prefix}-gateway.service-1"
    self.mock_ui_container_name = f"{prefix}-stoobly_ui.service-1"
    self.entrypoint_init_container_name = f"{prefix}-entrypoint.init-1"
    self.entrypoint_configure_container_name = f"{prefix}-entrypoint.configure-1"
