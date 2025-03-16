import pdb
from typing import TypedDict

from mitmproxy.http import HTTPFlow as MitmproxyHTTPFlow
from requests import Response

from stoobly_agent.lib.api.tests_resource import TestsResource
from stoobly_agent.app.settings import Settings
from stoobly_agent.lib.logger import Logger, bcolors

from stoobly_agent.app.proxy.intercept_settings import InterceptSettings

from ...intercept_settings import InterceptSettings
from ...record.join_request_service import join_request_from_flow

LOG_ID = 'Test'

class UploadTestData(TypedDict):
  expected_response: str
  log: str
  passed: bool
  request_id: int
  status: int
  strategy: str

def inject_upload_test(
  api: TestsResource,
  intercept_settings: InterceptSettings, 
):
  settings = intercept_settings.settings

  if not api:
    api = TestsResource(settings.remote.api_url, settings.remote.api_key)

  if not intercept_settings:
    intercept_settings = InterceptSettings(Settings.instance(LOG_ID))

  return lambda flow, **kwargs: upload_test(api, intercept_settings, flow, **kwargs)

def upload_test(
  api: TestsResource,
  intercept_settings: InterceptSettings, 
  flow: MitmproxyHTTPFlow, 
  **kwargs: UploadTestData
) -> Response:
    joined_request = join_request_from_flow(flow, intercept_settings)

    Logger.instance(LOG_ID).info(f"{bcolors.OKCYAN}Uploading{bcolors.ENDC} test results for {joined_request.proxy_request.url()}")

    raw_requests = joined_request.build()

    # If report key is set, upload test to report
    report_key = intercept_settings.report_key
    if report_key:
      Logger.instance(LOG_ID).debug(f"Using report {report_key}")

      api.with_report_key(report_key, kwargs)

    scenario_key = intercept_settings.scenario_key
    if scenario_key:
      return api.from_scenario_key(
        scenario_key, 
        lambda project_id, query_params: api.create(project_id, raw_requests, { **query_params, **kwargs })
      )
    else:
      return api.from_project_key(
        intercept_settings.project_key,
        lambda project_id: api.create(project_id, raw_requests, { **kwargs })
      )