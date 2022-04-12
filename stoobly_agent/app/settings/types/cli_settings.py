from typing import TypedDict

class FeatureSettings:
  dev_tools: bool
  exec: bool
  remote: bool

class CLISettings(TypedDict):
  features: FeatureSettings