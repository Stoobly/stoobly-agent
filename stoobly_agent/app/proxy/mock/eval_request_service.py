import json
import pdb
import re

from mitmproxy.http import Request as MitmproxyRequest
from requests import Response
from typing import List, TypedDict, Union
from stoobly_agent.config.constants import custom_headers

from stoobly_agent.lib.api.param_builder import ParamBuilder
from stoobly_agent.lib.api.interfaces.requests import RequestResponseShowQueryParams
from stoobly_agent.lib.logger import Logger
from stoobly_agent.app.models.request_model import RequestModel
from stoobly_agent.app.proxy.intercept_settings import InterceptSettings
from stoobly_agent.app.settings import Settings
from stoobly_agent.app.settings.constants import request_component
from stoobly_agent.app.settings.match_rule import MatchRule

from .hashed_request_decorator import HashedRequestDecorator
from .search_endpoint import inject_search_endpoint
from ..mitmproxy.request_facade import MitmproxyRequestFacade

class EvalRequestOptions(TypedDict):
    infer: bool
    retry: int

def inject_eval_request(
    request_model: RequestModel,
    intercept_settings: InterceptSettings,
):
    settings = Settings.instance()

    if not request_model:
        request_model = RequestModel(settings)

    if not intercept_settings:
        intercept_settings = InterceptSettings(intercept_settings)

    return lambda request, ignored_components, **options: eval_request(
        request_model, intercept_settings, request, ignored_components or [], **options 
    )

###
#
# @param settings [Settings.mode.mock | Settings.mode.record]
#
def eval_request(
    request_model: RequestModel,
    intercept_settings: InterceptSettings,
    request: MitmproxyRequest,
    ignored_components_list: List[Union[list, str, None]],
    **options: EvalRequestOptions
) -> Response:
    query_params_builder = ParamBuilder({})
    query_params_builder.with_resource_scoping(intercept_settings.project_key, intercept_settings.scenario_key)

    # Tease out API returning ignored components on not found
    if request_model.is_local and not options.get('retry'):
        remote_project_key = intercept_settings.parsed_remote_project_key

        if remote_project_key:
            search_endpoint = inject_search_endpoint(intercept_settings)
            remote_project_id = remote_project_key.id
            endpoint_promise = lambda: search_endpoint(remote_project_id, request.method, request.url, ignored_components=1) 

            query_params_builder.with_param('endpoint_promise', endpoint_promise)

    ignored_components = __build_ignored_components(ignored_components_list or [])
    query_params_builder.with_params(__build_request_params(request, ignored_components))
    query_params_builder.with_params(__build_optional_params(request, options))

    query_params = query_params_builder.build()
    __filter_by_match_rules(request, intercept_settings.match_rules, query_params)

    return request_model.response(**query_params)

def __build_ignored_components(ignored_components_list):
    ignored_components = []
    for el in ignored_components_list:
        if isinstance(el, bytes) or isinstance(el, str): 
            try:
                ignored_components += json.loads(el)
            except:
                pass
        elif isinstance(el, list):
            ignored_components += el
        elif isinstance(el, dict):
            ignored_components.append(el)

    return ignored_components

###
#
# Formats request into parameters expected by stoobly request_model
#
# @param request [lib.mitmproxy_request_adapter.MitmproxyRequestFacade]
# @param ignored_components [Array<Hash>]
#
# @return [Hash] query parameters to pass to stoobly request_model
#
def __build_request_params(request: MitmproxyRequest, ignored_components = []) -> RequestResponseShowQueryParams:
    request = MitmproxyRequestFacade(request)
    hashed_request = HashedRequestDecorator(request).with_ignored_components(ignored_components)

    query_params = {}
    query_params['host'] = request.host
    query_params['path'] = request.path
    query_params['port'] = request.port
    query_params['method'] = request.method

    headers_hash = hashed_request.headers_hash()
    query_params['headers_hash'] = headers_hash

    query_params_hash = hashed_request.query_params_hash()
    query_params['query_params_hash'] = query_params_hash

    body_params_hash = hashed_request.body_params_hash()
    body_text_hash = hashed_request.body_text_hash()

    # If a body_param_hash is not set, then body_text_hash is checked
    # 
    # However, if body_params are ignored, then there may not be a body_param_hash
    # If there are ignored body_params, this means there are body_params
    # Then we should use body_params_hash over body_text_hash
    if len(body_params_hash) > 0 or len(hashed_request.ignored_body_params) > 0:
        query_params['body_params_hash'] = body_params_hash
    else:
        query_params['body_text_hash'] = body_text_hash

    return query_params

def __build_optional_params(request: MitmproxyRequest, options: EvalRequestOptions):
    optional_params = {}

    if options.get('retry'):
        optional_params['retry'] = options['retry']

        if options.get('infer'):
            optional_params['infer'] = options['infer']

    headers = request.headers
    if custom_headers.MOCK_REQUEST_ID in headers:
        optional_params['request_id'] = headers[custom_headers.MOCK_REQUEST_ID]

    return optional_params

def __filter_by_match_rules(request: MitmproxyRequest, match_rules: List[MatchRule], query_params: RequestResponseShowQueryParams):
    components = [request_component.BODY_PARAM, request_component.HEADER, request_component.QUERY_PARAM]
    method = request.method.upper()

    keep = {
        request_component.BODY_PARAM: False,
        request_component.HEADER: False,
        request_component.QUERY_PARAM: False,
    }

    match_rules = list(filter(lambda rule: method in rule.methods, match_rules))
    for match_rule in match_rules:
        pattern = match_rule.pattern

        if not __matches(request.url, pattern):
            continue

        if not isinstance(match_rule.components, list):
            continue
 
        for component in components:
            keep[component] = component in match_rule.components

    if not keep[request_component.HEADER]:
        if 'headers_hash' in query_params:
            del query_params['headers_hash']

    if not keep[request_component.QUERY_PARAM]:
        if 'query_params_hash' in query_params:
            del query_params['query_params_hash']

    if not keep[request_component.BODY_PARAM]:
        if 'body_params_hash' in query_params:
            del query_params['body_params_hash']

        if 'body_text_hash' in query_params:
            del query_params['body_text_hash']

def __matches(url: str, pattern: str):
    try:
        return re.match(pattern, url)
    except re.error as e:
        Logger.instance().error(f"RegExp error '{e}' for {pattern}")
        return False