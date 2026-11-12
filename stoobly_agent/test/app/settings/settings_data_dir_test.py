import os

import pytest

from stoobly_agent.app.settings import Settings
from stoobly_agent.config.constants import env_vars
from stoobly_agent.config.data_dir import DATA_DIR_NAME


class TestSettingsWhenFileIsMissing:
    """Reading settings must not write settings.yml. Defaults come from the template in memory,
    and the file is only written when settings are changed."""

    @pytest.fixture(autouse=True)
    def isolate_env(self, monkeypatch):
        # Instances are cached per path, so a fresh tmp path does not need the global caches cleared
        monkeypatch.delenv(env_vars.AGENT_SETTINGS_PATH, raising=False)

    def test_does_not_create_settings_file_on_read(self, tmp_path):
        context_dir_path = os.path.join(str(tmp_path), 'read-only-context')

        Settings.instance(context_dir_path)

        assert not os.path.exists(os.path.join(context_dir_path, DATA_DIR_NAME, 'settings.yml'))

    def test_reset_writes_gitignore_for_new_data_dir(self, tmp_path):
        context_dir_path = os.path.join(str(tmp_path), 'reset-context')

        Settings.instance(context_dir_path).reset()

        assert os.path.exists(os.path.join(context_dir_path, DATA_DIR_NAME, '.gitignore'))

    def test_write_on_new_data_dir_writes_gitignore(self, tmp_path):
        context_dir_path = os.path.join(str(tmp_path), 'write-context')

        Settings.instance(context_dir_path).write({'version': 1})

        assert os.path.exists(os.path.join(context_dir_path, DATA_DIR_NAME, '.gitignore'))

    def test_reset_with_settings_path_override_does_not_write_gitignore_outside_data_dir(self, tmp_path, monkeypatch):
        override_dir_path = os.path.join(str(tmp_path), 'user-config')
        monkeypatch.setenv(env_vars.AGENT_SETTINGS_PATH, os.path.join(override_dir_path, 'settings.yml'))
        context_dir_path = os.path.join(str(tmp_path), 'override-context')

        Settings.instance(context_dir_path).reset()

        assert not os.path.exists(os.path.join(override_dir_path, '.gitignore'))

    def test_loads_template_defaults_when_file_is_missing(self, tmp_path):
        context_dir_path = os.path.join(str(tmp_path), 'defaults-context')

        settings = Settings.instance(context_dir_path)

        assert settings.to_dict()['proxy']['intercept']['mode'] == 'record'
