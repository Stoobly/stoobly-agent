import json
import requests
import sys
from typing import Dict, TypedDict, Optional

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

class ComponentImportArgs(TypedDict):
    project_id: int
    endpoint_id: int
    resource: EndpointsResource
    component: RequestComponentName
    parents: Optional[Dict]

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

def import_header_name(args: ComponentImportArgs):
    project_id = args['project_id']
    endpoint_id = args['endpoint_id']
    header_name_resource = args['resource']
    header_name = args['component']

    res: requests.Response = header_name_resource.create(endpoint_id, {
        'name': header_name.get('name'),
        'is_deterministic': header_name.get('is_deterministic', True),
        'is_required': header_name.get('is_required', False),
        'endpoint_id': endpoint_id,
        'project_id': project_id,  
    })

    res.raise_for_status()

def import_body_param_name(args: ComponentImportArgs):
    project_id = args['project_id']
    endpoint_id = args['endpoint_id']
    body_param_name_resource = args['resource']
    body_param_name = args['component']
    parents = args['parents']

    body_param_name_id = None
    parent_id = body_param_name.get('body_param_name_id')
    if parent_id:
        body_param_name_id = parents[parent_id]
    
    res: requests.Response = body_param_name_resource.create(endpoint_id, {
        'name': body_param_name.get('name'),
        'is_deterministic': body_param_name.get('is_deterministic', True),
        'is_required': body_param_name.get('is_required', False),
        'inferred_type': body_param_name.get('inferred_type'),
        'query': body_param_name.get('query'),
        'endpoint_id': endpoint_id,
        'project_id': project_id,
        'body_param_name_id': body_param_name_id
    })

    res.raise_for_status()

    res_id = res.json()['id']
    parents[body_param_name['id']] = res_id

def import_query_param_name(args: ComponentImportArgs):
    project_id = args['project_id']
    endpoint_id = args['endpoint_id']
    query_param_name_resource = args['resource']
    query_param_name = args['component']

    res: requests.Response = query_param_name_resource.create(endpoint_id, {
        'name': query_param_name.get('name'),
        'is_deterministic': query_param_name.get('is_deterministic', True),
        'is_required': query_param_name.get('is_required', False),
        'endpoint_id': endpoint_id,
        'project_id': project_id,
    })

    res.raise_for_status()

def import_response_param_name(args: ComponentImportArgs):
    project_id = args['project_id']
    endpoint_id = args['endpoint_id']
    response_param_name_resource = args['resource']
    response_param_name = args['component']
    parents = args['parents']

    response_param_name_id = None
    parent_id = response_param_name.get('response_param_name_id')
    if parent_id:
        response_param_name_id = parents[parent_id]
    
    res: requests.Response = response_param_name_resource.create(endpoint_id, {
        'name': response_param_name.get('name'),
        'is_deterministic': response_param_name.get('is_deterministic', True),
        'is_required': response_param_name.get('is_required', False),
        'inferred_type': response_param_name.get('inferred_type'),
        'query': response_param_name.get('query'),
        'endpoint_id': endpoint_id,
        'project_id': project_id,
        'response_param_name_id': response_param_name_id
    })

    res.raise_for_status()

    res_id = res.json()['id']
    parents[response_param_name['id']] = res_id


def import_response_header_name(args: ComponentImportArgs):
    project_id = args['project_id']
    endpoint_id = args['endpoint_id']
    response_header_name_resource = args['resource']
    response_header_name = args['component']

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

def import_component_names(project_id: int, endpoint_id: int, endpoint: EndpointShowResponse, resources: Dict[str, EndpointsResource]):
    for component_name in ENDPOINT_COMPONENT_NAMES:
        parents: Dict[int, int] = {}
        for component in endpoint.get(f'{component_name}s', {}):
            resource = resources[component_name]
            args = {
                'project_id': project_id,
                'endpoint_id': endpoint_id,
                'resource': resource,
                'component': component,
                'parents': parents
            }
            component_name_import_dispatch[component_name](args)
            

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