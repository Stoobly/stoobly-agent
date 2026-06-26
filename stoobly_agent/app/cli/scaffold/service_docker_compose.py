from stoobly_agent.app.cli.scaffold.app import App
from stoobly_agent.app.cli.scaffold.constants import SERVICES_NAMESPACE

class ServiceDockerCompose():
  def __init__(self, app_dir_path: str, namespace: str, workflow_name: str, service_name: str, hostname: str):
    self.service_name = service_name
    self.hostname = hostname
    self.container_name = f"{namespace}-{service_name}-1"
    self.proxy_container_name = f"{namespace}-{service_name}.proxy-1"
    self.init_container_name = f"{namespace}-{service_name}.init-1"

    app = App(app_dir_path)
    self.docker_compose_path = f"{app.data_dir_path}/{SERVICES_NAMESPACE}/{service_name}/{workflow_name}/docker-compose.yml"
    self.init_script_path = f"{app.data_dir_path}/{SERVICES_NAMESPACE}/{service_name}/{workflow_name}/init"
