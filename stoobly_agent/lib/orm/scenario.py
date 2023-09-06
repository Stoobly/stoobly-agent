import pdb
import uuid

from stoobly_orator.orm import has_many

from stoobly_agent.lib import orm
from stoobly_agent.lib.api.keys.project_key import LOCAL_PROJECT_ID
from stoobly_agent.lib.api.keys.scenario_key import ScenarioKey

from .base import Base

class Scenario(Base):
  __fillable__ = ['name','description', 'is_deleted', 'overwritable', 'position', 'priority', 'starred', 'uuid']
  
  @has_many
  def requests(self):
    return Request

  def key(self):
    return ScenarioKey.encode(LOCAL_PROJECT_ID, self.uuid)

  # Override
  def to_dict(self):
    h = super().attributes_to_dict()
    h['key'] = self.key()
    return h

def handle_creating(scenario):
  if not hasattr(scenario, 'uuid') or not scenario.uuid:
    scenario.uuid = str(uuid.uuid4())
  else:
    try:
      uuid.UUID(scenario.uuid)
    except Exception as e:
      scenario.uuid = str(uuid.uuid4())

def handle_deleting(scenario):
  requests = scenario.requests
  
  for request in requests:
    request.delete()

Scenario.creating(handle_creating)
Scenario.deleting(handle_deleting)

from .request import Request