from typing import TypedDict

class Route(TypedDict):
  path: str

class Fixtures(TypedDict):
  DELETE: Route
  GET: Route
  POST: Route
  PUT: Route
