import json
from typing import Tuple, Union

from stoobly_agent.app.models.helpers.create_request_service import create_from_gor
from stoobly_agent.app.models.request_model import RequestModel
from stoobly_agent.app.settings import Settings


def looks_like_har(raw_data: Union[bytes, bytearray, str]) -> bool:
  if isinstance(raw_data, str):
    raw_bytes = raw_data.encode('utf-8', errors='replace')
  else:
    raw_bytes = bytes(raw_data)

  try:
    text = raw_bytes.lstrip().decode('utf-8')
  except UnicodeDecodeError:
    return False

  if not text.startswith('{'):
    return False

  try:
    data = json.loads(text)
  except json.JSONDecodeError:
    return False

  return isinstance(data, dict) and isinstance((data.get('log') or {}).get('entries'), list)


class GorImporter:

  def import_file(
    self,
    raw_data,
    scenario_id,
    settings: Settings = None,
    sequence_id: int = None,
    payloads_delimitter=None,
  ) -> Tuple[dict, int]:
    if looks_like_har(raw_data):
      return {
        'error': 'Content looks like HAR. Try format HAR instead.'
      }, 400

    settings = settings or Settings.instance()
    request_model = RequestModel(settings)
    return create_from_gor(
      raw_data,
      request_model,
      settings=settings,
      scenario_id=scenario_id,
      sequence_id=sequence_id,
      payloads_delimitter=payloads_delimitter,
    )
