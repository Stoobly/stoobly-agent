from typing import TypedDict, Optional

class Route(TypedDict):
  path: str

class Fixtures(TypedDict):
  DELETE: Route
  GET: Route
  POST: Route
  PUT: Route

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

class MockOptions(TypedDict):
  """Options for mock service."""
  public_directory_path: str
  response_fixtures_path: str                        # Comma-separated list of paths, optionally with origin prefix