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
        filter=['created_at', 'organization_id', 'project_id', 'starred', 'updated_at'],
        headers=not kwargs.get('without_headers'),
        select=kwargs.get('select') or []
    )

def print_requests(requests, **kwargs):
    tabulate_print(
      requests, 
      filter=['components' , 'created_at', 'endpoint', 'endpoint_id', 'id', 'position', 'project_id', 'scenario_id', 'scheme', 'starred', 'updated_at', 'url'],
      headers=not kwargs.get('without_headers'),
      select=kwargs.get('select') or []
    )

def print_scenarios(scenarios, **kwargs):
    tabulate_print(
        scenarios, 
        filter=['created_at', 'priority', 'project_id', 'starred', 'updated_at'],
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