from .json_print import json_print
from .tabulate_print_service import tabulate_print
from ..types.print_options import TabulatePrintOptions

JSON_FORMAT = 'json'
SIMPLE_FORMAT = 'simple'
FORMATS = [JSON_FORMAT, SIMPLE_FORMAT]

def select_print_options(kwargs: TabulatePrintOptions):
    print_options = {
        'format': kwargs['format'],
        'select': kwargs['select'],
        'without_headers': kwargs['without_headers']
    }

    del kwargs['format']
    del kwargs['select']
    del kwargs['without_headers']

    return print_options

def print_projects(projects, **kwargs: TabulatePrintOptions):
    filter = ['created_at', 'is_deleted', 'organization_id', 'project_id', 'starred', 'updated_at']
    format = kwargs.get('format')

    if format == JSON_FORMAT:
        json_print(projects, **{
            'filter': filter,
            **kwargs
        })
    else:
        tabulate_print(
            projects, 
            filter=filter,
            headers=not kwargs.get('without_headers'),
            select=kwargs.get('select') or []
        )

def print_reports(reports, **kwargs: TabulatePrintOptions):
    filter = ['created_at', 'priority', 'user_id', 'starred', 'updated_at']
    format = kwargs.get('format')

    if format == JSON_FORMAT:
        json_print(reports, **{
            'filter': filter,
            **kwargs
        })
    else:
        tabulate_print(
            reports, 
            filter=filter,
            headers=not kwargs.get('without_headers'),
            select=kwargs.get('select') or []
        )

def print_requests(requests, **kwargs: TabulatePrintOptions):
    filter = [
        'body_params_hash', 'body_text_hash', 'components' , 'created_at', 'endpoint', 'endpoint_id', 'http_version', 'is_deleted', 'position', 'project_id', 'pushed_at', 'query_params_hash', 'scenario_id', 'scheme', 'starred', 'uuid', 'updated_at', 'url'
    ]
    format = kwargs.get('format')

    if format == JSON_FORMAT:
        json_print(requests, **{
            'filter': filter,
            **kwargs
        })
    else:
        tabulate_print(
            requests, 
            filter=filter,
            headers=not kwargs.get('without_headers'),
            select=kwargs.get('select') or []
        )

def print_scenarios(scenarios, **kwargs: TabulatePrintOptions):
    filter = ['created_at', 'is_deleted', 'priority', 'project_id', 'starred', 'uuid', 'updated_at']
    format = kwargs.get('format')

    if format == JSON_FORMAT:
        json_print(scenarios, **{
            'filter': filter,
            **kwargs
        })
    else:
        tabulate_print(
            scenarios, 
            filter=filter,
            headers=not kwargs.get('without_headers'),
            select=kwargs.get('select') or []
        )

def print_services(services, **kwargs: TabulatePrintOptions):
    filter = []
    format = kwargs.get('format')

    if format == JSON_FORMAT:
        json_print(services, **{
            'filter': filter,
            **kwargs
        })
    else:
        tabulate_print(
            services, 
            filter=filter,
            headers=not kwargs.get('without_headers'),
            select=kwargs.get('select') or []
        )

def print_snapshots(snapshots, **kwargs: TabulatePrintOptions):
    filter = ['resource_uuid']
    format = kwargs.get('format')

    if format == JSON_FORMAT:
        json_print(snapshots, **{
            'filter': filter,
            **kwargs
        })
    else:
        tabulate_print(
            snapshots,
            filter=filter,
            headers=not kwargs.get('without_headers'),
            select=kwargs.get('select') or []
        )

def print_tests(tests, **kwargs: TabulatePrintOptions):
    filter = ['created_at', 'id', 'log', 'position', 'project_id', 'report_id', 'scenario_id', 'starred', 'updated_at']
    format = kwargs.get('format')

    if format == JSON_FORMAT:
        json_print(tests, **{
            'filter': filter,
            **kwargs
        })
    else:
        tabulate_print(
            tests, 
            filter=filter,
            headers=not kwargs.get('without_headers'),
            select=kwargs.get('select') or []
        )

def print_traces(traces, **kwargs: TabulatePrintOptions):
    filter = kwargs.get('filter') or []
    format = kwargs.get('format')

    if format == JSON_FORMAT:
        json_print(traces, **{
            'filter': filter,
            **kwargs
        })
    else:
        tabulate_print(
        traces, 
        filter=filter,
        headers=not kwargs.get('without_headers'),
        select=kwargs.get('select') or []
        )