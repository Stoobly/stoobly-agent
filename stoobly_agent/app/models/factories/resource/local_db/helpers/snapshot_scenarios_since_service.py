from datetime import datetime, timezone
from typing import List, Tuple

from stoobly_agent.app.models.scenario_model import ScenarioModel
from stoobly_agent.app.settings import Settings
from stoobly_agent.lib.api.interfaces.scenarios import ScenarioShowResponse

from .snapshot_types import PUT_ACTION

TIMESTAMP_FORMAT = '%Y-%m-%d %H:%M:%S'

def snapshot_scenarios_since(updated_since: str, **options) -> List[Tuple[ScenarioShowResponse, str]]:
  """
  Snapshot all scenarios updated at or after `updated_since`.

  `updated_since` is expected to be an ISO-8601 timestamp.
  """
  formatted_updated_since = __normalize_iso_datetime(updated_since)

  data_dir_path = options.get('data_dir_path')

  scenario_model = ScenarioModel(
    Settings.instance(data_dir_path),
    data_dir_path=data_dir_path,
  )
  scenario_model.as_local()

  snapshots = []

  snapshot_options = {
    'action': PUT_ACTION,
    **options,
  }

  page = 0
  size = 100
  while True:
    res, status = scenario_model.index(page=page, size=size, updated_since=formatted_updated_since)
    if status != 200:
      break

    scenarios = res.get('list') or []
    for scenario in scenarios:
      scenario_id = scenario.get('uuid') or scenario.get('id')
      if not scenario_id:
        continue

      file_path, snapshot_status = scenario_model.snapshot(scenario_id, **snapshot_options)
      if snapshot_status == 200 and file_path:
        snapshots.append((scenario, file_path))

    total = res.get('total') or len(scenarios)
    if (page + 1) * size >= total:
      break
    page += 1

  return snapshots

def __normalize_iso_datetime(updated_since: str) -> str:
  if not updated_since:
    raise ValueError('updated_since is required')

  # Python does not parse a trailing Z in fromisoformat, normalize first.
  normalized = updated_since.replace('Z', '+00:00')
  parsed = datetime.fromisoformat(normalized)

  if parsed.tzinfo:
    parsed = parsed.astimezone(timezone.utc).replace(tzinfo=None)

  return parsed.strftime(TIMESTAMP_FORMAT)
