import os

class RootDir:
    HOME_DIR = os.path.expanduser('~')
    DIR_NAME = '.stoobly'

    _instance = None

    def __init__(self):
        if RootDir._instance:
            raise RuntimeError('Call instance() instead')
        else:
            self.root_dir = os.path.join(self.HOME_DIR, self.DIR_NAME)
            if not os.path.exists(self.root_dir):
                os.mkdir(self.root_dir)

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()

        return cls._instance

    @property
    def tmp_dir(self):
        return os.path.join(self.root_dir, 'tmp')

