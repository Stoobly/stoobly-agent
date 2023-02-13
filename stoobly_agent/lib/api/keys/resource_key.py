import base64
import json

class ResourceKey():

    def __init__(self, key):
        self.__raw = key

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

    @property
    def raw(self):
        return self.__raw

    @staticmethod
    def encode(data: dict):
        return base64.b64encode(json.dumps({
            **data,
        }).encode())

    def get(self, k: str):
        v = self.decoded_key.get(k)
        return str(v) if v != None else None