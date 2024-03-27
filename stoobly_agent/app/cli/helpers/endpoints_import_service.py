import requests
import json

from stoobly_agent.lib.api.interfaces.endpoints import EndpointShowResponse
from stoobly_agent.lib.api.interfaces.endpoints import RequestComponentName
from stoobly_agent.lib.api.interfaces.endpoints import BodyParamName
from stoobly_agent.lib.api.endpoints_resource import EndpointsResource

from .endpoints_import_context import EndpointsImportContext

def import_all_endpoints(context: EndpointsImportContext):
    for endpoint in context.endpoints:
        for endpoint_handler in context.endpoint_handlers:
            endpoint_handler(endpoint)

        import_endpoint_and_component_name_resources(context, endpoint)

def import_endpoint_and_component_name_resources(context: EndpointsImportContext, endpoint: EndpointShowResponse):
    res = import_endpoint(context, endpoint)

    endpoint_id = res['id']
    if endpoint.get('header_names'):
        for header_name in endpoint['header_names']:
            import_header_name(context, endpoint_id, header_name)
    
    if endpoint.get('body_param_names'):
        for body_param_name in endpoint['body_param_names']:
            import_body_param_name(context, endpoint_id, body_param_name)

    if endpoint.get('query_param_names'):
        for query_param_name in endpoint['query_param_names']:
            import_query_param_name(context, endpoint_id, query_param_name)
    
    if endpoint.get('response_param_names'):
        for response_param_name in endpoint['response_param_names']:
            import_response_param_name(context, endpoint_id, response_param_name)

    if endpoint.get('response_header_names'):
        for response_header_name in endpoint['response_header_names']:
            import_response_header_name(context, endpoint_id, response_header_name)
    
def import_endpoint(context: EndpointsImportContext, endpoint: EndpointShowResponse):
    res: requests.Response = context.endpoint_resource.create(**{
        'host': endpoint.get('host'),
        'method': endpoint.get('method'),
        'path_segments': json.dumps(endpoint.get('path_segment_names', [])),
        'path': endpoint.get('path'),
        'port': endpoint.get('port'),
        'project_id': context.project_id,
    })

    res.raise_for_status()
    
    return res.json()

def import_header_name(context: EndpointsImportContext, endpoint_id: int, header_name: RequestComponentName): 
    res: requests.Response = context.header_name_resource.create(**{
        'name': header_name.get('name'),
        'is_deterministic': header_name.get('is_deterministic', True),
        'is_required': header_name.get('is_required', False),
        'endpoint_id': endpoint_id,
        'project_id': context.project_id,  
    })

    res.raise_for_status()

    return res.json()

def import_body_param_name(context: EndpointsImportContext, endpoint_id: int,  body_param_name: BodyParamName):
    res: requests.Response = context.body_param_name_resource.create(**{
        'name': body_param_name.get('name'),
        'is_deterministic': body_param_name.get('is_deterministic', True),
        'is_required': body_param_name.get('is_required', False),
        'inferred_type': body_param_name.get('inferred_type'),
        'query': body_param_name.get('query'),
        'endpoint_id': endpoint_id,
        'project_id': context.project_id,
    })

    res.raise_for_status()

    return res.json()

def import_query_param_name(context: EndpointsImportContext, endpoint_id: int, query_param_name: RequestComponentName):
    res: requests.Response = context.query_param_name_resource.create(**{
        'name': query_param_name.get('name'),
        'is_deterministic': query_param_name.get('is_deterministic', True),
        'is_required': query_param_name.get('is_required', False),
        'endpoint_id': endpoint_id,
        'project_id': context.project_id,
    })

    res.raise_for_status()

    return res.json()

def import_response_param_name(context: EndpointsImportContext, endpoint_id: int, response_param_name: RequestComponentName):
    res: requests.Response = context.response_param_name_resource.create(**{
        'name': response_param_name.get('name'),
        'is_deterministic': response_param_name.get('is_deterministic', True),
        'is_required': response_param_name.get('is_required', False),
        'inferred_type': response_param_name.get('inferred_type'),
        'query': response_param_name.get('query'),
        'endpoint_id': endpoint_id,
        'project_id': context.project_id,
    })

    res.raise_for_status()

    return res.json()

def import_response_header_name(context: EndpointsImportContext, endpoint_id: int, response_header_name: RequestComponentName):
    res: requests.Response = context.response_header_name_resource.create(**{
        'name': response_header_name.get('name'),
        'is_deterministic': response_header_name.get('is_deterministic', True),
        'is_required': response_header_name.get('is_required', False),
        'endpoint_id': endpoint_id,
        'project_id': context.project_id,  
    })

    res.raise_for_status()

    return res.json()