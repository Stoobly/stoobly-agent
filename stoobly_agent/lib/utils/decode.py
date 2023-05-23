import json

from typing import Union

def decode(data: Union[bytes, str], encoding = None) -> str:
  if isinstance(data, bytes):
    try:
      encoding = encoding if encoding else json.detect_encoding(data)
      return data.decode(encoding)
    except Exception:
      return data.decode('ISO-8859-1')
  else:
    return data