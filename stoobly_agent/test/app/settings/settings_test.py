import pytest

from stoobly_agent.test.test_helper import reset
from stoobly_agent.app.settings import Settings


@pytest.fixture(scope='class')
def settings():
    return reset()

class TestSettings:
  class TestFromDict:

      class TestWithPreserveExistingFalse:

          def test_replaces_all_settings(self, settings: Settings):
              """Test that from_dict with preserve_existing=False replaces all existing settings"""
              # Create new settings dict
              new_settings = {
                  'cli': {
                      'features': {
                          'remote': True
                      }
                  },
                  'proxy': {
                      'url': 'http://new-proxy-url.com'
                  },
                  'remote': {
                      'api_key': 'new-api-key',
                      'api_url': 'https://new-api-url.com',
                      'project_key': 'new-project-key'
                  },
                  'ui': {
                      'active': True,
                      'url': 'http://new-ui-url.com'
                  }
              }

              # Apply new settings
              settings.from_dict(new_settings, preserve_existing=False)

              # Verify all settings were replaced
              cli_dict = settings.cli.to_dict()
              assert cli_dict['features']['remote'] == True

              proxy_dict = settings.proxy.to_dict()
              assert proxy_dict['url'] == new_settings['proxy']['url']

              remote_dict = settings.remote.to_dict()
              assert remote_dict['api_key'] == new_settings['remote']['api_key']
              assert remote_dict['api_url'] == new_settings['remote']['api_url']
              assert remote_dict['project_key'] == new_settings['remote']['project_key']

              ui_dict = settings.ui.to_dict()
              assert ui_dict['active'] == new_settings['ui']['active']
              assert ui_dict['url'] == new_settings['ui']['url']

      class TestWithPreserveExistingTrue:

          def test_merges_settings(self, settings: Settings):
              """Test that from_dict with preserve_existing=True merges with existing settings"""
              # Set initial settings
              initial_settings = {
                  'cli': {
                      'features': {
                          'remote': False
                      }
                  },
                  'proxy': {
                      'url': 'http://initial-proxy-url.com'
                  },
                  'remote': {
                      'api_key': 'initial-api-key',
                      'api_url': 'https://initial-api-url.com',
                      'project_key': 'initial-project-key'
                  },
                  'ui': {
                      'active': False,
                      'url': 'http://initial-ui-url.com'
                  }
              }
              settings.from_dict(initial_settings, preserve_existing=False)

              # Create partial new settings to merge
              partial_new_settings = {
                  'cli': {
                      'features': {
                          'remote': True
                      }
                  },
                  'remote': {
                      'api_key': 'updated-api-key'
                  }
              }

              # Merge new settings
              settings.from_dict(partial_new_settings, preserve_existing=True)

              # Verify merged settings
              cli_dict = settings.cli.to_dict()
              assert cli_dict['features']['remote'] == True  # Updated

              proxy_dict = settings.proxy.to_dict()
              assert proxy_dict['url'] == 'http://initial-proxy-url.com'  # Preserved

              remote_dict = settings.remote.to_dict()
              assert remote_dict['api_key'] == 'updated-api-key'  # Updated
              assert remote_dict['api_url'] == 'https://initial-api-url.com'  # Preserved
              assert remote_dict['project_key'] == 'initial-project-key'  # Preserved

              ui_dict = settings.ui.to_dict()
              assert ui_dict['active'] == False  # Preserved
              assert ui_dict['url'] == 'http://initial-ui-url.com'  # Preserved

      class TestWithEmptyDict:

          def test_does_not_modify_settings(self, settings: Settings):
              """Test that from_dict with empty dict does not modify existing settings objects
              
              Note: Empty dict is falsy in Python, so the condition `if settings:` in from_dict
              evaluates to False, meaning the settings objects are not recreated.
              """
              # Set some initial settings first
              initial_settings = {
                  'cli': {
                      'features': {
                          'remote': True
                      }
                  },
                  'proxy': {
                      'url': 'http://some-url.com'
                  }
              }
              settings.from_dict(initial_settings, preserve_existing=False)

              # Store references to verify they're the same objects
              cli_before = settings.cli
              proxy_before = settings.proxy

              # Apply empty dict
              settings.from_dict({}, preserve_existing=False)

              # Verify settings objects remain unchanged (empty dict is falsy, so condition fails)
              cli_dict = settings.cli.to_dict()
              assert cli_dict['features']['remote'] == True  # Still has the value

              proxy_dict = settings.proxy.to_dict()
              assert proxy_dict['url'] == 'http://some-url.com'  # Still has the value

              # Verify same objects (not recreated)
              assert settings.cli is cli_before
              assert settings.proxy is proxy_before

      class TestWithNone:

          def test_does_not_create_settings(self, settings: Settings):
              """Test that from_dict with None does not create new settings objects"""
              # Get initial settings
              initial_cli_dict = settings.cli.to_dict()
              initial_proxy_dict = settings.proxy.to_dict()

              # Apply None
              settings.from_dict(None, preserve_existing=False)

              # Verify settings objects still exist (they should remain unchanged)
              # The method sets self.__settings = None but doesn't modify the settings objects
              # when settings is None/empty
              assert settings.cli is not None
              assert settings.proxy is not None

      class TestWithPartialSettings:

          def test_only_updates_provided_sections(self, settings: Settings):
              """Test that from_dict with partial settings only updates provided sections"""
              # Set initial settings
              initial_settings = {
                  'cli': {
                      'features': {
                          'remote': False
                      }
                  },
                  'proxy': {
                      'url': 'http://initial-proxy-url.com'
                  },
                  'remote': {
                      'api_key': 'initial-api-key',
                      'api_url': 'https://initial-api-url.com',
                      'project_key': 'initial-project-key'
                  },
                  'ui': {
                      'active': False,
                      'url': 'http://initial-ui-url.com'
                  }
              }
              settings.from_dict(initial_settings, preserve_existing=False)

              # Apply only CLI settings
              partial_settings = {
                  'cli': {
                      'features': {
                          'remote': True
                      }
                  }
              }
              settings.from_dict(partial_settings, preserve_existing=False)

              # Verify only CLI was updated
              cli_dict = settings.cli.to_dict()
              assert cli_dict['features']['remote'] == True

              # Verify other settings are empty/default (since preserve_existing=False)
              proxy_dict = settings.proxy.to_dict()
              remote_dict = settings.remote.to_dict()
              ui_dict = settings.ui.to_dict()

              # These should be empty/default since they weren't provided
              assert 'url' not in proxy_dict or proxy_dict['url'] == ''
              assert remote_dict.get('api_key') == '' or remote_dict.get('api_key') is None
              assert ui_dict.get('active') == False or ui_dict.get('active') is None

      class TestWithMissingSections:

          def test_uses_empty_dicts(self, settings: Settings):
              """Test that from_dict with missing sections uses empty dicts for those sections"""
              # Set initial settings
              initial_settings = {
                  'cli': {
                      'features': {
                          'remote': True
                      }
                  },
                  'proxy': {
                      'url': 'http://initial-proxy-url.com'
                  }
              }
              settings.from_dict(initial_settings, preserve_existing=False)

              # Apply settings with only some sections
              partial_settings = {
                  'remote': {
                      'api_key': 'new-api-key'
                  }
              }
              settings.from_dict(partial_settings, preserve_existing=False)

              # Verify that missing sections use empty dicts
              # CLI and proxy should be empty/default since they weren't provided
              cli_dict = settings.cli.to_dict()
              # Should have default structure even if empty
              assert 'features' in cli_dict

              proxy_dict = settings.proxy.to_dict()
              # URL should be empty since it wasn't provided
              assert 'url' not in proxy_dict or proxy_dict['url'] == ''

              # Remote should have the new value
              remote_dict = settings.remote.to_dict()
              assert remote_dict['api_key'] == 'new-api-key'
