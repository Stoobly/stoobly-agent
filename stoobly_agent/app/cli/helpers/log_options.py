import functools

import click

from stoobly_agent.app.cli.helpers.print_service import FORMATS

LOG_FILTER_KEYS = [
    # Filter keys only — display options (format, select, without_headers)
    # are intentionally excluded and handled directly by each CLI command.
    'level', 'message', 'method', 'scenario_key', 'scenario_name',
    'status_code', 'url', 'request_key', 'test_title',
]


def build_log_filters(kwargs: dict, extra_keys: list = None) -> dict:
    """Extract filter parameters from CLI kwargs.

    Args:
        kwargs: Full kwargs dict from a Click command.
        extra_keys: Additional filter keys beyond LOG_FILTER_KEYS (e.g. ['service_name']).

    Returns:
        Dict of non-None filter key/value pairs.
    """
    keys = LOG_FILTER_KEYS + (extra_keys or [])
    return {k: v for k, v in kwargs.items() if k in keys and v is not None}


def log_list_options(func):
    """Composite decorator: shared filter + print options for request log list commands."""
    decorators = [
        click.option('--follow', '-f', is_flag=True, default=False, help='Follow log output (like tail -f). Ctrl-C to stop.'),
        click.option('--format', type=click.Choice(FORMATS), help='Format output.'),
        click.option('--level', default=None,
            type=click.Choice(['DEBUG', 'INFO', 'WARNING', 'ERROR'], case_sensitive=False),
            help='Filter by log level.'),
        click.option('--message', default=None,
            help='Filter by log message (e.g., "Mock success", "Mock failure").'),
        click.option('--method', default=None,
            type=click.Choice(['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'HEAD', 'OPTIONS'],
                case_sensitive=False),
            help='Filter by HTTP method.'),
        click.option('--request-key', default=None, help='Filter by request key.'),
        click.option('--scenario-key', default=None, help='Filter by scenario key.'),
        click.option('--scenario-name', default=None, help='Filter by scenario name.'),
        click.option('--select', multiple=True, help='Select column(s) to display.'),
        click.option('--status-code', default=None, type=click.IntRange(min=100, max=599),
            help='Filter by HTTP status code.'),
        click.option('--test-title', default=None, help='Filter by test title.'),
        click.option('--url', default=None, help='Filter by URL (substring match).'),
        click.option('--without-headers', is_flag=True, default=False,
            help='Disable printing column headers.'),
    ]
    return functools.reduce(lambda f, d: d(f), reversed(decorators), func)
