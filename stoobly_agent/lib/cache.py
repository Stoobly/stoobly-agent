import pdb
import random
import re

from time import time

class Cache:
    _instance = None

    def __init__(self):
        if self._instance:
            raise RuntimeError('Call instance() instead')
        else:
            self.data = {}
            self.dataVersions = {}
            self.startVersion = random.randint(1, 1000000)
            self.timeouts = {}
            self.version = self.startVersion

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()

        return cls._instance

    def clear(self, pattern: str = None):
        if not pattern:
            self.data = {}
            self.dataVersions = {}
            self.version += 1
        else:
            delete_list = []
            for key in self.data.keys():
                if re.match(pattern, key):
                    delete_list.append(key)
            
            for key in delete_list:
                self.delete(key)

    def read(self, key):
        if key in self.timeouts:
            timeout = self.timeouts[key]
            if round(time() * 1000) > timeout:
                self.delete(key)
                return None

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
        
        for key in list(self.data.keys()):
            datum = self.read(key)

            if datum:
                data.append(datum)

        return data

    # timeout: milliseconds
    def write(self, key, val, timeout = None):
        if timeout and timeout <= 0:
            return

        self.data[key] = val

        if key not in self.dataVersions:
            self.dataVersions[key] = self.startVersion

        if timeout:
            self.timeouts[key] = round(time() * 1000) + timeout

        self.dataVersions[key] += 1
        self.version += 1

    def delete(self, key):
        if key in self.data:
            del self.data[key]

        if key in self.dataVersions:
            del self.dataVersions[key]

        if key in self.timeouts:
            del self.timeouts[key]

        self.version += 1
