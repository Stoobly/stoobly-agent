import base64
import json
import random
import time

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
    def encode(data: dict):
        return base64.b64encode(json.dumps({
            **data,
            't': random.randint(1000000, 10000000),
        }).encode())


    def get(self, k: str):
        v = self.decoded_key.get(k)
        return str(v) if v else None