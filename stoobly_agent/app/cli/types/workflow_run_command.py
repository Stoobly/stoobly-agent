from typing import TypedDict

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