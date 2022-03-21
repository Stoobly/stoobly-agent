import base64
import json
import pdb

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


    @staticmethod
    def encode(data):
        return base64.b64encode(json.dumps(data).encode())