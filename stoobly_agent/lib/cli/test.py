import json
import pdb
import requests

from typing import List, Union

from stoobly_agent.lib.api.interfaces.report_show_response import ReportShowResponse
from stoobly_agent.lib.api.interfaces.requests_index_query_params import RequestsIndexQueryParams
from stoobly_agent.lib.api.interfaces.requests_index_response import RequestsIndexResponse
from stoobly_agent.lib.api.schemas.request import Request
from stoobly_agent.lib.api.stoobly_api import StooblyApi
from stoobly_agent.lib.intercept_handler.constants import modes

from .replay_request_service import replay_request

class Test():

  def __init__(self, api: StooblyApi, project_key: str, strategy: str):
    self.report_key = None
    self.scenario_keys = []

    self.api = api
    self.project_key = project_key
    self.strategy = strategy

  def from_scenario(self, scenario_key: str):
    self.scenario_keys.append(scenario_key)

  def to_report(self, report_key: str):
    self.report_key = report_key

  def create_report(self, name: str, description: str = ''):
    report = self.__create_report(self.project_key, name, description)
    self.report_key = report.get('key')

  def run(self):
    if not self.report_key:
      return

    for scenario_key in self.scenario_keys:
      self.__map_scenario_requests(scenario_key, replay_request)

  def __create_report(self, project_key: str, name, description) -> ReportShowResponse:
    res: requests.Response = self.api.report_create(project_key, {
      'description': description,
      'name': name,
    })

    if not res.ok:
      raise AssertionError('Could not create report')

    return res.json()

  def __get_requests(
    self, project_key: str, scenario_key: str, query_params: RequestsIndexQueryParams = {}
  ) -> Union[None, RequestsIndexResponse]:
    scenario_data = StooblyApi.decode_scenario_key(scenario_key)
    scenario_id = scenario_data['id']

    res = self.api.requests_index(project_key, {
      'scenario_id': scenario_id,
      'page': query_params.get('page'),
      'size': query_params.get('size'),
    })

    if not res.ok:
      raise AssertionError(f"Could not get requests for scenario {scenario_key}")

    return res.json()

  def __get_request(self, project_key: str, request_id: int):
    res = self.api.request_show(
      project_key, request_id, {
        'body': True,
        'headers': True,
        'query_params': True,
        'response': True
      }
    )

    if not res.ok:
      raise AssertionError(f"Could not get details for request {request_id}")

    return res.json()

  def __map_scenario_requests(self, scenario_key: str, handler):
    page = 0
    count = 0

    l = []

    while True:
      requests_response = self.__get_requests(
        self.project_key, scenario_key, { 
          'page': page, 'size': '25'
        }
      )

      if not requests_response:
        return l

      total = requests_response['total']
      requests = requests_response['list']
      
      if len(requests) == 0:
        return l

      for request_partial in requests:
        request_id = request_partial['id']
        request = self.__get_request(self.project_key, request_id)

        response = handler(
          Request(request), 
          mode=modes.TEST,
          project_key=self.project_key,
          report_key=self.report_key,
          scenario_key=scenario_key
        )

        l.append(response)

      count += len(requests)

      if count >= total:
        return l

      page += 1
