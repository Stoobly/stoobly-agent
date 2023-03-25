import pdb
import random

class Cache:
    _instance = None

    def __init__(self):
        if self._instance:
            raise RuntimeError('Call instance() instead')
        else:
            self.data = {}
            self.dataVersions = {}
            self.startVersion = random.randint(1, 1000000)
            self.version = self.startVersion

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()

        return cls._instance

    def clear(self):
        self.data = {}
        self.dataVersions = {}
        self.version += 1

    def read(self, key):
        data = self.data.get(key)

        if data == None:
            return None

        return {
            'name': key,
            'value': data,
            'version': self.dataVersions[key],
        }

    def read_all(self):
        data = []

        for key in self.data.keys():
            datum = self.read(key)
            if datum:
                data.append(datum)

        return data

    def write(self, key, val):
        self.data[key] = val

        if key not in self.dataVersions:
            self.dataVersions[key] = self.startVersion

        self.dataVersions[key] += 1
        self.version += 1

    def delete(self, key):
        del self.data[key]
        del self.dataVersions[key]
        self.version += 1
