import pdb
from orator.orm import has_many

from stoobly_agent.lib import orm
from stoobly_agent.lib.api.keys.project_key import LOCAL_PROJECT_ID
from stoobly_agent.lib.api.keys.scenario_key import ScenarioKey

from .base import Base

class Scenario(Base):
  __fillable__ = ['name','description', 'is_deleted', 'position', 'priority', 'starred']
  
  @has_many
  def requests(self):
    return Request

  def key(self):
    return ScenarioKey.encode(LOCAL_PROJECT_ID, self.id).decode()

  def to_dict(self):
    h = super().to_dict()
    h['key'] = self.key()
    return h

def handle_deleting(scenario):
  requests = scenario.requests
  
  for request in requests:
    request.is_deleted = True
    request.scenario_id = None
    request.save()

Scenario.deleting(handle_deleting)

from .request import Request