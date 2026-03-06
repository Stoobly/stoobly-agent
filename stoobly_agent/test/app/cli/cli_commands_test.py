import pytest
from click.testing import CliRunner

from stoobly_agent.cli import main


@pytest.fixture(scope='module')
def runner():
    return CliRunner()


class TestCliCommandsLoad:
    """Smoke tests to ensure all CLI commands load without errors."""

    COMMANDS = [
        [],  # root help
        ['ca-cert'],
        ['config'],
        ['endpoint'],
        ['feature'],
        ['intercept'],
        ['request'],
        ['scaffold'],
        ['scenario'],
        ['snapshot'],
    ]

    @pytest.mark.parametrize('command', COMMANDS)
    def test_command_loads(self, runner: CliRunner, command: list):
        """Test that running --help on a command doesn't show 'No such command'."""
        result = runner.invoke(main, command + ['--help'])

        assert 'No such command' not in result.output, (
            f"Command {' '.join(command) or 'root'} failed to load. "
            f"This usually indicates an import or other error in the CLI module.\n"
            f"Output: {result.output}"
        )
        assert result.exit_code == 0, (
            f"Command {' '.join(command) or 'root'} exited with code {result.exit_code}.\n"
            f"Output: {result.output}"
        )


class TestCliSubcommandsLoad:
    """Test that subcommands within groups load correctly."""

    SUBCOMMANDS = [
        ['endpoint', 'import'],
        ['request', 'list'],
        ['scaffold', 'app'],
        ['scaffold', 'app', 'create'],
        ['scaffold', 'app', 'mkcert'],
        ['scaffold', 'hostname'],
        ['scaffold', 'hostname', 'install'],
        ['scaffold', 'hostname', 'uninstall'],
        ['scaffold', 'service'],
        ['scaffold', 'service', 'create'],
        ['scaffold', 'service', 'delete'],
        ['scaffold', 'service', 'list'],
        ['scaffold', 'service', 'show'],
        ['scaffold', 'service', 'update'],
        ['scaffold', 'workflow'],
        ['scaffold', 'workflow', 'copy'],
        ['scaffold', 'workflow', 'create'],
        ['scaffold', 'workflow', 'down'],
        ['scaffold', 'workflow', 'logs'],
        ['scaffold', 'workflow', 'show'],
        ['scaffold', 'workflow', 'up'],
        ['scaffold', 'workflow', 'validate'],
        ['scenario', 'list'],
    ]

    @pytest.mark.parametrize('command', SUBCOMMANDS)
    def test_subcommand_loads(self, runner: CliRunner, command: list):
        """Test that subcommands load without 'No such command' errors."""
        result = runner.invoke(main, command + ['--help'])

        assert 'No such command' not in result.output, (
            f"Subcommand '{' '.join(command)}' failed to load.\n"
            f"Output: {result.output}"
        )
        assert result.exit_code == 0, (
            f"Subcommand '{' '.join(command)}' exited with code {result.exit_code}.\n"
            f"Output: {result.output}"
        )
