import json
import requests
import sys
from typing import Dict

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
from stoobly_agent.lib.logger import bcolors

def import_endpoints(context: EndpointsImportContext):
    for endpoint in context.endpoints:
        for endpoint_handler in context.endpoint_handlers:
            endpoint_handler(endpoint)

        try:
            res = import_endpoint(context.project_id, context.resources['endpoint'], endpoint)
        except requests.HTTPError as e:
            error_handler(e, f"Failed to import endpoint: {endpoint['method']} {endpoint['path']}")
            return
        
        if res.status_code == 409: # Endpoint already created
            continue

        endpoint_id = res.json()['id']
        try:
            res = import_component_names(context.project_id, endpoint_id, endpoint, context.resources)
        except requests.HTTPError as e:
            error_handler(e, f"Failed to import endpoint: {endpoint['method']} {endpoint['path']}")

            try:
                cleanup_endpoint(context.project_id, endpoint_id, context.resources['endpoint'])
            except requests.HTTPError as e:
                error_handler(e, f"Failed to delete endpoint: {endpoint['method']} {endpoint['path']}, id {endpoint_id}")
            return

def import_endpoint(project_id: int, endpoint_resource: EndpointsResource, endpoint: EndpointShowResponse):
    res: requests.Response = endpoint_resource.create(**{
        'host': endpoint.get('host'),
        'method': endpoint.get('method'),
        'path_segments': json.dumps(endpoint.get('path_segment_names', [])),
        'path': endpoint.get('path'),
        'port': endpoint.get('port'),
        'project_id': project_id,
    })

    if res.ok or res.status_code == 409: # Endpoint already created
        return res
    
    res.raise_for_status()

def import_header_name(project_id: int, endpoint_id: int, header_name_resource: HeaderNamesResource, header_name: RequestComponentName): 
    res: requests.Response = header_name_resource.create(endpoint_id, {
        'name': header_name.get('name'),
        'is_deterministic': header_name.get('is_deterministic', True),
        'is_required': header_name.get('is_required', False),
        'endpoint_id': endpoint_id,
        'project_id': project_id,  
    })

    res.raise_for_status()

def import_body_param_name(project_id: int, endpoint_id: int, body_param_name_resource: BodyParamNamesResource, body_param_name: BodyParamName):
    res: requests.Response = body_param_name_resource.create(endpoint_id, {
        'name': body_param_name.get('name'),
        'is_deterministic': body_param_name.get('is_deterministic', True),
        'is_required': body_param_name.get('is_required', False),
        'inferred_type': body_param_name.get('inferred_type'),
        'query': body_param_name.get('query'),
        'endpoint_id': endpoint_id,
        'project_id': project_id,
    })

    res.raise_for_status()

def import_query_param_name(project_id: int, endpoint_id: int, query_param_name_resource: QueryParamNamesResource, query_param_name: RequestComponentName):
    res: requests.Response = query_param_name_resource.create(endpoint_id, {
        'name': query_param_name.get('name'),
        'is_deterministic': query_param_name.get('is_deterministic', True),
        'is_required': query_param_name.get('is_required', False),
        'endpoint_id': endpoint_id,
        'project_id': project_id,
    })

    res.raise_for_status()

def import_response_param_name(project_id: int, endpoint_id: int, response_param_name_resource: ResponseParamNamesResource, response_param_name: RequestComponentName):
    res: requests.Response = response_param_name_resource.create(endpoint_id, {
        'name': response_param_name.get('name'),
        'is_deterministic': response_param_name.get('is_deterministic', True),
        'is_required': response_param_name.get('is_required', False),
        'inferred_type': response_param_name.get('inferred_type'),
        'query': response_param_name.get('query'),
        'endpoint_id': endpoint_id,
        'project_id': project_id,
    })

    res.raise_for_status()

def import_response_header_name(project_id: int, endpoint_id: int, response_header_name_resource: ResponseHeaderNamesResource, response_header_name: RequestComponentName):
    res: requests.Response = response_header_name_resource.create(endpoint_id, {
        'name': response_header_name.get('name'),
        'is_deterministic': response_header_name.get('is_deterministic', True),
        'is_required': response_header_name.get('is_required', False),
        'endpoint_id': endpoint_id,
        'project_id': project_id,  
    })

    res.raise_for_status()

component_name_import_dispatch = {
    ENDPOINT_COMPONENT_NAMES[0]: import_header_name,
    ENDPOINT_COMPONENT_NAMES[1]: import_body_param_name,
    ENDPOINT_COMPONENT_NAMES[2]: import_query_param_name,
    ENDPOINT_COMPONENT_NAMES[3]: import_response_header_name,
    ENDPOINT_COMPONENT_NAMES[4]: import_response_param_name
}

def process_import(component_name: str, *args):
    return component_name_import_dispatch[component_name](*args)

def import_component_names(project_id: int, endpoint_id: int, endpoint: EndpointShowResponse, resources: Dict[str, EndpointsResource]):
    for component_name in ENDPOINT_COMPONENT_NAMES:
        for component in endpoint.get(f'{component_name}s', {}):
            resource = resources[component_name]
            process_import(component_name, project_id, endpoint_id, resource, component)

def cleanup_endpoint(project_id: int, endpoint_id: int, resource: EndpointsResource):
    print(f"{bcolors.OKBLUE}Cleaning up partial import...{bcolors.ENDC}")
    res: requests.Response = resource.destroy(endpoint_id, **{
        'project_id': project_id
    })

    res.raise_for_status()

def error_handler(error: requests.HTTPError, message = ''):
    if message:
        print(
            f"{bcolors.FAIL}{message}{bcolors.ENDC}",
            file=sys.stderr
        )

    print(error.response.text, file=sys.stderr)
    print(f"Error {error.response.status_code} {error.response.reason}", file=sys.stderr)