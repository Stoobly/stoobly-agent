import pdb
import os
import shutil

from stoobly_agent.config.constants.env_vars import ENV

CERTS_DIR_NAME = 'certs'
DATA_DIR_NAME = '.stoobly'
DB_FILE_NAME = 'stoobly_agent.sqlite3'
DB_VERSION_NAME = 'VERSION'
MITMPROXY_OPTIONS_FILE_NAME = 'options.json'
TMP_DIR_NAME = 'tmp'

class DataDir:

    _instances = None

    def __init__(self, path: str = None):
        if DataDir._instances.get(path):
            raise RuntimeError('Call instance() instead')
        else:
            self.__path = path

            if path:
                self.__data_dir_path = os.path.join(path, DATA_DIR_NAME)
            else:
                cwd = os.getcwd()
                self.__data_dir_path = self.find_data_dir(cwd)

            if not os.path.exists(self.__data_dir_path):
                self.create(os.path.dirname(self.__data_dir_path))

    def __repr__(self) -> str:
      return self.path

    @classmethod
    def instance(cls, path: str = None):
        if not cls._instances:
            cls._instances = {}

        if not cls._instances.get(path):
            cls._instances[path] = cls(path)

        return cls._instances[path]

    @classmethod
    def handle_chdir(cls):
        if cls._instances and None in cls._instances:
            del cls._instances[None]

        return cls.instance()

    @property
    def context_dir_path(self):
        return os.path.abspath(os.path.join(self.path, '..'))

    @property
    def path(self):
        return self.__data_dir_path

    @property
    def tmp_dir_path(self):
        tmp_dir_path = os.path.join(self.path, TMP_DIR_NAME)

        if not os.path.exists(tmp_dir_path):
            os.mkdir(tmp_dir_path)

        return tmp_dir_path

    @property
    def certs_dir_path(self):
        certs_dir_path = os.path.join(self.path, CERTS_DIR_NAME)

        if not os.path.exists(certs_dir_path):
            os.mkdir(certs_dir_path)

        return certs_dir_path

    @property
    def db_dir_path(self):
        db_dir_path = os.path.join(self.path, 'db')

        if not os.path.exists(db_dir_path):
            os.mkdir(db_dir_path)

        return db_dir_path

    @property
    def db_file_path(self):
        return os.path.join(self.db_dir_path, DB_FILE_NAME)

    @property
    def db_version_path(self):
        return os.path.join(self.db_dir_path, DB_VERSION_NAME)

    @property
    def mitmproxy_options_json_path(self):
        return os.path.join(self.tmp_dir_path, MITMPROXY_OPTIONS_FILE_NAME)

    @property
    def ca_certs_dir_path(self):
        path = os.path.join(self.path, 'ca_certs')

        if not os.path.exists(path):
            os.makedirs(path)

        return path

    @property
    def settings_file_path(self):
        return os.path.join(self.path, 'settings.yml')

    @property
    def snapshots_dir_path(self):
        snapshots_dir_path = os.path.join(self.path, 'snapshots')

        if not os.path.exists(snapshots_dir_path):
            os.mkdir(snapshots_dir_path)

        return snapshots_dir_path

    @property
    def snapshots_history_dir_path(self):
        snapshots_history_dir_path = os.path.join(self.snapshots_dir_path, 'history')

        if not os.path.exists(snapshots_history_dir_path):
            os.mkdir(snapshots_history_dir_path)

        return snapshots_history_dir_path

    @property
    def snapshots_log_file_path(self):
        snapshots_log_file_path = os.path.join(self.snapshots_dir_path, 'log')

        return snapshots_log_file_path

    @property
    def snapshots_requests_dir_path(self):
        base_path = self.snapshots_dir_path
        requests_dir_path = os.path.join(base_path, 'requests')

        if not os.path.exists(requests_dir_path):
            os.mkdir(requests_dir_path)

        return requests_dir_path

    @property
    def snapshots_scenarios_dir_path(self):
        base_path = self.snapshots_dir_path
        scenarios_dir_path = os.path.join(base_path, 'scenarios')

        if not os.path.exists(scenarios_dir_path):
            os.mkdir(scenarios_dir_path)

        return scenarios_dir_path

    @property
    def snapshots_scenario_requests_dir_path(self):
        base_path = self.snapshots_scenarios_dir_path
        requests_dir_path = os.path.join(base_path, 'requests')

        if not os.path.exists(requests_dir_path):
            os.mkdir(requests_dir_path)

        return requests_dir_path

    @property
    def snapshosts_version_path(self):
        return os.path.join(self.snapshots_dir_path, 'VERSION')

    def remove(self, directory_path = None):
        if directory_path:
            data_dir_path = os.path.join(directory_path, DATA_DIR_NAME)
        else:
            data_dir_path = self.path

        if os.path.exists(data_dir_path):
            shutil.rmtree(data_dir_path)

    def create(self, directory_path = None):
        if not directory_path:
            directory_path = os.getcwd()

        self.__data_dir_path = os.path.join(directory_path, DATA_DIR_NAME)

        if not os.path.exists(self.__data_dir_path):
            os.mkdir(self.__data_dir_path)

            # Create the certs_dir_path if it doesn't exist
            self.certs_dir_path
            # Create tmp folder
            os.makedirs(os.path.join(self.__data_dir_path, TMP_DIR_NAME), exist_ok=True)

            with open(os.path.join(self.__data_dir_path, '.gitignore'), 'w') as fp:
                fp.write(
                    "\n".join([
                        '.settings.yml.lock',
                        'ca_certs',
                        'certs',
                        'db',
                        'settings.yml',
                        os.path.join('snapshots', 'log'),
                        os.path.join('snapshots', 'VERSION'),
                        TMP_DIR_NAME
                    ])
                )

    # If the current working directory does not contain a .stoobly folder,
    # then search in the parent directories until the home directory.
    def find_data_dir(self, start_path: str) -> str:
        root_dir = os.path.abspath(os.sep)

        while True:
            data_dir_path = os.path.join(start_path, DATA_DIR_NAME)
            if os.path.exists(data_dir_path) and os.stat(data_dir_path).st_uid == os.getuid():
                return data_dir_path

            # Root reached
            if start_path == root_dir:
                break

            # Move up one directory
            start_path = os.path.dirname(start_path)

        return os.path.join(os.path.expanduser('~'), DATA_DIR_NAME)
