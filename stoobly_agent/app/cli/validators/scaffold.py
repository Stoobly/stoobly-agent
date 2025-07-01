import re
import sys

from stoobly_agent.app.cli.scaffold.templates.constants import CORE_SERVICES

def validate_app_name(ctx, param, app_name: str) -> str:
  app_name_regex = re.compile(r'^[a-zA-Z0-9._-]+$')
  if not re.search(app_name_regex, app_name):
    print(f"Error: app name {app_name} is invalid.", file=sys.stderr)
    sys.exit(1)
  return app_name

def validate_hostname(ctx, param, hostname: str) -> str:
  if not hostname:
    return
  hostname_regex = re.compile(r'^[a-zA-Z0-9.-]+$')
  if not re.search(hostname_regex, hostname):
    print(f"Error: hostname {hostname} is invalid.", file=sys.stderr)
    sys.exit(1)
  return hostname

def validate_namespace(ctx, param, namespace: str) -> str:
  if not namespace:
    return
  namespace_regex = re.compile(r'^[a-z0-9_-]+$')
  if not re.search(namespace_regex, namespace) or namespace[0] in ['-', '_']:
    print(f"Error: namespace {namespace} is invalid.", file=sys.stderr)
    sys.exit(1)
  return namespace

def validate_service_name(ctx, param, service_name: str) -> str:
  if service_name in CORE_SERVICES:
    print(f"Error: {service_name} is a core service", file=sys.stderr)
    sys.exit(1)
  service_name_regex = re.compile(r'^[a-zA-Z0-9._-]+$')
  if not re.search(service_name_regex, service_name):
    print(f"Error: service name {service_name} is invalid.", file=sys.stderr)
    sys.exit(1)
  return service_name
