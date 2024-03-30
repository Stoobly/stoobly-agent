import json
import requests
from typing import TypedDict

from .endpoints_import_context import EndpointsImportContext
from stoobly_agent.app.models.types import ENDPOINT_COMPONENT_NAMES
from stoobly_agent.lib.api.body_param_names_resource import BodyParamNamesResource
from stoobly_agent.lib.api.endpoints_resource import EndpointsResource
from stoobly_agent.lib.api.header_names_resource import HeaderNamesResource
from stoobly_agent.lib.api.interfaces.endpoints import BodyParamName
from stoobly_agent.lib.api.interfaces.endpoints import EndpointShowResponse
from stoobly_agent.lib.api.interfaces.endpoints import RequestComponentName
from stoobly_agent.lib.api.query_param_names_resource import QueryParamNamesResource
from stoobly_agent.lib.api.response_header_names_resource import ResponseHeaderNamesResource
from stoobly_agent.lib.api.response_param_names_resource import ResponseParamNamesResource

class PendingImportArgs(TypedDict):
    project_id: int
    endpoint_id: int
    component_name: str
    component: RequestComponentName
    component_resource_class: EndpointsResource

def import_endpoints(context: EndpointsImportContext):
    uploaded_endpoints = []
    for endpoint in context.endpoints:
        for endpoint_handler in context.endpoint_handlers:
            endpoint_handler(endpoint)

        res = import_endpoint_and_component_name(context, endpoint, uploaded_endpoints)
        if not res.ok:
            for error_handler in context.error_handlers:
                error_handler(endpoint)
            cleanup_endpoints(context.project_id, context.resources['endpoint'], uploaded_endpoints)
            raise AssertionError(res.content)


def import_endpoint(project_id: int, endpoint_resource: EndpointsResource, endpoint: EndpointShowResponse):
    res: requests.Response = endpoint_resource.create(**{
        'host': endpoint.get('host'),
        'method': endpoint.get('method'),
        'path_segments': json.dumps(endpoint.get('path_segment_names', [])),
        'path': endpoint.get('path'),
        'port': endpoint.get('port'),
        'project_id': project_id,
    })
    
    return res

def import_header_name(project_id: int, endpoint_id: int, header_name_resource: HeaderNamesResource, header_name: RequestComponentName): 
    res: requests.Response = header_name_resource.create(**{
        'name': header_name.get('name'),
        'is_deterministic': header_name.get('is_deterministic', True),
        'is_required': header_name.get('is_required', False),
        'endpoint_id': endpoint_id,
        'project_id': project_id,  
    })

    return res

def import_body_param_name(project_id: int, endpoint_id: int, body_param_name_resource: BodyParamNamesResource, body_param_name: BodyParamName):
    res: requests.Response = body_param_name_resource.create(**{
        'name': body_param_name.get('name'),
        'is_deterministic': body_param_name.get('is_deterministic', True),
        'is_required': body_param_name.get('is_required', False),
        'inferred_type': body_param_name.get('inferred_type'),
        'query': body_param_name.get('query'),
        'endpoint_id': endpoint_id,
        'project_id': project_id,
    })

    return res

def import_query_param_name(project_id: int, endpoint_id: int, query_param_name_resource: QueryParamNamesResource, query_param_name: RequestComponentName):
    res: requests.Response = query_param_name_resource.create(**{
        'name': query_param_name.get('name'),
        'is_deterministic': query_param_name.get('is_deterministic', True),
        'is_required': query_param_name.get('is_required', False),
        'endpoint_id': endpoint_id,
        'project_id': project_id,
    })

    return res

def import_response_param_name(project_id: int, endpoint_id: int, response_param_name_resource: ResponseParamNamesResource, response_param_name: RequestComponentName):
    res: requests.Response = response_param_name_resource.create(**{
        'name': response_param_name.get('name'),
        'is_deterministic': response_param_name.get('is_deterministic', True),
        'is_required': response_param_name.get('is_required', False),
        'inferred_type': response_param_name.get('inferred_type'),
        'query': response_param_name.get('query'),
        'endpoint_id': endpoint_id,
        'project_id': project_id,
    })

    return res

def import_response_header_name(project_id: int, endpoint_id: int, response_header_name_resource: ResponseHeaderNamesResource, response_header_name: RequestComponentName):
    res: requests.Response = response_header_name_resource.create(**{
        'name': response_header_name.get('name'),
        'is_deterministic': response_header_name.get('is_deterministic', True),
        'is_required': response_header_name.get('is_required', False),
        'endpoint_id': endpoint_id,
        'project_id': project_id,  
    })

    return res

component_name_import_dispatch = {
    'header_name': import_header_name,
    'body_param_name': import_body_param_name,
    'query_param_name': import_query_param_name,
    'response_param_name': import_response_param_name,
    'response_header_name': import_response_header_name
}

def process_import(args: PendingImportArgs):
    return component_name_import_dispatch[args['component_name']](args['project_id'], args['endpoint_id'], args['component_resource_class'], args['component'])

def import_endpoint_and_component_name(context: EndpointsImportContext, endpoint: EndpointShowResponse, uploaded_endpoints):
    res = import_endpoint(context.project_id, context.resources['endpoint'], endpoint)

    if not res.ok:
        return res

    endpoint_id = res.json()['id']
    uploaded_endpoints.append(endpoint_id)
    import_queue = []
    for component_name in ENDPOINT_COMPONENT_NAMES:
        for component in endpoint.get(f'{component_name}s', {}):
            resource = context.resources[component_name]
            pending_import: PendingImportArgs = {
                'project_id': context.project_id,
                'endpoint_id': endpoint_id,
                'component_name': component_name,
                'component': component,
                'component_resource_class': resource
            }
            import_queue.append(pending_import)
    
    while res.ok and len(import_queue) > 0:
        pending_import = import_queue.pop()
        res = process_import(pending_import)
    
    return res

def cleanup_endpoints(project_id: int, resource: EndpointsResource, uploaded_endpoints):
    for endpoint_id in uploaded_endpoints:
        res: requests.Response = resource.destroy(endpoint_id, **{
            'project_id': project_id
        })

        res.raise_for_status()