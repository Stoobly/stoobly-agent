import json

from typing import Union

def decode(data: Union[bytes, str]) -> str:
  if isinstance(data, bytes):
    try:
      return data.decode(json.detect_encoding(data))
    except Exception:
      return data.decode('ISO-8859-1')
  else:
    return data