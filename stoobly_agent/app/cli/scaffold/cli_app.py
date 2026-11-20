"""Shared App construction and validation for scaffold CLI modules."""

import os
import sys

from stoobly_agent.app.cli.scaffold.app import App
from stoobly_agent.app.cli.scaffold.containerized_app import ContainerizedApp
from stoobly_agent.config.data_dir import DATA_DIR_NAME

# Only forward App constructor options. CLI kwargs often include unrelated names
# (e.g. setting rewrite --path) that collide with App(path=...).
_APP_KWARG_KEYS = (
  'app_dir_path',
  'ca_certs_dir_path',
  'certs_dir_path',
  'context_dir_path',
  'containerized',
  'dry_run',
  'scaffold_namespace',
  'skip_find_app_dir',
)


def app_from_kwargs(kwargs):
  app_kwargs = {key: kwargs[key] for key in _APP_KWARG_KEYS if key in kwargs}
  if app_kwargs.get('containerized'):
    return ContainerizedApp(**app_kwargs)
  return App(app_kwargs.get('app_dir_path'), **app_kwargs)


def validate_app(app: App, require_context: bool = True):
  """Validate that a scaffold app is usable.

  Args:
    app: Resolved App instance.
    require_context: When False, allow a missing context ``.stoobly`` if the
      scaffold app itself exists. Used by request-log commands whose paths live
      under APP_DIR and must work with ``--app-dir-path`` outside a Stoobly cwd.
  """
  try:
    app.valid
  except ValueError as e:
    if not require_context:
      context_missing = not os.path.exists(os.path.join(app.context_dir_path, DATA_DIR_NAME))
      if context_missing and os.path.exists(app.scaffold_namespace_path):
        return
    print(f"Error: {e}", file=sys.stderr)
    sys.exit(1)
