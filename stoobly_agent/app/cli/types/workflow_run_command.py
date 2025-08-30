from typing import TypedDict, List, Callable, Optional

class ComposeOptions(TypedDict):
  namespace: str
  user_id: str

class BuildOptions(ComposeOptions):
  user_id: str
  verbose: bool

class DownOptions(ComposeOptions):
  extra_compose_path: str
  rmi: bool

class UpOptions(ComposeOptions):
  attached: bool
  pull: bool

# Workflow-specific option types
class WorkflowDownOptions(TypedDict, total=False):
  print_service_header: Optional[Callable[[str], None]]
  extra_entrypoint_compose_path: Optional[str]
  namespace: Optional[str]
  rmi: bool
  user_id: Optional[int]
  # CLI-specific options that get passed through
  containerized: bool
  dry_run: bool
  log_level: str
  script_path: Optional[str]
  service: List[str]
  app_dir_path: Optional[str]
  context_dir_path: Optional[str]

class WorkflowUpOptions(TypedDict, total=False):
  print_service_header: Optional[Callable[[str], None]]
  extra_entrypoint_compose_path: Optional[str]
  namespace: Optional[str]
  pull: bool
  user_id: Optional[int]
  detached: bool
  # CLI-specific options that get passed through
  containerized: bool
  dry_run: bool
  log_level: str
  script_path: Optional[str]
  service: List[str]
  no_publish: bool
  verbose: bool
  mkcert: bool
  app_dir_path: Optional[str]
  ca_certs_dir_path: Optional[str]
  certs_dir_path: Optional[str]
  context_dir_path: Optional[str]

class WorkflowLogsOptions(TypedDict, total=False):
  print_service_header: Optional[Callable[[str], None]]
  container: List[str]
  follow: bool
  namespace: Optional[str]
  # CLI-specific options that get passed through
  containerized: bool
  dry_run: bool
  log_level: str
  script_path: Optional[str]
  service: List[str]
  app_dir_path: Optional[str]