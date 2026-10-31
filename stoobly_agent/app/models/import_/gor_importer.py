from stoobly_agent.app.models.helpers.create_request_service import create_from_gor
from stoobly_agent.app.models.request_model import RequestModel
from stoobly_agent.app.settings import Settings


class GorImporter:

  def import_file(self, raw_data, scenario_id, settings: Settings = None):
    settings = settings or Settings.instance()
    request_model = RequestModel(settings)
    return create_from_gor(
      raw_data,
      request_model,
      settings=settings,
      scenario_id=scenario_id,
    )
