import base64
import json

class ResourceKey():

  def __init__(self, key):
    try:
        key = base64.b64decode(key)
    except:
        self.decoded_key = {}

        return

    # TODO: add specific error catching
    try:
        self.decoded_key: dict = json.loads(key)
    except:
        self.decoded_key = {}