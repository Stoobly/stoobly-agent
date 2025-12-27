import asyncio
import os
import pdb
import threading

from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mitmproxy.http import Request as MitmproxyRequest

from stoobly_agent.app.proxy.handle_replay_service import handle_request_replay, handle_response_replay
from stoobly_agent.app.settings.constants.mode import TEST
from stoobly_agent.app.models.request_model import RequestModel
from stoobly_agent.app.proxy.intercept_settings import InterceptSettings
from stoobly_agent.config.constants.env_vars import ENV
from stoobly_agent.config.constants import lifecycle_hooks, mode, record_order, record_policy, record_strategy
from stoobly_agent.lib.logger import Logger

from .constants import custom_response_codes
from .mock.eval_request_service import inject_eval_request
from .record.context import RecordContext
from .record.overwrite_scenario_service import overwrite_scenario
from .record.upload_request_service import inject_upload_request
from .replay.context import ReplayContext
from .replay.body_parser_service import is_json, is_xml
from .utils.allowed_request_service import get_active_mode_policy
from .utils.minimize_headers import minimize_headers
from .utils.response_handler import bad_request, disable_transfer_encoding 
from .utils.rewrite import rewrite_request_response
from .utils.strategy import get_active_mode_strategy


LOG_ID = 'Record'

# Shared thread pool executor for record operations
# Limits concurrent record operations and integrates with asyncio event loop
#
# Shutdown handling not needed, this module will not be reloaded, 
# so we can safely use a global variable and not worry about it being recreated on each request
_record_executor = None
_MAX_WORKERS = 10

###
#
# 1. BEFORE_REPLAY gets triggered
#
def handle_request_record(context: ReplayContext) -> None:
    # To differentiate record rewrite rules, outbound request uses replay rules
    # Record rules are applied to the request and its response when storing
    handle_request_replay(context)

###
# 1. AFTER_REPLAY gets triggered
# 2. BEFORE_RECORD gets triggered
# 3. AFTER_RECORD gets triggered
#
def handle_response_record(context: RecordContext):
    flow = context.flow
    intercept_settings = context.intercept_settings

    disable_transfer_encoding(flow.response)
    handle_response_replay(context)

    # Lazy import for runtime usage
    from mitmproxy.http import Request as MitmproxyRequest
    request: 'MitmproxyRequest' = flow.request
    request_model = RequestModel(intercept_settings.settings)

    active_record_policy = get_active_mode_policy(request, intercept_settings, mode.RECORD)
    Logger.instance(LOG_ID).debug(f"RecordPolicy: {active_record_policy}")

    if active_record_policy == record_policy.ALL:
        __record_request(context, request_model)
    elif active_record_policy == record_policy.API:
        response = flow.response
        content_type: str = response.headers.get('content-type')

        if content_type:
            if is_json(content_type) or is_xml(content_type) or content_type.startswith('text/plain'):
                __record_request(context, request_model)
    elif active_record_policy == record_policy.FOUND:
        res = inject_eval_request(request_model, intercept_settings)(request, [])

        if res.status_code != custom_response_codes.NOT_FOUND:
            __record_request(context, request_model)
    elif active_record_policy == record_policy.NOT_FOUND:
        res = inject_eval_request(request_model, intercept_settings)(request, [])

        if res.status_code == custom_response_codes.NOT_FOUND:
            __record_request(context, request_model)
    else:
        if active_record_policy != record_policy.NONE:
            return bad_request(
                flow,
                "Valid record policies: %s, Got: %s" %
                ([record_policy.ALL, record_policy.API, record_policy.FOUND, record_policy.NOT_FOUND], active_record_policy)
            )

def __record_handler(context: RecordContext, request_model: RequestModel):
    flow = context.flow
    flow_copy = deepcopy(flow)
    intercept_settings = context.intercept_settings

    context.flow = flow_copy # Deep copy flow to prevent response modifications from persisting

    active_record_strategy = get_active_mode_strategy(intercept_settings)
    if active_record_strategy == record_strategy.MINIMAL:
        minimize_headers(flow_copy)

    rewrite_request_response(flow_copy, intercept_settings.record_rewrite_rules)

    __record_hook(lifecycle_hooks.BEFORE_RECORD, context)

    inject_upload_request(request_model, intercept_settings)(flow_copy)

    __record_hook(lifecycle_hooks.AFTER_RECORD, context)
    context.flow = flow # Reset flow

def __record_request(context: RecordContext, request_model: RequestModel):
    intercept_settings = context.intercept_settings

    # If record order header is set to overwrite, then make the scenario overwritable
    if intercept_settings.order_from_header == record_order.OVERWRITE:
        scenario_key = intercept_settings.parsed_scenario_key
        scenario_model = intercept_settings.scenario_model
        if scenario_key and scenario_model:
            res, status = scenario_model.update(scenario_key.id, **{ 'overwritable': True })
            if status != 200:
                Logger.instance(LOG_ID).error(f"Failed to update scenario {scenario_key.id} to overwritable: {res}")
                return
            
            overwrite_scenario(scenario_key)
    elif intercept_settings.order == record_order.OVERWRITE:
        scenario_key = intercept_settings.parsed_scenario_key

        if scenario_key:
            overwrite_scenario(scenario_key)

    if os.environ.get(ENV) == TEST:
        __record_handler(context, request_model)
    else:
        # Use asyncio.run_in_executor to schedule record handler without blocking event loop
        # This integrates with mitmproxy's async event loop and limits thread usage
        try:
            loop = asyncio.get_running_loop()
            # Schedule the blocking I/O operation in a thread pool
            # This allows the event loop to process other requests while upload happens
            # When max_workers is reached, tasks are queued and processed as workers become available
            executor = __get_record_executor()
            loop.run_in_executor(executor, __record_handler, context, request_model)
        except RuntimeError:
            # No running event loop, fall back to threading for compatibility
            # This should rarely happen in mitmproxy context
            thread = threading.Thread(
                target=__record_handler,
                args=[context, request_model],
                daemon=True  # Mark as daemon to avoid blocking shutdown
            )
            thread.start()

def __get_record_executor():
    """Get or create the shared thread pool executor for record operations."""
    global _record_executor
    if _record_executor is None:
        # Use a reasonable max_workers to limit resource usage
        # This allows multiple concurrent uploads without creating unlimited threads
        _record_executor = ThreadPoolExecutor(max_workers=_MAX_WORKERS, thread_name_prefix='request-record')
    return _record_executor

def __record_hook(hook: str, context: RecordContext):
    intercept_settings: InterceptSettings = context.intercept_settings
    lifecycle_hooks_module = intercept_settings.lifecycle_hooks

    if hook in lifecycle_hooks_module:
        lifecycle_hooks_module[hook](context)