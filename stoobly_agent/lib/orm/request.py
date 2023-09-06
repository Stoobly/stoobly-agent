import pdb
import uuid

from stoobly_orator.orm import belongs_to, has_many, has_one 

from stoobly_agent.lib.api.keys.project_key import LOCAL_PROJECT_ID
from stoobly_agent.lib.api.keys.request_key import RequestKey
from stoobly_agent.lib.utils.decode import decode

from .base import Base
from .response import Response

class InvalidScenario(Exception):
  pass

class Request(Base):
  __fillable__ = [
    'body_params_hash', 
    'body_text_hash', 
    'pushed_at',
    'control',
    'headers_hash', 
    'host', 
    'http_version',
    'is_deleted',
    'latency',
    'method', 
    'password',
    'path', 
    'port', 
    'query',
    'query_params_hash', 
    'raw', 
    'response_hash',
    'response_headers_hash',
    'scenario_id',
    'scheme', 
    'starred',
    'status',
    'uuid',
    'user',
  ]
  __primary_key__ = 'id'

  @has_one
  def response(self):
    return Response

  @has_many
  def replayed_responses(self):
    return ReplayedResponse

  @belongs_to
  def scenario(self):
    return Scenario

  def key(self):
    return decode(RequestKey.encode(LOCAL_PROJECT_ID, self.uuid))

  # Override
  def to_dict(self):
    h = super().attributes_to_dict()
    h['key'] = self.key()
    return h

  @property
  def url(self):
    s = self.host

    if self.user:
      if not self.password:
        s = f"{self.user}@{s}"
      else:
        s = f"{self.user}:{self.password}@#{s}"

    if self.scheme and len(self.scheme) > 0:
      s = f"{self.scheme}://{s}"

    if self.port != None:
      if not ((self.scheme == 'https' and self.port == 443) or (self.scheme == 'http' and self.port == 80)):
        s = f"{s}:{self.port}"

    s += self.path

    _query = self.get_raw_attribute('query')
    if _query and len(_query) > 0:
      s = f"{s}?{_query}"

    return s

def handle_creating(request):
  if not hasattr(request, 'uuid') or not request.uuid:
    request.uuid = str(uuid.uuid4())
  else:
    try:
      uuid.UUID(request.uuid)
    except Exception:
      request.uuid = str(uuid.uuid4())

def handle_created(request):
  pass

def handle_saving(request):
  if hasattr(request, 'is_deleted') and request.is_deleted:
    request.scenario_id = None

  if hasattr(request, 'scenario_id') and request.scenario_id:
    try:
      # If set as uuid, convert to id
      uuid.UUID(request.scenario_id) 

      scenario = Scenario.find_by(uuid=request.scenario_id)

      if scenario:
        request.scenario_id = scenario.id
      else:
        raise InvalidScenario()
    except Exception:
      scenario = Scenario.find_by(id=request.scenario_id)

      if scenario:
        request.scenario_id = request.scenario_id
      else:
        raise InvalidScenario()

def handle_saved(request):
  request_before = request.get_original()

  if not request_before.get('scenario_id'):
    scenario = request.scenario
    if scenario:
      scenario.requests_count += 1
      scenario.save()
  else:
    if request_before.get('scenario_id') != request.scenario_id:
      scenario = Scenario.find(request_before.get('scenario_id'))
      if scenario:
        scenario.requests_count -= 1
        scenario.save()

      scenario = request.scenario
      if scenario:
        scenario.requests_count += 1
        scenario.save()

def handle_deleting(request):
  response = request.response

  if response:
    response.delete()

  replayed_responses = request.replayed_responses

  for replayed_response in replayed_responses:
    replayed_response.delete()

def handle_deleted(request):
  request_before = request.get_original()

  if request_before.get('scenario_id'):
    # request.scenario returns a cached version of the scenario
    scenario = Scenario.find(request_before['scenario_id'])

    if scenario:
      scenario.requests_count -= 1
      scenario.save()

Request.saved(handle_saved)
Request.saving(handle_saving)
Request.created(handle_created)
Request.creating(handle_creating)
Request.deleted(handle_deleted)
Request.deleting(handle_deleting)

from .replayed_response import ReplayedResponse
from .scenario import Scenario