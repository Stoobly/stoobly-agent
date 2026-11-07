import os

from stoobly_agent.config.data_dir import DATA_DIR_NAME, DataDir

# TODO: Move use scaffold constants after it is refactored to config/constants
SERVICES_CONFIG_FILE_PATH = os.path.join('services', '.config.yml')

class AppDataDir:
    """Resolves the scaffold app data dir (a .stoobly with services/.config.yml)."""

    _instance = None

    def __init__(self):
        raise RuntimeError('Call instance() instead')

    @classmethod
    def instance(cls, path: str = None) -> DataDir:
        data_dir_path = cls.find_data_dir(path or os.getcwd())
        cls._instance = DataDir.instance(os.path.dirname(data_dir_path))

        return cls._instance

    # If the current working directory does not contain a .stoobly/services/.config.yml,
    # then search in the parent directories until the filesystem root.
    @classmethod
    def find_data_dir(cls, start_path: str) -> str:
        root_dir = os.path.abspath(os.sep)
        start_path = os.path.abspath(start_path)

        while True:
            data_dir_path = os.path.join(start_path, DATA_DIR_NAME)
            services_config_path = os.path.join(data_dir_path, SERVICES_CONFIG_FILE_PATH)

            if (
                os.path.exists(data_dir_path)
                and os.stat(data_dir_path).st_uid == os.getuid()
                and os.path.exists(services_config_path)
            ):
                return data_dir_path

            # Root reached
            if start_path == root_dir:
                break

            # Move up one directory
            start_path = os.path.dirname(start_path)

        return os.path.join(os.path.expanduser('~'), DATA_DIR_NAME)
