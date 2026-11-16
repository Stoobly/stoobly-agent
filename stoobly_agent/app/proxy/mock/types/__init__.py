from typing import Callable, Optional, TypedDict, Union

class Route(TypedDict):
  path: str

class Fixtures(TypedDict):
  DELETE: Route
  GET: Route
  POST: Route
  PUT: Route
  
class LifecycleHooksPath(TypedDict):
  origin: Optional[str]
  path: str

class PublicDirectoryPath(TypedDict):
  """Represents a public directory path with optional origin specification.
  
  Format: <FOLDER-PATH>:<ORIGIN> where ORIGIN is scheme:hostname:port
  """
  origin: Optional[str]  # Optional origin (e.g., "https://api.example.com:8080")
  path: str              # File system path to the public directory

class ResponseFixturesPath(TypedDict):
  """Represents a response fixtures file path with optional origin specification.
  
  Format: <FILE-PATH>:<ORIGIN> where ORIGIN is scheme:hostname:port
  """
  origin: Optional[str]  # Optional origin (e.g., "https://api.example.com:8080")
  path: str              # File system path to the response fixtures file

class OpenapiSpecificationPath(TypedDict):
  """Represents an OpenAPI specification path with optional origin specification.
  
  Format: <FILE-PATH>:<ORIGIN> where ORIGIN is scheme:hostname:port
  """
  origin: Optional[str]  # Optional origin (e.g., "https://api.example.com:8080")
  path: str              # File system path to the OpenAPI specification file

# str, or a zero-arg callable resolved just-in-time when a fixture uses scenario_names
ScenarioNameOption = Optional[Union[str, Callable[[], Optional[str]]]]

class MockOptions(TypedDict):
  """Options for mock service."""
  public_directory_path: str
  response_fixtures_path: str                        # Comma-separated list of paths, optionally with origin prefix
  scenario_key: Optional[str]                        # Active scenario key; used to match fixture scenario_keys
  scenario_name: ScenarioNameOption                  # Active scenario name (or lazy getter) for scenario_names