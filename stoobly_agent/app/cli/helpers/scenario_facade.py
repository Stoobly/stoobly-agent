import pdb
import time
from pathlib import Path

from stoobly_agent.app.cli.helpers.iterate_group_by import iterate_group_by
from stoobly_agent.app.cli.helpers.replay_facade import ReplayCliOptions, ReplayFacade, TestCliOptions
from stoobly_agent.app.models.helpers.create_request_service import InvalidRequestFormatError
from stoobly_agent.app.models.import_ import get_importer
from stoobly_agent.app.models.request_model import RequestModel
from stoobly_agent.app.models.scenario_model import ScenarioModel
from stoobly_agent.app.proxy.replay.replay_scenario_service import inject_replay
from stoobly_agent.app.proxy.replay.trace_context import TraceContext
from stoobly_agent.app.settings import Settings
from stoobly_agent.config.constants import mode
from stoobly_agent.lib.api.keys import ProjectKey, ScenarioKey

class ScenarioFacade(ReplayFacade):

  def __init__(self, settings: Settings):
    super().__init__(settings)
    self.__model = ScenarioModel(settings)
    self.__settings = settings

  def create(self, project_key: str, name: str, description: str = ''):
    key = ProjectKey(project_key)
    return self.__model.create(**{
      'project_id': key.id, 
      'description': description,
      'name': name,
    })

  def import_file(
    self,
    file_path: str,
    format: str,
    scenario_key: str = None,
    project_key: str = None,
    overwrite: bool = False,
  ):
    path = Path(file_path)
    raw = path.read_bytes()

    created_scenario = False
    if scenario_key:
      key = ScenarioKey(scenario_key)
      scenario, status = self.__model.show(key.id)
      if status != 200:
        return scenario, status
    else:
      name = f"{path.stem}-{int(time.time())}"
      scenario, status = self.create(project_key, name)
      if status != 200:
        return scenario, status
      key = ScenarioKey(scenario['key'])
      created_scenario = True

    scenario_id = key.id
    request_model = RequestModel(self.__settings)
    existing_ids = set(self.__scenario_request_ids(request_model, scenario_id)) if overwrite else set()

    importer = get_importer(format)
    try:
      import_res, import_status = importer.import_file(raw, scenario_id, settings=self.__settings)
    except InvalidRequestFormatError as e:
      self.__rollback_import(request_model, scenario_id, created_scenario, overwrite, existing_ids)
      return {'error': str(e)}, 400

    if import_status != 200:
      self.__rollback_import(request_model, scenario_id, created_scenario, overwrite, existing_ids)
      return import_res, import_status

    if overwrite and existing_ids:
      request_model.destroy_all(ids=list(existing_ids))

    return self.__model.show(scenario_id)

  def __scenario_request_ids(self, request_model: RequestModel, scenario_id) -> list:
    ids = []
    page = 0
    size = 100
    while True:
      indexed, status = request_model.index(scenario_id=scenario_id, page=page, size=size)
      if status != 200 or not isinstance(indexed, dict):
        break
      batch = indexed.get('list') or []
      ids.extend(r['id'] for r in batch if r.get('id') is not None)
      total = indexed.get('total') or 0
      if len(ids) >= total or len(batch) < size:
        break
      page += 1
    return ids

  def __rollback_import(
    self,
    request_model: RequestModel,
    scenario_id,
    created_scenario: bool,
    overwrite: bool,
    existing_ids: set,
  ):
    if created_scenario:
      self.__model.destroy(scenario_id, force=True)
      return

    if not overwrite:
      return

    # Drop requests created during the failed import; keep prior ones.
    current_ids = self.__scenario_request_ids(request_model, scenario_id)
    new_ids = [request_id for request_id in current_ids if request_id not in existing_ids]
    if new_ids:
      request_model.destroy_all(ids=new_ids)

  def index(self, project_key, cli_options: dict):
    key = ProjectKey(project_key)
    return self.__model.index(**{ 'project_id': key.id, **cli_options})

  def show(self, scenario_key: str):
    key = ScenarioKey(scenario_key)
    return self.__model.show(key.id)

  def replay(self, source_key: str, cli_options: ReplayCliOptions):
    return self.__replay(source_key, {
      'mode': mode.RECORD if cli_options.get('record') else mode.DEVELOP,
      **self.common_replay_cli_options(cli_options),
      **self.__common_replay_options(source_key),
    })

  def snapshot(self, scenario_key: str, cli_options: dict):
    key = ScenarioKey(scenario_key)

    return self.__model.snapshot(key.id, **cli_options)

  def test(self, scenario_key: str, cli_options: TestCliOptions):
    return self.__replay(scenario_key, {
      'mode': mode.TEST,
      'report_key': cli_options.get('report_key'),
      'scenario_key': scenario_key, # Mock the request from the specified scenario instead of active scenario
      **self.common_test_cli_options(cli_options),
      **self.__common_replay_options(scenario_key),
    })

  def delete(self, scenario_key: str):
    key = ScenarioKey(scenario_key)

    return self.__model.destroy(key.id)

  def __common_replay_options(self, scenario_key: str):
    return {
      'project_key': ProjectKey.encode(ScenarioKey(scenario_key).project_id),
    }

  def __replay(self, scenario_key: str, replay_options: ReplayCliOptions):
    trace_context = replay_options['trace_context']
    group_by = replay_options['group_by']

    if not group_by or not trace_context:
      replay = inject_replay()
      return replay(scenario_key, replay_options)
    else:
      return iterate_group_by(
        group_by, 
        trace_context,
        lambda trace_context: self.__replay_with_trace_context(trace_context, scenario_key, replay_options)
      )

  def __replay_with_trace_context(self, trace_context: TraceContext, scenario_key: str, replay_options: ReplayCliOptions):
    _replay_options = replay_options.copy()
    _replay_options['trace_context'] = trace_context
    replay = inject_replay()
    return replay(scenario_key, _replay_options)
