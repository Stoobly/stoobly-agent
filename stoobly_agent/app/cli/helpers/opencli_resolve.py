"""Resolve packaged OpenCLI description files for CLI command groups.

Convention: add ``{group}.opencli.yaml`` under ``stoobly_agent/app/cli/``, then
register the group name in ``OPENCLI_GROUPS`` below. Optionally add a
Click-vs-OpenCLI interface test patterned on
``stoobly_agent/test/app/cli/scaffold/opencli_interface_test.py``.

The ``main`` group is the root ``stoobly-agent`` index. ``opencli show`` with no
argument defaults to it. ``main`` is omitted from ``opencli list`` (overview via
``show``, drill-down groups via ``list``).
"""

from importlib import resources
from pathlib import Path
from typing import Any, Dict, List

import yaml

MAIN_GROUP = 'main'

# Group name → filename under stoobly_agent.app.cli
OPENCLI_GROUPS: Dict[str, str] = {
  MAIN_GROUP: 'main.opencli.yaml',
  'endpoint': 'endpoint.opencli.yaml',
  'intercept': 'intercept.opencli.yaml',
  'request': 'request.opencli.yaml',
  'scaffold': 'scaffold.opencli.yaml',
  'scenario': 'scenario.opencli.yaml',
  'setting': 'setting.opencli.yaml',
  'snapshot': 'snapshot.opencli.yaml',
}

_PACKAGE = 'stoobly_agent.app.cli'


class OpencliResolveError(Exception):
  """Raised when an OpenCLI group cannot be resolved."""


def registered_groups() -> List[str]:
  """Return all registered OpenCLI group names including ``main`` (sorted, main first)."""
  others = sorted(name for name in OPENCLI_GROUPS if name != MAIN_GROUP)
  if MAIN_GROUP in OPENCLI_GROUPS:
    return [MAIN_GROUP] + others
  return others


def list_groups() -> List[str]:
  """Return OpenCLI groups shown by ``opencli list`` (excludes ``main``)."""
  return sorted(name for name in OPENCLI_GROUPS if name != MAIN_GROUP)


def resolve_path(group: str) -> Path:
  """Return the filesystem path to the OpenCLI YAML for ``group``.

  Raises:
    OpencliResolveError: Unknown group or missing packaged file.
  """
  if group not in OPENCLI_GROUPS:
    known = ', '.join(registered_groups()) or '(none)'
    raise OpencliResolveError(
      f"Unknown OpenCLI group {group!r}. Known groups: {known}"
    )

  filename = OPENCLI_GROUPS[group]
  resource = resources.files(_PACKAGE).joinpath(filename)
  if not resource.is_file():
    raise OpencliResolveError(
      f"OpenCLI description for group {group!r} is missing at {_PACKAGE}/{filename}"
    )

  return Path(str(resource))


def read_document(group: str = None) -> str:
  """Return the raw OpenCLI YAML text for ``group`` (defaults to ``main``)."""
  return resolve_path(group or MAIN_GROUP).read_text(encoding='utf-8')


def list_group_rows() -> List[Dict[str, Any]]:
  """Return table rows for listable OpenCLI groups (``name``, ``summary``)."""
  rows: List[Dict[str, Any]] = []
  for name in list_groups():
    data = yaml.safe_load(read_document(name)) or {}
    info = data.get('info') or {}
    rows.append({
      'name': name,
      'summary': info.get('summary') or '',
    })
  return rows
