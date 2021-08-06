import os
import yaml
import pdb

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

from . import env_vars
from .logger import Logger

class Settings:
    LOG_ID = 'lib.settings'

    _instance = None
    _agent_url = ''
    _proxy_url = ''

    def __init__(self):
        if Settings._instance:
            raise RuntimeError('Call instance() instead')
        else:
            cwd = os.path.dirname(os.path.realpath(__file__))

            self.config_file_path = os.path.join(cwd, '..', 'config', 'settings.yml')

            self.__load_config()
            self.__observe_config()

    ### Statuses

    # Headless means the agent is packaged without the frontend and
    # supports configuration with environment variables or the yaml file.
    def is_headless(self):
        if os.environ.get(env_vars.AGENT_IS_HEADLESS):
            return True

        return False

    def is_debug(self):
        return os.environ.get(env_vars.LOG_LEVEL) == 'debug'

    ### CRUD

    def to_hash(self):
        return self.config

    def update(self, contents):
        fp = open(self.config_file_path, 'w')
        yaml.dump(contents, fp, allow_unicode=True)
        fp.close()

    def reload_config(self):
        Logger.instance().info(f"{self.LOG_ID}.reload_config")
        self.__load_config()

    ### Properties

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()

        return cls._instance

    @property
    def agent_url(self):
        return self._agent_url

    @agent_url.setter
    def agent_url(self, value):
        self._agent_url = value

    @property
    def proxy_url(self):
        return self._proxy_url

    @proxy_url.setter
    def proxy_url(self, value):
        self._proxy_url = value

    @property
    def api_url(self):
        if self.is_headless() and os.environ.get(env_vars.API_URL):
            return os.environ[env_vars.API_URL]

        return self.config.get('api_url')

    @property
    def api_key(self):
        if self.is_headless() and os.environ.get(env_vars.API_KEY):
            return os.environ[env_vars.API_KEY]

        return self.config.get('api_key')

    @property
    def mode(self):
        return self.config.get('mode')

    @property
    def active_mode(self):
        mode = self.mode

        if not mode:
            return None
        else:
            if self.is_headless() and os.environ.get(env_vars.AGENT_ACTIVE_MODE):
                return os.environ[env_vars.AGENT_ACTIVE_MODE]

            return mode.get('active')

    # Get active mode settings first from environment variables
    # If the env var is null, get the setting from the yaml file
    @property
    def active_mode_settings(self):
        mode = self.mode

        if not mode:
            return None

        active_mode = self.active_mode

        if not active_mode:
            return None

        if self.is_headless():
            # Get settings from yaml file, replace setting with env var if set
            active_mode_settings = mode.get(active_mode)

            enabled = os.environ.get(env_vars.AGENT_ENABLED)
            if enabled != None:
                active_mode_settings['enabled'] = not not enabled

            include_patterns = os.environ.get(env_vars.AGENT_INCLUDE_PATTERNS)
            if include_patterns != None:
                # Split the string based on commas, strip whitespace
                active_mode_settings['include_patterns'] = list(map(str.strip, include_patterns.split(',')))

            exclude_patterns = os.environ.get(env_vars.AGENT_EXCLUDE_PATTERNS)
            if exclude_patterns != None:
                # Split the string based on commas, strip whitespace
                active_mode_settings['exclude_patterns'] = list(map(str.strip, exclude_patterns.split(',')))

            policy = os.environ.get(env_vars.AGENT_POLICY)
            if policy != None:
                active_mode_settings['policy'] = policy

            proxy_service_url = os.environ.get(env_vars.AGENT_SERVICE_URL)
            if proxy_service_url != None:
                active_mode_settings['service_url'] = proxy_service_url

            proxy_project_key = os.environ.get(env_vars.AGENT_PROJECT_KEY)
            if proxy_project_key != None:
                active_mode_settings['project_key'] = proxy_project_key

            proxy_scenario_key = os.environ.get(env_vars.AGENT_SCENARIO_KEY)
            if proxy_scenario_key != None:
                active_mode_settings['scenario_key'] = proxy_scenario_key

            return active_mode_settings

        return mode.get(active_mode)

    ### Helpers

    def __load_config(self):
        with open(self.config_file_path, 'r') as stream:
            try:
                self.config = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                pass

    def __observe_config(self):
        patterns = ['settings.yml']
        ignore_patterns = None
        ignore_directories = False
        case_sensitive = True
        event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)

        event_handler.on_modified = self.reload_config

        observer = Observer()
        watch_dir = os.path.dirname(self.config_file_path)
        observer.schedule(event_handler, watch_dir)
        observer.start()
