import os
import pdb
import time
import yaml

from shutil import copyfile
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from yamale import *

from stoobly_agent.config.constants import env_vars, statuses
from stoobly_agent.config.data_dir import DataDir
from stoobly_agent.config.source_dir import SourceDir
from stoobly_agent.lib.logger import Logger

from .cli_settings import CLISettings
from .proxy_settings import ProxySettings
from .remote_settings import RemoteSettings
from .ui_settings import UISettings

LOG_ID = 'Settings'

class Settings:
    _instances = None

    __data_dir: DataDir = None

    __cli_settings = None
    __proxy_settings = None
    __remote_settings = None
    __ui_settings = None

    __settings_file_path = None
    __schema_file_path = None

    __load_lock = False
    __watching = False

    def __init__(self, data_dir_path: str = None):
        if Settings._instances.get(data_dir_path):
            raise RuntimeError('Call instance() instead')

        self.__data_dir = DataDir.instance(data_dir_path)
        self.__detect_paths()

        # If the config does not exist, use template
        if not os.path.exists(self.__settings_file_path):
            self.__create_default_file()

        self.__load_settings()

    @classmethod
    def instance(cls, data_dir_path: str = None):
        if not cls._instances:
            cls._instances = {}

        if not cls._instances.get(data_dir_path):
            cls._instances[data_dir_path] = cls(data_dir_path)

        return cls._instances[data_dir_path]

    @classmethod
    def handle_chdir(cls):
        '''
        Reloads data dir to be relative to new working directory
        '''
        DataDir.handle_chdir()

        if cls._instances and None in cls._instances:
            del cls._instances[None]

        return cls.instance()

    ### Statuses

    def is_debug(self):
        return os.environ.get(env_vars.LOG_LEVEL) == 'debug'

    ### Properties

    @property
    def cli(self):
        return self.__cli_settings

    @property
    def ui(self):
        return self.__ui_settings

    @property
    def path(self):
        return self.__settings_file_path

    @property
    def proxy(self):
        return self.__proxy_settings

    @property
    def remote(self):
        return self.__remote_settings

    def watch(self):
        if self.__watching:
            return False

        patterns = ['settings.yml']
        ignore_patterns = None
        ignore_directories = False
        case_sensitive = True
        event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)
        event_handler.on_modified = self.__reload_settings

        observer = Observer()
        watch_dir = os.path.dirname(self.__settings_file_path)

        observer.schedule(event_handler, watch_dir)
        observer.start()

        self.__watching = True

        return True

    ### Get

    def to_dict(self):
        if not self.__settings:
            self.__load_settings()

        return {
            **self.__settings,
            **{ 'cli': self.__cli_settings.to_dict() },
            **{ 'proxy': self.__proxy_settings.to_dict() },
            **{ 'remote': self.__remote_settings.to_dict() },
            **{ 'ui': self.__ui_settings.to_dict() },
        }

    def read(self):
        with open(self.__settings_file_path, 'r') as fp:
            return yaml.safe_load(fp)

    def validate(self):
        try:
            schema = yamale.make_schema(self.__schema_file_path)
            data = yamale.make_data(self.__settings_file_path)
            yamale.validate(schema, data)
        except YamaleError as e:
            for result in e.results:
                print(f"{result}\n")

    ### Set

    def commit(self):
        settings = self.to_dict()
        self.write(settings)

    def from_dict(self, settings):
        self.__settings = settings
        if settings:
            self.__cli_settings = CLISettings(settings.get('cli'))
            self.__proxy_settings = ProxySettings(settings.get('proxy'))
            self.__remote_settings = RemoteSettings(settings.get('remote'))
            self.__ui_settings = UISettings(settings.get('ui'))

    def load(self):
        self.__load_settings()

    def reset(self):
        self.__detect_paths()
        self.__create_default_file()

    def reset_and_load(self):
        self.reset()
        self.__load_settings()

    def write(self, contents):
        if contents:
            fp = open(self.__settings_file_path, 'w')
            yaml.dump(contents, fp, allow_unicode=True)
            fp.close()

    ### Helpers

    def __create_default_file(self):
        copyfile(SourceDir.instance().settings_template_file_path, self.__settings_file_path)

    def __detect_paths(self):
        self.__settings_file_path = os.environ.get(env_vars.AGENT_CONFIG_PATH) or self.__data_dir.settings_file_path
        self.__schema_file_path = SourceDir.instance().schema_file_path

    def __load_settings(self):
        with open(self.__settings_file_path, 'r') as stream:
            try:
                settings = yaml.safe_load(stream)
                if not settings:
                    time.sleep(1) # TODO: Sometimes it takes a bit to read, should look into this
                    settings = yaml.safe_load(stream)

                self.from_dict(settings)
            except yaml.YAMLError as exc:
                Logger.instance().error(exc)

    def __reload_settings(self, event):
        if not self.__load_lock:
            from stoobly_agent.app.proxy.utils.publish_change_service import publish_change

            self.__load_lock = True

            Logger.instance(LOG_ID).debug('Reloading settings')
            self.__load_settings()

            publish_change(statuses.SETTINGS_MODIFIED, self.__settings, sync=True)

        self.__load_lock = False
