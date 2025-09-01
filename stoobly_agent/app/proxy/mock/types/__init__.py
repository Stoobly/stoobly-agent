from typing import TypedDict, Optional

class Route(TypedDict):
  path: str

class Fixtures(TypedDict):
  DELETE: Route
  GET: Route
  POST: Route
  PUT: Route

class PublicDirectoryPath(TypedDict):
  """Represents a public directory path with optional origin specification."""
  origin: Optional[str]  # Optional origin (e.g., "example.com")
  path: str              # File system path to the public directory

class MockOptions(TypedDict):
  """Options for mock service."""
  public_directory_path: str
  response_fixtures: dict                            # Response fixtures configuration