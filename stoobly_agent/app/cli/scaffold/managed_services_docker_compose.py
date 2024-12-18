
class ManagedServicesDockerCompose():
  def __init__(self, target_workflow_name):
    self.core_init_container_name = f"{target_workflow_name}-build.init-1" 
    self.core_configure_container_name = f"{target_workflow_name}-build.configure-1"
    self.core_gateway_container_name = f"{target_workflow_name}-gateway.service-1"
    self.core_mock_ui_container_name = f"{target_workflow_name}-stoobly_ui.service-1"
    self.core_entrypoint_init_container_name = f"{target_workflow_name}-entrypoint.init-1" 
    self.core_entrypoint_configure_container_name = f"{target_workflow_name}-entrypoint.configure-1"

