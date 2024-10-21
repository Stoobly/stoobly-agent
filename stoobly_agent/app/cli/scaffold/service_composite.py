from stoobly_agent.config.data_dir import DATA_DIR_NAME


class ServiceComposite():
  def __init__(self, app_dir_path, target_workflow_name, service_name, hostname):
    self.service_name = service_name
    self.hostname = hostname
    self.service_container_name = f"/{target_workflow_name}-{service_name}-1"
    self.service_proxy_container_name = f"/{target_workflow_name}-{service_name}.proxy-1"
    self.service_init_container_name = f"/{target_workflow_name}-{service_name}.init-1"
    self.service_configure_container_name = f"/{target_workflow_name}-{service_name}.configure-1"
    self.docker_compose_path = f"{app_dir_path}/{DATA_DIR_NAME}/docker/{service_name}/{target_workflow_name}/docker-compose.yml"
    self.init_script_path = f"{app_dir_path}/{DATA_DIR_NAME}/docker/{service_name}/{target_workflow_name}/bin/init"

