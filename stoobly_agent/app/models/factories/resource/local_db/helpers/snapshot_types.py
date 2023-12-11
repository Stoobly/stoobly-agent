from typing import Literal, TypedDict

REQUEST_RESOURCE = 'request'
SCENARIO_RESOURCE = 'scenario'

DELETE_ACTION = 'DELETE'
PUT_ACTION = 'PUT'

Action = Literal[f"{DELETE_ACTION}", f"{PUT_ACTION}"]
Resource = Literal[f"{REQUEST_RESOURCE}", f"{SCENARIO_RESOURCE}"]

class SnapshotOptions(TypedDict):
  action: Action

class RequestSnapshotOptions(SnapshotOptions):
  decode: bool