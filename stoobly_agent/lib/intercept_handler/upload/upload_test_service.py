from mitmproxy.http import HTTPFlow as MitmproxyHTTPFlow
from requests import Response

from stoobly_agent.lib.api.tests_resource import TestsResource
from stoobly_agent.lib.settings import IProjectTestSettings, Settings
from stoobly_agent.lib.logger import Logger

from .join_request_service import join_filtered_request
from ..settings import get_report_key

def inject_upload_test(
  api: TestsResource,
  active_mode_settings: IProjectTestSettings, 
):
  settings = Settings.instance()

  if not api:
    api = TestsResource(settings.api_url, settings.api_key)

  if not active_mode_settings:
    active_mode_settings = Settings.instance().active_mode_settings

  return lambda flow, **kwargs: upload_test(api, active_mode_settings, flow, **kwargs)

def upload_test(
  api: TestsResource,
  active_mode_settings: IProjectTestSettings, 
  flow: MitmproxyHTTPFlow, 
  **kwargs
) -> Response:
    joined_request = join_filtered_request(flow, active_mode_settings)

    Logger.instance().info(f"Uploading test results for {joined_request.proxy_request.url()}")

    raw_requests = joined_request.build()

    # If report key is set, upload test to report
    report_key = get_report_key(flow.request.headers)
    if report_key:
      Logger.instance().debug(f"Using report {report_key}")

      api.with_report_key(report_key, kwargs)

    scenario_key = active_mode_settings.get('scenario_key')
    if scenario_key:
      return api.from_scenario_key(
        scenario_key, 
        lambda project_id, query_params: api.create(project_id, raw_requests, { **query_params, **kwargs })
      )
    else:
      return api.from_project_key(
        active_mode_settings.get('project_key'),
        lambda project_id: api.create(project_id, raw_requests, { **kwargs })
      )