import os

import pytest

from stoobly_agent.app.settings import Settings
from stoobly_agent.config.constants import env_vars
from stoobly_agent.config.data_dir import DATA_DIR_NAME


class TestSettingsWatchWhenDataDirIsMissing:

    @pytest.fixture(autouse=True)
    def isolate_env(self, monkeypatch):
        monkeypatch.delenv(env_vars.AGENT_SETTINGS_PATH, raising=False)

    def test_watch_creates_missing_settings_directory(self, tmp_path):
        # Instances are cached per path, so the global caches are left alone to avoid leaking into other tests
        context_dir_path = os.path.join(str(tmp_path), 'watched-context')
        settings = Settings.instance(context_dir_path)

        assert settings.watch() is True
        assert os.path.isdir(os.path.join(context_dir_path, DATA_DIR_NAME))
