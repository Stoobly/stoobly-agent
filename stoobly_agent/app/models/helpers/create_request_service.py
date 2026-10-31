import uuid as uuid_lib

from typing import Optional, Tuple

from stoobly_agent.app.models.helpers.create_request_params_service import (
  MitmproxyFlowMock,
  build_params,
  build_params_from_python,
)
from stoobly_agent.app.models.request_model import RequestModel
from stoobly_agent.app.proxy.intercept_settings import InterceptSettings
from stoobly_agent.app.proxy.record import REQUEST_DELIMITTER
from stoobly_agent.app.proxy.record.join_request_service import join_request_from_flow
from stoobly_agent.app.proxy.utils.allowed_request_service import allowed_request
from stoobly_agent.app.proxy.utils.rewrite import rewrite_request_response
from stoobly_agent.app.settings import Settings
from stoobly_agent.config.constants import mode


class InvalidRequestFormatError(Exception):
  pass


class RequestNotAllowedError(Exception):
  pass


REQUEST_NOT_ALLOWED_STATUS = 403
INVALID_FORMAT_STATUS = 400


def create_from_flow(
  flow: MitmproxyFlowMock,
  request_model: RequestModel,
  settings: Settings = None,
  scenario_id=None,
  request_uuid: str = None,
  sequence_id: int = None,
  skip_if_not_allowed: bool = False,
) -> Tuple[Optional[dict], Optional[int]]:
  """
  Persist a single request from a mitmproxy flow mock.

  Applies RECORD-mode firewall (filter) rules and rewrite rules before create.
  When skip_if_not_allowed is True and the request is blocked, returns (None, None).
  When skip_if_not_allowed is False and blocked, raises RequestNotAllowedError.
  """
  settings = settings or Settings.instance()
  intercept_settings = InterceptSettings(settings, flow.request)

  if not allowed_request(flow.request, intercept_settings, mode.RECORD):
    if skip_if_not_allowed:
      return None, None
    raise RequestNotAllowedError('Request blocked by firewall rules')

  rewrite_request_response(flow, intercept_settings.record_rewrite_rules, mode=mode.RECORD)

  joined_request = join_request_from_flow(flow, intercept_settings=intercept_settings)

  create_body = {
    'flow': flow,
    'joined_request': joined_request,
    'uuid': request_uuid or str(uuid_lib.uuid4()),
  }
  if scenario_id is not None:
    create_body['scenario_id'] = scenario_id
  if sequence_id is not None:
    create_body['sequence_id'] = sequence_id

  return request_model.create(**create_body)


def create_from_python(
  request,
  response,
  request_model: RequestModel,
  settings: Settings = None,
  scenario_id=None,
  request_uuid: str = None,
  sequence_id: int = None,
  skip_if_not_allowed: bool = False,
) -> Tuple[Optional[dict], Optional[int]]:
  params = build_params_from_python(request, response)
  if not params:
    raise InvalidRequestFormatError('Could not parse request')

  return create_from_flow(
    params['flow'],
    request_model,
    settings=settings,
    scenario_id=scenario_id,
    request_uuid=request_uuid,
    sequence_id=sequence_id,
    skip_if_not_allowed=skip_if_not_allowed,
  )


def create_from_gor(
  raw_requests,
  request_model: RequestModel,
  settings: Settings = None,
  scenario_id=None,
  sequence_id: int = None,
  payloads_delimitter=None,
) -> Tuple[dict, int]:
  """
  Create one or more requests from GOR-joined request/response bytes.

  Blocked requests (firewall) are skipped. Invalid format raises InvalidRequestFormatError.
  """
  payloads_delimitter = payloads_delimitter or REQUEST_DELIMITTER
  if isinstance(raw_requests, str):
    raw_requests = raw_requests.encode()
  if isinstance(payloads_delimitter, str):
    payloads_delimitter = payloads_delimitter.encode()

  toks = raw_requests.split(payloads_delimitter)

  if len(toks) % 2 != 0:
    raise InvalidRequestFormatError('Invalid requests format')

  created_requests = []

  for i in range(0, len(toks), 2):
    raw_request = payloads_delimitter.join([toks[i], toks[i + 1]])
    create_params = build_params(raw_request, payloads_delimitter)

    if not create_params:
      raise InvalidRequestFormatError('Could not parse requests')

    res, status = create_from_flow(
      create_params['flow'],
      request_model,
      settings=settings,
      scenario_id=scenario_id,
      sequence_id=sequence_id,
      skip_if_not_allowed=True,
    )

    if res is None and status is None:
      continue

    if status and status >= 400:
      return res, status

    created_requests.append(res['list'][0])

  return {
    'list': created_requests,
    'total': len(created_requests),
  }, 200
