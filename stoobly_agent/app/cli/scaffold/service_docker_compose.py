from stoobly_agent.config.data_dir import DataDir


class ServiceDockerCompose():
  def __init__(self, app_dir_path, target_workflow_name, service_name, hostname):
    self.service_name = service_name
    self.hostname = hostname
    self.container_name = f"{target_workflow_name}-{service_name}-1"
    self.proxy_container_name = f"{target_workflow_name}-{service_name}.proxy-1"
    self.init_container_name = f"{target_workflow_name}-{service_name}.init-1"
    self.configure_container_name = f"{target_workflow_name}-{service_name}.configure-1"

    data_dir_path = DataDir.instance(app_dir_path).path
    self.docker_compose_path = f"{data_dir_path}/docker/{service_name}/{target_workflow_name}/docker-compose.yml"
    self.init_script_path = f"{data_dir_path}/docker/{service_name}/{target_workflow_name}/bin/init"
