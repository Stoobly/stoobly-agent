from typing import TypedDict

class ResponseHeader(TypedDict):
  name: str
  value: str
  
class ResponseHeaderShowResponse(ResponseHeader):
  id: str