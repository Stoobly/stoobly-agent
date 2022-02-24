import json
import os
import yaml
import pdb

from shutil import copyfile
from typing import List, Optional, TypedDict, Union
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from yamale import *

from .constants import env_vars
from .logger import Logger
from .root_dir import RootDir

class Rewrite:
    name: Optional[str]
    type: str
    value: str

class FilterRule(TypedDict):
    filters: List[Rewrite]
    method: str
    pattern: str

class RewriteRule(TypedDict):
    rewrites: List[Rewrite]
    method: str
    pattern: str

class IProjectRecordSettings(TypedDict):
    enabled: bool
    exclude_patterns: list
    filter_rules: list
    include_patterns: list
    policy: str
    project_key: str
    service_url: str
    scenario_key: str

class IProjectMockSettings(TypedDict):
    enabled: bool
    exclude_patterns: list
    include_patterns: list
    policy: str
    project_key: str
    service_url: str
    scenario_key: str

class IProjectTestSettings(TypedDict):
    exclude_patterns: list
    include_patterns: list
    policy: str
    project_key: str
    rewrite_rules: list
    service_url: str
    scenario_key: str
    test_strategy: str
    enabled: bool

class IRecordSettings(TypedDict):
    enabled: bool
    project_key: str
    settings: dict

class IMockSettings(TypedDict):
    enabled: bool
    project_key: str
    settings: dict

class ITestSettings(TypedDict):
    enabled: bool
    project_key: str
    settings: dict

class ISettingsMode(TypedDict):
    active: str
    record: IRecordSettings
    mock: IMockSettings
    test: ITestSettings

class ISettings(TypedDict):
    agent_url: str
    api_url: str
    api_key: str
    mode: ISettingsMode
    proxy_config_path: str

Component = {
    'Header': 'Header',
    'BodyParam': 'Body Param',
    'QueryParam': 'Query Param',
}
IProjectModeSettings = Union[IProjectMockSettings, IProjectRecordSettings, IProjectTestSettings]
Rule = Union[FilterRule, RewriteRule]

class Settings:
    LOG_ID = 'lib.settings'
    FILE_NAME = 'settings.yml'
    SCHEMA_FILE_NAME = 'schema.yml'

    _instance = None
    _agent_url = ''
    _proxy_url = ''
    _api_url = ''

    def __init__(self):
        if Settings._instance:
            raise RuntimeError('Call instance() instead')
        else:
            cwd = os.path.dirname(os.path.realpath(__file__))
            config_dir = os.path.join(cwd, '..', 'config')

            self.config_file_path = os.path.join(RootDir.instance().root_dir, self.FILE_NAME)
            self.schema_file_path = os.path.join(config_dir, self.SCHEMA_FILE_NAME)

            # If the config does not exist, use template
            if not os.path.exists(self.config_file_path):
                self.config_template_file_path = os.path.join(config_dir, self.FILE_NAME)
                copyfile(self.config_template_file_path, self.config_file_path)

            self.__validate()
            self.__load_config()

    def observe_config(self):
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

    def reload_config(self, event):
        Logger.instance().info(f"{self.LOG_ID}.reload_config")
        self.__load_config()

    def to_json(self, pretty_print=False):
        output = None
        settings_dict = self.__dict__
        settings_dict['is_headless'] = self.is_headless()
        settings_dict['is_debug'] = self.is_debug()

        settings_dict['env_vars'] = {}
        environ_vars = settings_dict['env_vars']

        # https://stackoverflow.com/questions/11637293/iterate-over-object-attributes-in-python
        env_vars_fields = [a for a in dir(env_vars) if not a.startswith('__')]

        for env_var in env_vars_fields:
            environ_vars[env_var] = os.environ.get(env_vars.__dict__[env_var])

        if pretty_print:
            output = json.dumps(settings_dict, indent=4)
        else:
            output = json.dumps(settings_dict)

        return output

    ### Properties

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()

        return cls._instance

    @property
    def agent_url(self):
        if self._agent_url:
            return self._agent_url

        if os.environ.get(env_vars.AGENT_URL):
            return os.environ[env_vars.AGENT_URL]

        return self.config.get('agent_url')

    @agent_url.setter
    def agent_url(self, value):
        self._agent_url = value

    @property
    def proxy_url(self):
        if self._proxy_url:
            return self._proxy_url

        if os.environ.get(env_vars.AGENT_PROXY_URL):
            return os.environ[env_vars.AGENT_PROXY_URL]

        return self.config.get('proxy_url')

    @proxy_url.setter
    def proxy_url(self, value) -> None:
        self._proxy_url = value

    @property
    def api_url(self) -> str:
        if self._api_url:
            return self._api_url

        if os.environ.get(env_vars.API_URL):
            return os.environ[env_vars.API_URL]

        return self.config.get('api_url')

    @api_url.setter
    def api_url(self, value) -> None:
        self._api_url = value

    @property
    def api_key(self) -> str:
        if os.environ.get(env_vars.API_KEY):
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
            if os.environ.get(env_vars.AGENT_ACTIVE_MODE):
                return os.environ[env_vars.AGENT_ACTIVE_MODE]

            return mode.get('active')

    # Get active mode settings first from environment variables
    # If the env var is null, get the setting from the yaml file
    @property
    def active_mode_settings(self) -> IProjectModeSettings:
        active_mode_settings = self.__build_active_mode_settings()

        if self.is_headless():
            self.__override_settings_with_env(active_mode_settings)
            self.__override_project_settings_with_env(active_mode_settings)

        return active_mode_settings

    ### Helpers

    #
    # Return active project's settings
    # If a scenario is set, return scenario settings
    #
    def __build_active_mode_settings(self) -> IProjectModeSettings:
        mode = self.mode

        if not mode:
            return {}

        active_mode = self.active_mode

        if not active_mode:
            return {}

        active_mode_settings = mode.get(active_mode, {})
        all_project_settings = active_mode_settings.get('settings', {})

        project_key = active_mode_settings.get('project_key')
        project_settings = all_project_settings.get(project_key)

        if not project_settings:
            project_settings = {}
        else:
            scenario_key = project_settings.get('scenario_key')
            if scenario_key and len(scenario_key) != 0:
                project_settings = all_project_settings.get(scenario_key) or {}

                project_settings['scenario_key'] = scenario_key
            else:
                project_settings['scenario_key'] = ''

        # Merge higher level settings
        project_settings['project_key'] = project_key
        project_settings['enabled'] = active_mode_settings.get('enabled')

        return project_settings

    def __override_project_settings_with_env(self, active_mode_settings: IProjectModeSettings):
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

        proxy_scenario_key = os.environ.get(env_vars.AGENT_SCENARIO_KEY)
        if proxy_scenario_key != None:
            active_mode_settings['scenario_key'] = proxy_scenario_key

        proxy_service_url = os.environ.get(env_vars.AGENT_SERVICE_URL)
        if proxy_service_url != None:
            active_mode_settings['service_url'] = proxy_service_url

    ###
    #
    # Replace setting with env var if set
    #
    # @param active_mode_settings [Dict]
    #
    def __override_settings_with_env(self, active_mode_settings: IProjectModeSettings):
        enabled = os.environ.get(env_vars.AGENT_ENABLED)

        if enabled != None:
            active_mode_settings['enabled'] = not not enabled

        proxy_project_key = os.environ.get(env_vars.AGENT_PROJECT_KEY)
        if proxy_project_key != None:
            active_mode_settings['project_key'] = proxy_project_key


    def __load_config(self):
        with open(self.config_file_path, 'r') as stream:
            try:
                self.config = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                pass

    def __validate(self):
        try:
            schema = yamale.make_schema(self.schema_file_path)
            data = yamale.make_data(self.config_file_path)
            yamale.validate(schema, data)
        except YamaleError as e:
            for result in e.results:
                print(f"{result}\n")
