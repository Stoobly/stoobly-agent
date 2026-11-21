from typing import Literal, Optional, TypedDict

REQUEST_RESOURCE = 'request'
SCENARIO_RESOURCE = 'scenario'

DELETE_ACTION = 'DELETE'
PUT_ACTION = 'PUT'

Action = Literal[f"{DELETE_ACTION}", f"{PUT_ACTION}"]
Resource = Literal[f"{REQUEST_RESOURCE}", f"{SCENARIO_RESOURCE}"]

class SnapshotOptions(TypedDict, total=False):
  action: Action
  format: Optional[int]
  data_dir_path: Optional[str]

class RequestSnapshotOptions(SnapshotOptions, total=False):
  decode: bool
