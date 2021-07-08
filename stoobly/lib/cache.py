class Cache:
    _instance = None

    def __init__(self):
        if self._instance:
            raise RuntimeError('Call instance() instead')
        else:
            self.data = {}


    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()

        return cls._instance

    def read(self, key):
        return self.data.get(key)

    def write(self, key, val):
        self.data[key] = val

    def delete(self, key):
        del self.data[key]
