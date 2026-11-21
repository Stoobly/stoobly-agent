from typing import Literal, Optional, TypedDict

REQUEST_RESOURCE: Literal['request'] = 'request'
SCENARIO_RESOURCE: Literal['scenario'] = 'scenario'

DELETE_ACTION: Literal['DELETE'] = 'DELETE'
PUT_ACTION: Literal['PUT'] = 'PUT'

Action = Literal['DELETE', 'PUT']
Resource = Literal['request', 'scenario']

class SnapshotOptions(TypedDict, total=False):
  action: Action
  format: Optional[int]
  data_dir_path: Optional[str]

class RequestSnapshotOptions(SnapshotOptions, total=False):
  decode: bool
