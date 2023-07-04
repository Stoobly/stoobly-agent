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

  def __decode(self, key: str):
    toks = key.split(DELIMITTER)

    d = {}
    for tok in toks:
      d[tok[0]] = tok[1:]

    return d