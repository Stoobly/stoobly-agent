from typing import TypedDict

class Header(TypedDict):
  name: str
  value: str
  
class HeaderShowResponse(Header):
  id: str