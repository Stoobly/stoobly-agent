import pdb

from stoobly_agent.app.models.factories.resource.local_db.helpers.log import Log
from stoobly_agent.app.models.factories.resource.local_db.helpers.request_snapshot import RequestSnapshot
from stoobly_agent.app.models.factories.resource.local_db.helpers.scenario_snapshot import ScenarioSnapshot
from stoobly_agent.app.proxy.record import REQUEST_STRING_CLRF, RequestStringControl
from stoobly_agent.app.settings import Settings
from stoobly_agent.lib.logger import bcolors

from ..request_model import RequestModel
from ..scenario_model import ScenarioModel
from .create_request_params_service import build_params

class Apply():

  def __init__(self, **options):
    self.__force = options.get('force') or False
    self.__logger = None
    self.__request_model = None
    self.__scenario_model = None

  @property
  def force(self):
    return self.__force

  @force.setter
  def force(self, v):
    self.__force = v

  @property
  def request_model(self):
    if not self.__request_model:
      self.__request_model = RequestModel(Settings.instance())
    return self.__request_model

  @property 
  def scenario_model(self):
    if not self.__scenario_model:
      self.__scenario_model = ScenarioModel(Settings.instance())
    return self.__scenario_model

  def with_logger(self, logger):
    self.__logger = logger
    return self

  def with_request_model(self, request_model: RequestModel):
    self.__request_model = request_model
    return self

  def with_scenario_model(self, scenario_model: ScenarioModel):
    self.__scenario_model = scenario_model
    return self

  def all(self):
    log = Log()

    unprocessed_events = log.unprocessed_events
    events_count = len(unprocessed_events) 

    if events_count == 0:
      return

    last_processed_event = None

    for event in unprocessed_events:
      if self.__logger:
        self.__logger(f"Processing event {event.uuid}")

      results = event.apply(**self.__handlers())
      if results:
        status = results[1]
        if status == 0 or status >= 500:
          break

      last_processed_event = event

    if last_processed_event:
      last_unprocessed_event = unprocessed_events[events_count - 1]

      if last_processed_event.uuid == last_unprocessed_event.uuid:
        # All unproccessed events have been processed, we are up to date
        log.version = log.next_version()
      else:
        # Some failure occurred, update log to last processed event uuid
        log.version = log.next_version(last_processed_event.uuid)

    log.lock()

  def request(self, uuid: str):
    result = self.__apply_put_request(uuid)
    if not result:
      return False

    status = result[1]
    return status == 200

  def scenario(self, uuid: str):
    result = self.__apply_put_scenario(uuid)
    if not result:
      return False

    status = result[1]
    return status == 200

  def single(self, uuid: str):
    log = Log()

    events = log.events
    events_count = len(events) 

    if events_count == 0:
      return False

    target_event = None
    for event in events:
      if event.uuid == uuid:
        target_event = event
        break

    if not target_event:
      return False

    if self.__logger:
      self.__logger(f"Processing event {event.uuid}")

    event.apply(**self.__handlers())

    return True

  def __handlers(self):
    return {
      'handle_request_delete': self.__apply_delete_request,
      'handle_request_put': self.__apply_put_request,
      'handle_scenario_delete': self.__apply_delete_scenario,
      'handle_scenario_put': self.__apply_put_scenario,
    }

  def __apply_delete_request(self, uuid: str):
    res, status = self.request_model.destroy(uuid, force=self.__force)

    if status == 200:
      self.__logger(f"{bcolors.WARNING}Deleted{bcolors.ENDC} request {uuid}") 
    else: 
      self.__logger(f"{bcolors.FAIL}{status}{bcolors.ENDC} {res}")

    return res, status

  def __apply_put_request(self, uuid: str):
    snapshot = RequestSnapshot(uuid)

    raw_request = snapshot.request
    if not raw_request:
      error = f"Snapshot for request {uuid} not found" 
      self.__logger(f"{bcolors.FAIL}400{bcolors.ENDC} {error}")
      return error, 400

    return self.__put_request(uuid, raw_request)

  def __apply_delete_scenario(self, uuid: str):
    res, status = self.scenario_model.destroy(uuid, force=self.__force)

    if self.__logger and status == 200:
      self.__logger(f"{bcolors.WARNING}Deleted{bcolors.ENDC} scenario {uuid}")
    else: 
      self.__logger(f"{bcolors.FAIL}{status}{bcolors.ENDC} {res}")

    return res, status

  def __apply_put_scenario(self, uuid: str):
    snapshot = ScenarioSnapshot(uuid)
    metadata = snapshot.metadata

    if not metadata:
      error = f"Snapshot for scenario {uuid} not found"
      self.__logger(f"{bcolors.FAIL}400{bcolors.ENDC} {error}")
      return error, 400

    res, status = self.scenario_model.show(uuid)
    if status == 404:
      res, status = self.scenario_model.create(**{
        **metadata,
        'uuid': uuid,
      })

      if self.__logger:
        if status == 200:
          self.__logger(f"{bcolors.OKGREEN}Created scenario{bcolors.ENDC} {res['name']}") 
        else: 
          self.__logger(f"{bcolors.FAIL}{status}{bcolors.ENDC} {res}")
    else:
      res, status = self.scenario_model.update(uuid, **{
        **metadata,
        'is_deleted': False,
      })

      if self.__logger:
        if status == 200:
          self.__logger(f"{bcolors.OKBLUE}Updated{bcolors.ENDC} scenario {res['name']}") 
        else:
          self.__logger(f"{bcolors.FAIL}{status}{bcolors.ENDC} {res}")

    if status != 200:
      return res, status
    else:
      return self.__apply_put_scenario_requests(res, snapshot)

  def __apply_put_scenario_requests(self, scenario, snapshot: ScenarioSnapshot = None):
    if not snapshot:
      snapshot = ScenarioSnapshot(scenario['uuid'])

    snapshot_requests = {}

    raw_requests = snapshot.requests
    for raw_request in raw_requests:
      toks = raw_request.split(REQUEST_STRING_CLRF.encode(), 1)

      if len(toks) != 2:
        return f"{snapshot.requests_path} contains an invalid request", 400

      control = RequestStringControl(toks[0])
      uuid = control.id
      res, status = self.__put_request(uuid, raw_request, scenario_id=scenario['id'])

      snapshot_requests[uuid] = res

    # Remove requests in scenario that don't exist in the snapshot
    scenario_requests = []
    res, status = self.request_model.index(scenario_id=scenario['id'])

    if status == 200:
      scenario_requests = res['list']

    for request in scenario_requests:
      if request['uuid'] in snapshot_requests:
        continue

      res, status = self.__apply_delete_request(request['uuid'])

    return res, status

  def __put_request(self, uuid: str, raw_request: bytes, **base_params):   
    res, status = self.request_model.show(uuid)

    if status == 404:
      params = {
        **build_params(raw_request),
        **base_params,
      }

      res, status = self.request_model.create(**params)

      if self.__logger and status == 200:
        self.__logger(f"{bcolors.OKGREEN}Created{bcolors.ENDC} {res['list'][0]['url']}")
      else: 
        self.__logger(f"{bcolors.FAIL}{status}{bcolors.ENDC} {res}")
    elif status == 200:
      params = {
        'is_deleted': False,
        'request': raw_request,
        **base_params,
      }
      res, status = self.request_model.update(uuid, **params)

      if self.__logger:
        if status == 200:
          self.__logger(f"{bcolors.OKBLUE}Updated{bcolors.ENDC} {res['url']}")
        else: 
          self.__logger(f"{bcolors.FAIL}{status}{bcolors.ENDC} {res}")

    return res, status