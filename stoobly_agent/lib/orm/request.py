from argparse import ONE_OR_MORE
import pdb
from orator.orm import belongs_to, has_one

from stoobly_agent.lib.api.keys.project_key import LOCAL_PROJECT_ID
from stoobly_agent.lib.api.keys.request_key import RequestKey

from .base import Base
from .response import Response

class Request(Base):
  __fillable__ = [
    'body_params_hash', 
    'body_text_hash', 
    'committed_at',
    'control',
    'headers_hash', 
    'host', 
    'is_deleted',
    'latency',
    'method', 
    'password',
    'path', 
    'port', 
    'query',
    'query_params_hash', 
    'raw', 
    'scenario_id',
    'scheme', 
    'starred',
    'status',
    'user',
  ]
  __primary_key__ = 'id'

  @has_one
  def response(self):
    return Response

  @belongs_to
  def scenario(self):
    return Scenario

  def key(self):
    return RequestKey.encode(LOCAL_PROJECT_ID, self.id).decode()

  def to_dict(self):
    h = super().to_dict()
    h['key'] = self.key()
    return h

# Handles creating and updating
def handle_created(request):
  scenario = request.scenario

  if scenario:
    scenario.requests_count += 1
    scenario.save()

def handle_deleting(request):
  response = request.response

  if response:
    response.delete()

def handle_deleted(request):
  scenario = request.scenario

  if scenario:
    scenario.requests_count -= 1
    scenario.save()

Request.created(handle_created)
Request.deleted(handle_deleted)
Request.deleting(handle_deleting)

from .scenario import Scenario