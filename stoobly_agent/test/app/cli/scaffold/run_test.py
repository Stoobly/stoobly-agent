import os
import pytest
from unittest.mock import Mock, MagicMock, patch

from stoobly_agent.app.cli.scaffold.run import iter_commands, run_options
from stoobly_agent.app.cli.scaffold.app_config import AppConfig


class TestIterCommands:
    """Test iter_commands function"""

    @pytest.fixture
    def mock_app(self):
        """Create a mock App instance"""
        mock_app = Mock()
        mock_app.app_dir_path = '/app'
        return mock_app

    @pytest.fixture
    def mock_command(self, mock_app):
        """Create a mock WorkflowRunCommand instance"""
        mock_command = Mock()
        mock_command.app = mock_app
        mock_command.service_config = Mock()
        mock_command.service_config.hostname = 'localhost'
        mock_command.service_config.port = 3000
        mock_command.service_config.scheme = 'http'
        mock_command.service_config.upstream_hostname = 'localhost'
        mock_command.service_config.upstream_port = 3000
        mock_command.service_config.upstream_scheme = 'http'
        mock_command.service_config.url = 'http://localhost:3000'
        mock_command.public_dir_path = '/app/public'
        mock_command.response_fixtures_path = '/app/fixtures'
        mock_command.openapi_specification_path = '/app/openapi.yaml'
        mock_command.lifecycle_hooks_path = '/app/hooks.sh'
        mock_command.normalize_path = Mock(side_effect=lambda x: x)
        return mock_command

    def test_iter_commands_empty_list(self):
        """Test iter_commands with empty command list"""
        called_before_entrypoint = False
        called_command = False

        def handle_before_entrypoint(*args):
            nonlocal called_before_entrypoint
            called_before_entrypoint = True

        def handle_command(*args):
            nonlocal called_command
            called_command = True

        iter_commands([], handle_before_entrypoint, handle_command)

        assert not called_before_entrypoint
        assert not called_command

    def test_iter_commands_single_command(self, mock_command):
        """Test iter_commands with single command"""
        called_before_entrypoint = False
        called_command_count = 0

        def handle_command(cmd):
            nonlocal called_command_count
            called_command_count += 1

        iter_commands([mock_command], handle_command=handle_command)

        # Single command is both first and second-to-last, but before_entrypoint requires >= 2 commands
        assert called_command_count == 1

    def test_iter_commands_multiple_commands(self, mock_command, mock_app):
        """Test iter_commands with multiple commands"""
        mock_command2 = Mock()
        mock_command2.app = mock_app
        mock_command2.service_config = Mock()
        mock_command2.service_config.hostname = 'api'
        mock_command2.service_config.port = 8000
        mock_command2.service_config.scheme = 'https'
        mock_command2.service_config.upstream_hostname = 'api'
        mock_command2.service_config.upstream_port = 8000
        mock_command2.service_config.upstream_scheme = 'https'

        called_before_entrypoint = False
        called_commands = []

        def handle_before_entrypoint(*args):
            nonlocal called_before_entrypoint
            called_before_entrypoint = True

        def handle_command(cmd):
            called_commands.append(cmd)

        iter_commands(
            [mock_command, mock_command2],
            handle_before_entrypoint,
            handle_command
        )

        assert called_before_entrypoint
        assert len(called_commands) == 2

    def test_iter_commands_before_entrypoint_receives_correct_paths(self, mock_command, mock_app, tmp_path):
        """Test handle_before_entrypoint receives correct path information"""
        # Create actual temporary directories
        public_dir = tmp_path / 'public'
        fixtures_dir = tmp_path / 'fixtures'
        openapi_file = tmp_path / 'openapi.yaml'
        hooks_file = tmp_path / 'hooks.sh'

        public_dir.mkdir()
        fixtures_dir.mkdir()
        openapi_file.touch()
        hooks_file.touch()

        mock_command.public_dir_path = str(public_dir)
        mock_command.response_fixtures_path = str(fixtures_dir)
        mock_command.openapi_specification_path = str(openapi_file)
        mock_command.lifecycle_hooks_path = str(hooks_file)
        mock_command.service_config.url = 'http://localhost:3000'

        received_args = []

        def handle_before_entrypoint(*args):
            received_args.extend(args)

        mock_command2 = Mock()
        mock_command2.app = mock_app
        mock_command2.service_config = Mock()
        mock_command2.service_config.hostname = 'localhost'
        mock_command2.service_config.upstream_hostname = 'localhost'

        iter_commands(
            [mock_command, mock_command2],
            handle_before_entrypoint,
            None
        )

        assert len(received_args) == 5
        lifecycle_hooks_paths, openapi_spec_paths, proxy_upstreams, public_dirs, fixtures = received_args
        
        assert '--lifecycle-hooks-path' in lifecycle_hooks_paths
        assert '--openapi-specification-path' in openapi_spec_paths
        assert '--public-dir-path' in public_dirs
        assert '--response-fixtures-path' in fixtures

    def test_iter_commands_proxy_regular_upstream_added_on_hostname_mismatch(self, mock_app):
        """Test proxy_regular_upstream is added when hostnames differ"""
        received_args = []

        def handle_before_entrypoint(*args):
            received_args.extend(args)

        mock_command = Mock()
        mock_command.app = mock_app
        mock_command.service_config = Mock()
        mock_command.service_config.hostname = 'frontend'
        mock_command.service_config.port = 3000
        mock_command.service_config.scheme = 'http'
        mock_command.service_config.upstream_hostname = 'backend'
        mock_command.service_config.upstream_port = 8080
        mock_command.service_config.upstream_scheme = 'http'
        mock_command.service_config.url = 'http://localhost:3000'
        mock_command.public_dir_path = '/nonexistent'
        mock_command.response_fixtures_path = '/nonexistent'
        mock_command.openapi_specification_path = None
        mock_command.lifecycle_hooks_path = '/nonexistent'

        mock_command2 = Mock()
        mock_command2.app = mock_app
        mock_command2.service_config = Mock()

        iter_commands([mock_command, mock_command2], handle_before_entrypoint, None)

        proxy_upstreams = received_args[2]
        assert '--proxy-regular-upstream' in proxy_upstreams
        assert 'frontend:3000=http://backend:8080' in proxy_upstreams

    def test_iter_commands_containerized_path_normalization(self, mock_app, tmp_path):
        """Test containerized mode normalizes paths correctly"""
        # Create temporary directories
        app_dir = tmp_path / 'app'
        app_dir.mkdir()
        public_dir = app_dir / 'public'
        public_dir.mkdir()

        mock_app.app_dir_path = str(app_dir)

        mock_command = Mock()
        mock_command.app = mock_app
        mock_command.public_dir_path = str(public_dir)
        mock_command.response_fixtures_path = '/nonexistent'
        mock_command.openapi_specification_path = None
        mock_command.lifecycle_hooks_path = '/nonexistent'
        mock_command.service_config.hostname = 'localhost'
        mock_command.service_config.upstream_hostname = 'localhost'
        mock_command.service_config.url = 'http://localhost:3000'
        mock_command.normalize_path = Mock(side_effect=lambda x: x)

        received_args = []

        def handle_before_entrypoint(*args):
            received_args.extend(args)

        mock_command2 = Mock()
        mock_command2.app = mock_app
        mock_command2.service_config = Mock()

        iter_commands([mock_command, mock_command2], handle_before_entrypoint, None, containerized=True)

        public_dirs = received_args[3]
        assert '--public-dir-path' in public_dirs

    def test_iter_commands_skips_nonexistent_paths(self, mock_app):
        """Test iter_commands skips nonexistent file paths"""
        received_args = []

        def handle_before_entrypoint(*args):
            received_args.extend(args)

        mock_command = Mock()
        mock_command.app = mock_app
        mock_command.service_config = Mock()
        mock_command.service_config.hostname = 'localhost'
        mock_command.service_config.upstream_hostname = 'localhost'
        mock_command.service_config.url = 'http://localhost:3000'
        mock_command.public_dir_path = '/nonexistent/path'
        mock_command.response_fixtures_path = '/nonexistent/fixtures'
        mock_command.openapi_specification_path = '/nonexistent/openapi.yaml'
        mock_command.lifecycle_hooks_path = '/nonexistent/hooks.sh'

        mock_command2 = Mock()
        mock_command2.app = mock_app
        mock_command2.service_config = Mock()

        iter_commands([mock_command, mock_command2], handle_before_entrypoint, None)

        lifecycle_hooks, openapi_specs, proxy_upstreams, public_dirs, fixtures = received_args
        
        # All should be empty since paths don't exist
        assert len(lifecycle_hooks) == 0
        assert len(openapi_specs) == 0
        assert len(public_dirs) == 0
        assert len(fixtures) == 0


class TestRunOptions:
    """Test run_options function"""

    @pytest.fixture
    def mock_app_config(self):
        """Create a mock AppConfig instance"""
        mock_config = Mock(spec=AppConfig)
        mock_config.proxy_port = 8080
        mock_config.ui_port = 9090
        return mock_config

    def test_run_options_base_options(self, mock_app_config):
        """Test run_options returns base options"""
        options = run_options(mock_app_config)

        assert '--proxy-port' in options
        assert '8080' in options
        assert '--ui-port' in options
        assert '9090' in options
        assert '--request-log-enable' in options
        assert '--settings-watch' in options
        assert '--ssl-insecure' in options

    def test_run_options_with_log_level(self, mock_app_config):
        """Test run_options includes log level when provided"""
        options = run_options(mock_app_config, log_level='debug')

        assert '--log-level' in options
        assert 'debug' in options

    def test_run_options_without_log_level(self, mock_app_config):
        """Test run_options without log level"""
        options = run_options(mock_app_config)

        assert '--log-level' not in options

    def test_run_options_with_proxy_regular_upstreams(self, mock_app_config):
        """Test run_options includes proxy regular upstreams"""
        proxy_upstreams = ['--proxy-regular-upstream', 'frontend:3000=http://backend:8080']
        options = run_options(mock_app_config, proxy_regular_upstreams=proxy_upstreams)

        assert '--proxy-regular-upstream' in options
        assert 'frontend:3000=http://backend:8080' in options

    def test_run_options_with_public_directory_paths(self, mock_app_config):
        """Test run_options includes public directory paths"""
        public_dirs = ['--public-dir-path', './public:http://localhost:3000']
        options = run_options(mock_app_config, public_directory_paths=public_dirs)

        assert '--public-dir-path' in options
        assert './public:http://localhost:3000' in options

    def test_run_options_with_response_fixtures_paths(self, mock_app_config):
        """Test run_options includes response fixtures paths"""
        fixtures = ['--response-fixtures-path', './fixtures:http://localhost:3000']
        options = run_options(mock_app_config, response_fixtures_paths=fixtures)

        assert '--response-fixtures-path' in options
        assert './fixtures:http://localhost:3000' in options

    def test_run_options_with_openapi_specification_paths(self, mock_app_config):
        """Test run_options includes openapi specification paths"""
        openapi_specs = ['--openapi-specification-path', './openapi.yaml:http://localhost:3000']
        options = run_options(mock_app_config, openapi_specification_paths=openapi_specs)

        assert '--openapi-specification-path' in options
        assert './openapi.yaml:http://localhost:3000' in options

    def test_run_options_with_lifecycle_hooks_paths(self, mock_app_config):
        """Test run_options includes lifecycle hooks paths"""
        hooks = ['--lifecycle-hooks-path', './hooks.sh:http://localhost:3000']
        options = run_options(mock_app_config, lifecycle_hooks_paths=hooks)

        assert '--lifecycle-hooks-path' in options
        assert './hooks.sh:http://localhost:3000' in options

    def test_run_options_with_all_extra_options(self, mock_app_config):
        """Test run_options with all extra options combined"""
        options = run_options(
            mock_app_config,
            log_level='info',
            proxy_regular_upstreams=['--proxy-regular-upstream', 'host:port=http://upstream:port'],
            public_directory_paths=['--public-dir-path', './public:http://localhost:3000'],
            response_fixtures_paths=['--response-fixtures-path', './fixtures:http://localhost:3000'],
            openapi_specification_paths=['--openapi-specification-path', './openapi.yaml:http://localhost:3000'],
            lifecycle_hooks_paths=['--lifecycle-hooks-path', './hooks.sh:http://localhost:3000']
        )

        # Base options
        assert '--proxy-port' in options
        assert '--ui-port' in options
        assert '--request-log-enable' in options
        assert '--settings-watch' in options
        assert '--ssl-insecure' in options

        # Log level
        assert '--log-level' in options
        assert 'info' in options

        # Extra options
        assert '--proxy-regular-upstream' in options
        assert '--public-dir-path' in options
        assert '--response-fixtures-path' in options
        assert '--openapi-specification-path' in options
        assert '--lifecycle-hooks-path' in options

    def test_run_options_order(self, mock_app_config):
        """Test run_options maintains consistent ordering"""
        options1 = run_options(mock_app_config, log_level='debug')
        options2 = run_options(mock_app_config, log_level='debug')

        assert options1 == options2

    def test_run_options_returns_list(self, mock_app_config):
        """Test run_options returns a list"""
        options = run_options(mock_app_config)

        assert isinstance(options, list)

    def test_run_options_empty_extra_options(self, mock_app_config):
        """Test run_options with empty extra_options dict"""
        options = run_options(mock_app_config, **{})

        # Should contain only base options
        assert len(options) >= 8  # Base options count

    def test_run_options_with_none_extra_options(self, mock_app_config):
        """Test run_options handles None values in extra_options"""
        options = run_options(
            mock_app_config,
            log_level=None,
            proxy_regular_upstreams=None,
            public_directory_paths=None
        )

        # Should contain only base options
        assert '--log-level' not in options
        assert '--proxy-regular-upstream' not in options
        assert '--public-dir-path' not in options
