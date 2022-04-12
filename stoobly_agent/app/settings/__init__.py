import json
import os
import time
import yaml
import pdb

from shutil import copyfile
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from yamale import *

from stoobly_agent.config.constants import env_vars
from stoobly_agent.config.data_dir import DataDir
from stoobly_agent.config.source_dir import SourceDir
from stoobly_agent.lib.logger import Logger

#from .helpers.active_mode_settings_builder import ActiveModeSettingsBuilder
from .cli_settings import CLISettings
from .proxy_settings import ProxySettings
from .remote_settings import RemoteSettings
from .ui_settings import UISettings
from .types import IProjectModeSettings

class Settings:
    LOG_ID = 'app.settings'

    __instance = None

    __cli_settings = None
    __proxy_settings = None
    __remote_settings = None
    __ui_settings = None

    __settings_file_path = None
    __schema_file_path = None

    def __init__(self, **kwargs):
        if Settings.__instance:
            raise RuntimeError('Call instance() instead')

        self.__settings_file_path = DataDir.instance().settings_file_path
        self.__schema_file_path = SourceDir.instance().schema_file_path

        # If the config does not exist, use template
        if not os.path.exists(self.__settings_file_path):
            self.reset()

        if kwargs.get('validate'):
            self.__validate()
        
        self.__load_settings()

    @classmethod
    def instance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

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
    def proxy(self):
        return self.__proxy_settings

    @property
    def remote(self):
        return self.__remote_settings

    # Get active mode settings first from environment variables
    # If the env var is null, get the setting from the yaml file
    @property
    def active_mode_settings(self) -> IProjectModeSettings:
        if self.cli.remote_enabled:
            active_mode_settings = self.__build_active_mode_settings()

            if self.ui.active:
                self.__override_settings_with_env(active_mode_settings)
                self.__override_project_settings_with_env(active_mode_settings)

            return active_mode_settings
        else:
            return ActiveModeSettingsBuilder(self.proxy.intercept.active).with_enabled(True).build()

    def watch(self):
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

    ### Get

    def to_dict(self):
        if not self.__settings:
            self.__load_settings()
        return self.__settings

    ### Set

    def reset(self):
        copyfile(SourceDir.instance().settings_template_file_path, self.__settings_file_path)

    def write(self, contents):
        fp = open(self.__settings_file_path, 'w')
        yaml.dump(contents, fp, allow_unicode=True)
        fp.close()

    def commit(self):
        self.write(self.to_dict())

    ### Helpers

    #
    # Return active project's settings
    # If a scenario is set, return scenario settings
    #
    def __build_active_mode_settings(self) -> IProjectModeSettings:
        mode = self.mode

        if not mode:
            return {}

        active_mode = self.proxy.intercept.active

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


    def __load_settings(self):
        with open(self.__settings_file_path, 'r') as stream:
            try:
                settings = yaml.safe_load(stream)
                self.__settings = settings
                if settings:
                    self.__cli_settings = CLISettings(settings.get('cli'))
                    self.__proxy_settings = ProxySettings(settings.get('proxy'))
                    self.__remote_settings = RemoteSettings(settings.get('remote'))
                    self.__ui_settings = UISettings(settings.get('ui'))
            except yaml.YAMLError as exc:
                Logger.instance().error(exc)

    def __reload_settings(self, event):
        Logger.instance().info(f"{self.LOG_ID}.reload_settings")
        self.__load_settings()

    def __validate(self):
        try:
            schema = yamale.make_schema(self.__schema_file_path)
            data = yamale.make_data(self.__settings_file_path)
            yamale.validate(schema, data)
        except YamaleError as e:
            for result in e.results:
                print(f"{result}\n")
