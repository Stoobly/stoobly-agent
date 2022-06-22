import os
import pdb

class MitmproxyDir:
    MITMPROXY_DIR_NAME = '.mitmproxy'

    _instance = None

    def __init__(self):
        if MitmproxyDir._instance:
            raise RuntimeError('Call instance() instead')
        else:
            self.__mitmproxy_dir_path = os.path.join(os.path.expanduser('~'), self.MITMPROXY_DIR_NAME)

            if not os.path.exists(self.__mitmproxy_dir_path):
                os.mkdir(self.__mitmproxy_dir_path)

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()

        return cls._instance

    @property
    def ca_cert_pem_path(self):
        path = os.path.join(self.__mitmproxy_dir_path, 'mitmproxy_ca_cert.pem')

        if not os.path.exists(path):
            return ''

        return path