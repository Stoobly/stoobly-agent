import sys

from .tabulate_print_service import tabulate_print

def select_print_options(kwargs):
    print_options = {
        'select': kwargs['select'],
        'without_headers': kwargs['without_headers']
    }

    del kwargs['without_headers']
    del kwargs['select']

    return print_options

def print_projects(projects, **kwargs):
    tabulate_print(
        projects, 
        filter=['created_at', 'is_deleted', 'organization_id', 'project_id', 'starred', 'updated_at'],
        headers=not kwargs.get('without_headers'),
        select=kwargs.get('select') or []
    )

def print_requests(requests, **kwargs):
    tabulate_print(
      requests, 
      filter=[
        'body_params_hash', 'body_text_hash', 'components' , 'created_at', 'endpoint', 'endpoint_id', 'http_version', 'is_deleted', 'position', 'project_id', 'pushed_at', 'query_params_hash', 'scenario_id', 'scheme', 'starred', 'uuid', 'updated_at', 'url'
      ],
      headers=not kwargs.get('without_headers'),
      select=kwargs.get('select') or []
    )

def print_scenarios(scenarios, **kwargs):
    tabulate_print(
        scenarios, 
        filter=['created_at', 'is_deleted', 'priority', 'project_id', 'starred', 'uuid', 'updated_at'],
        headers=not kwargs.get('without_headers'),
        select=kwargs.get('select') or []
    )

def print_tests(requests, **kwargs):
    tabulate_print(
      requests, 
      filter=['created_at', 'id', 'log', 'position', 'project_id', 'report_id', 'scenario_id', 'starred', 'updated_at'],
      headers=not kwargs.get('without_headers'),
      select=kwargs.get('select') or []
    )