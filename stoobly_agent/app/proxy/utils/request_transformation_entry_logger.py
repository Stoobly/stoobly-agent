from __future__ import annotations

import re
from collections import defaultdict
from dataclasses import dataclass
from typing import TYPE_CHECKING, Literal, Optional, cast

if TYPE_CHECKING:
    from mitmproxy.http import Request as MitmproxyRequest
    from stoobly_agent.app.proxy.intercept_settings import InterceptSettings

from stoobly_agent.app.proxy.utils.request_correlation import get_proxy_request_uuid
from stoobly_agent.config.constants import mode as agent_mode
from stoobly_agent.config.constants.mode import AgentMode
from stoobly_agent.lib.logger import Logger, bcolors

from .request_transformation_log_cache import (
    RequestTransformationLogCache,
    RequestTransformationLogEntry,
    TransformationLifecycle,
    TransformationTarget,
)

LogLevel = Literal['info', 'error']


@dataclass(frozen=True)
class _BufferedRecord:
    level: LogLevel
    log_id: Optional[str]
    console_message: str
    entry: Optional[RequestTransformationLogEntry]


class RequestTransformationEntryLogger:
    REQUEST_FACADE_LOG_ID = 'RequestFacade'
    RESPONSE_LOG_ID = 'Response'
    FILTER_LOG_ID = 'Filter'
    MOCK_LOG_ID = 'Mock'
    TEST_LOG_ID = 'Test'
    RECORD_LOG_ID = 'Record'
    DEVELOP_LOG_ID = 'Develop'

    _pending: dict[str, list[_BufferedRecord]] = defaultdict(list)

    @staticmethod
    def _rewrite_log_id(mode: Optional[AgentMode], fallback: str) -> str:
        return mode.capitalize() if mode else fallback

    @staticmethod
    def _filter_lifecycle(intercept_settings: InterceptSettings) -> TransformationLifecycle:
        return 'response' if intercept_settings.is_for_response else 'request'

    @classmethod
    def _enqueue(cls, request: Optional['MitmproxyRequest'], record: _BufferedRecord) -> None:
        if request is None:
            cls._emit_one(record)
            return
        request_id = get_proxy_request_uuid(request)
        if not request_id:
            cls._emit_one(record)
            return
        cls._pending[str(request_id)].append(record)

    @staticmethod
    def _emit_one(record: _BufferedRecord) -> None:
        if record.level == 'info':
            Logger.instance(record.log_id).info(record.console_message)
        elif record.log_id is None:
            Logger.instance().error(record.console_message)
        else:
            Logger.instance(record.log_id).error(record.console_message)

    @classmethod
    def flush(cls, request: 'MitmproxyRequest') -> None:
        request_id = get_proxy_request_uuid(request)
        if not request_id:
            return
        key = str(request_id)
        pending = cls._pending.pop(key, None)
        if not pending:
            return
        cache_entries: list[RequestTransformationLogEntry] = []
        for record in pending:
            cls._emit_one(record)
            if record.entry is not None:
                cache_entries.append(record.entry)
        if cache_entries:
            RequestTransformationLogCache.instance().append_many(key, cache_entries)

    @classmethod
    def log_rewrite_request_url(
        cls,
        request: 'MitmproxyRequest',
        mode: Optional[AgentMode],
        url_before: str,
        url_after: str,
    ) -> None:
        log_id = cls._rewrite_log_id(mode, cls.REQUEST_FACADE_LOG_ID)
        details = f'rewriting URL {url_before} => {url_after}'
        cls._enqueue(request, _BufferedRecord(
            level='info',
            log_id=log_id,
            console_message=(
                f"{bcolors.OKCYAN}rewriting{bcolors.ENDC} URL {url_before} => {url_after}"
            ),
            entry={
                'action': 'rewrite',
                'lifecycle': 'request',
                'target': 'url',
                'mode': mode or agent_mode.NONE,
                'details': details,
            },
        ))

    @classmethod
    def log_rewrite_request_parameter(
        cls,
        request: 'MitmproxyRequest',
        mode: Optional[AgentMode],
        component_type: str,
        name: str,
        value: str,
    ) -> None:
        log_id = cls._rewrite_log_id(mode, cls.REQUEST_FACADE_LOG_ID)
        ct_lower = component_type.lower()
        details = f'rewriting request {ct_lower} {name} => {value}'
        cls._enqueue(request, _BufferedRecord(
            level='info',
            log_id=log_id,
            console_message=(
                f"{bcolors.OKCYAN}rewriting{bcolors.ENDC} request {ct_lower} {name} => {value}"
            ),
            entry={
                'action': 'rewrite',
                'lifecycle': 'request',
                'target': cast(TransformationTarget, component_type),
                'mode': mode or agent_mode.NONE,
                'details': details,
            },
        ))

    @classmethod
    def log_rewrite_response_parameter(
        cls,
        request: Optional['MitmproxyRequest'],
        mode: Optional[AgentMode],
        component_type: str,
        name: str,
        value: str,
    ) -> None:
        log_id = cls._rewrite_log_id(mode, cls.RESPONSE_LOG_ID)
        ct_lower = component_type.lower()
        details = f'rewriting {ct_lower} {name} => {value}'
        entry: Optional[RequestTransformationLogEntry] = None
        if request is not None:
            entry = {
                'action': 'rewrite',
                'lifecycle': 'response',
                'target': cast(TransformationTarget, component_type),
                'mode': mode or agent_mode.NONE,
                'details': details,
            }
        cls._enqueue(request, _BufferedRecord(
            level='info',
            log_id=log_id,
            console_message=(
                f"{bcolors.OKCYAN}rewriting{bcolors.ENDC} {ct_lower} {name} => {value}"
            ),
            entry=entry,
        ))

    @classmethod
    def log_rewrite_rule_regexp_error(
        cls,
        request: 'MitmproxyRequest',
        mode: Optional[AgentMode],
        pattern: str,
        exc: re.error,
    ) -> None:
        details = f"RegExp error '{exc}' for {pattern}"
        cls._enqueue(request, _BufferedRecord(
            level='error',
            log_id=None,
            console_message=details,
            entry={
                'action': 'rewrite',
                'lifecycle': 'request',
                'target': 'url',
                'mode': mode or agent_mode.NONE,
                'details': details,
            },
        ))

    @classmethod
    def log_filter_exclude(
        cls,
        request: 'MitmproxyRequest',
        intercept_settings: InterceptSettings,
        mode: str,
        url: str,
    ) -> None:
        lifecycle = cls._filter_lifecycle(intercept_settings)
        log_id = cls._rewrite_log_id(cast(AgentMode, mode), cls.FILTER_LOG_ID)
        details = f'filtering (exclude) {lifecycle} {url}'
        cls._enqueue(request, _BufferedRecord(
            level='info',
            log_id=log_id,
            console_message=(
                f"{bcolors.OKCYAN}filtering{bcolors.ENDC} (exclude) {lifecycle} {url}"
            ),
            entry={
                'action': 'filter',
                'lifecycle': lifecycle,
                'target': 'url',
                'mode': cast(AgentMode, mode),
                'details': details,
            },
        ))

    @classmethod
    def log_filter_include_method_mismatch(
        cls,
        request: 'MitmproxyRequest',
        intercept_settings: InterceptSettings,
        mode: str,
        url: str,
    ) -> None:
        lifecycle = cls._filter_lifecycle(intercept_settings)
        log_id = cls._rewrite_log_id(cast(AgentMode, mode), cls.FILTER_LOG_ID)
        details = f'filtering (not include) {lifecycle} {url}'
        cls._enqueue(request, _BufferedRecord(
            level='info',
            log_id=log_id,
            console_message=(
                f"{bcolors.OKCYAN}filtering{bcolors.ENDC} (not include) {lifecycle} {url}"
            ),
            entry={
                'action': 'filter',
                'lifecycle': lifecycle,
                'target': 'url',
                'mode': cast(AgentMode, mode),
                'details': details,
            },
        ))

    @classmethod
    def log_filter_include_pattern_miss(
        cls,
        request: 'MitmproxyRequest',
        intercept_settings: InterceptSettings,
        mode: str,
        url: str,
    ) -> None:
        lifecycle = cls._filter_lifecycle(intercept_settings)
        log_id = cls._rewrite_log_id(cast(AgentMode, mode), cls.FILTER_LOG_ID)
        details = f'filtering (not include) {lifecycle} {url}'
        cls._enqueue(request, _BufferedRecord(
            level='info',
            log_id=log_id,
            console_message=(
                f"{bcolors.OKCYAN}filtering{bcolors.ENDC} (not include) {lifecycle} {url}"
            ),
            entry={
                'action': 'filter',
                'lifecycle': lifecycle,
                'target': 'url',
                'mode': cast(AgentMode, mode),
                'details': details,
            },
        ))

    @classmethod
    def log_filter_regexp_error(
        cls,
        request: 'MitmproxyRequest',
        intercept_settings: InterceptSettings,
        mode: str,
        pattern: str,
        exc: re.error,
    ) -> None:
        lifecycle = cls._filter_lifecycle(intercept_settings)
        log_id = cls._rewrite_log_id(cast(AgentMode, mode), cls.FILTER_LOG_ID)
        details = f"filtering {lifecycle} RegExp error '{exc}' for {pattern}"
        cls._enqueue(request, _BufferedRecord(
            level='error',
            log_id=log_id,
            console_message=(
                f"{bcolors.OKCYAN}filtering{bcolors.ENDC} {lifecycle} RegExp error '{exc}' for {pattern}"
            ),
            entry={
                'action': 'filter',
                'lifecycle': lifecycle,
                'target': 'url',
                'mode': cast(AgentMode, mode),
                'details': details,
            },
        ))

    @classmethod
    def log_mocked_response(cls, request: 'MitmproxyRequest', url: str, target: str) -> None:
        details = f'mocked {url} -> {target}'
        cls._enqueue(request, _BufferedRecord(
            level='info',
            log_id=cls.MOCK_LOG_ID,
            console_message=f"{bcolors.OKBLUE}mocked{bcolors.ENDC} {url} -> {target}",
            entry={
                'action': 'rewrite',
                'lifecycle': 'response',
                'target': 'url',
                'mode': agent_mode.MOCK,
                'details': details,
            },
        ))

    @classmethod
    def log_testing_response(
        cls,
        request: 'MitmproxyRequest',
        request_key: str,
        request_origin_value: str,
    ) -> None:
        details = f'testing {request_key} from {request_origin_value}'
        cls._enqueue(request, _BufferedRecord(
            level='info',
            log_id=cls.TEST_LOG_ID,
            console_message=(
                f"{bcolors.OKBLUE}testing{bcolors.ENDC} {request_key} from {request_origin_value}"
            ),
            entry={
                'action': 'noop',
                'lifecycle': 'response',
                'target': 'url',
                'mode': agent_mode.TEST,
                'details': details,
            },
        ))

    @classmethod
    def _log_passthrough(cls, log_id: str, verb: str, mode: str, mitmproxy_request: Optional['MitmproxyRequest'], url: str) -> None:
        details = f'{verb} {url}'
        entry: Optional[RequestTransformationLogEntry] = None
        if mitmproxy_request is not None:
            entry = {
                'action': 'noop',
                'lifecycle': 'response',
                'target': 'url',
                'mode': mode,
                'details': details,
            }
        record = _BufferedRecord(
            level='info',
            log_id=log_id,
            console_message=f"{bcolors.OKBLUE}{verb}{bcolors.ENDC} {url}",
            entry=entry,
        )
        if mitmproxy_request is None:
            cls._emit_one(record)
            return
        cls._enqueue(mitmproxy_request, record)

    @classmethod
    def log_recording(cls, mitmproxy_request: Optional['MitmproxyRequest'], url: str) -> None:
        cls._log_passthrough(cls.RECORD_LOG_ID, 'recording', agent_mode.RECORD, mitmproxy_request, url)

    @classmethod
    def log_developing(cls, mitmproxy_request: Optional['MitmproxyRequest'], url: str) -> None:
        cls._log_passthrough(cls.DEVELOP_LOG_ID, 'developing', agent_mode.DEVELOP, mitmproxy_request, url)
