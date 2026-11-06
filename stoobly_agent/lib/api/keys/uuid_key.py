import uuid

from .resource_key import ResourceKey

DELIMITTER = '.'

class UuidKey(ResourceKey):
  def __init__(self, key: str):
    super().__init__(super().encode(self.__decode(key)))

  @staticmethod
  def encode(d: dict):
    toks = []
    for key in d:
      toks.append(f"{key}{d[key]}")

    return DELIMITTER.join(toks)

  @property
  def id(self) -> str:
    try:
      u = uuid.UUID(self.get('i'))
    except (TypeError, ValueError):
      return ''
    return str(u)

  def __decode(self, key: str):
    d = {}

    if not isinstance(key, str) or not key:
      return d

    for tok in key.split(DELIMITTER):
      # Skip empty tokens from malformed keys like "abc." or "p1..i2"
      if not tok:
        continue
      d[tok[0]] = tok[1:]

    return d