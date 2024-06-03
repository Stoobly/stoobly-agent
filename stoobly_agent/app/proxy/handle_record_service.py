import os
import pdb
import threading

from mitmproxy.http import Request as MitmproxyRequest

from stoobly_agent.app.settings.constants.mode import TEST
from stoobly_agent.app.models.request_model import RequestModel
from stoobly_agent.app.proxy.intercept_settings import InterceptSettings
from stoobly_agent.config.constants.env_vars import ENV
from stoobly_agent.config.constants import lifecycle_hooks, record_policy
from stoobly_agent.lib.logger import Logger

from .constants import custom_response_codes
from .mock.eval_request_service import inject_eval_request
from .record.context import RecordContext
from .record.overwrite_scenario_service import overwrite_scenario
from .record.upload_request_service import inject_upload_request
from .utils.allowed_request_service import get_active_mode_policy
from .utils.response_handler import bad_request, disable_transfer_encoding 

LOG_ID = 'Record'

def handle_response_record(context: RecordContext):
    flow = context.flow
    disable_transfer_encoding(flow.response)

    __record_hook(lifecycle_hooks.BEFORE_RECORD, context)

    intercept_settings = context.intercept_settings
    request: MitmproxyRequest = flow.request
    request_model = RequestModel(intercept_settings.settings)

    active_record_policy = get_active_mode_policy(request, intercept_settings)
    Logger.instance(LOG_ID).debug(f"RecordPolicy: {active_record_policy}")

    if active_record_policy == record_policy.ALL:
        __record_request(context, request_model)
    elif active_record_policy == record_policy.FOUND:
        res = inject_eval_request(request_model, intercept_settings)(request, [])

        if res.status_code != custom_response_codes.NOT_FOUND:
            __record_request(context , request_model)
    elif active_record_policy == record_policy.NOT_FOUND:
        res = inject_eval_request(request_model, intercept_settings)(request, [])

        if res.status_code == custom_response_codes.NOT_FOUND:
            __record_request(context, request_model)
    elif active_record_policy == record_policy.OVERWRITE:
        overwrite_scenario(intercept_settings.scenario_key)

        __record_request(context, request_model)
    else:
        if active_record_policy != record_policy.NONE:
            return bad_request(
                flow,
                "Valid env RECORD_POLICY: %s, Got: %s" %
                ([record_policy.ALL, record_policy.FOUND, record_policy.NOT_FOUND], active_record_policy)
            )

def __record_handler(context: RecordContext, request_model: RequestModel):
    flow = context.flow
    intercept_settings = context.intercept_settings

    inject_upload_request(request_model, intercept_settings)(flow)

    __record_hook(lifecycle_hooks.AFTER_RECORD, context)

def __record_request(context: RecordContext, request_model: RequestModel):
    if os.environ.get(ENV) == TEST:
        __record_handler(context, request_model)
    else:
        thread = threading.Thread(
            target=__record_handler,
            args=[context, request_model]
        )
        thread.start()

def __record_hook(hook: str, context: RecordContext):
    intercept_settings: InterceptSettings = context.intercept_settings
    lifecycle_hooks_module = intercept_settings.lifecycle_hooks

    if hook in lifecycle_hooks_module:
        lifecycle_hooks_module[hook](context)