import re
import sys
from typing import Optional

from stoobly_agent.app.cli.scaffold.templates.constants import CORE_SERVICES

def validate_app_name(ctx, param, app_name: str) -> str:
  app_name_regex = re.compile(r'^[a-zA-Z0-9._-]+$')
  if not re.search(app_name_regex, app_name):
    print(f"Error: app name {app_name} is invalid.", file=sys.stderr)
    sys.exit(1)
  return app_name

def validate_hostname(ctx, param, hostname: str) -> Optional[str]:
  if not hostname:
    return None
  hostname_regex = re.compile(r'^[a-zA-Z0-9.-]+$')
  if not re.search(hostname_regex, hostname):
    print(f"Error: hostname {hostname} is invalid.", file=sys.stderr)
    sys.exit(1)
  return hostname

def validate_network(ctx, param, network: str) -> Optional[str]:
  if not network:
    return None
  network_regex = re.compile(r'^[a-zA-Z0-9._-]+$')
  if not re.search(network_regex, network):
    print(f"Error: network {network} is invalid.", file=sys.stderr)
    sys.exit(1)
  return network

def validate_namespace(ctx, param, namespace: str) -> Optional[str]:
  if not namespace:
    return None
  namespace_regex = re.compile(r'^[a-z0-9_-]+$')
  if not re.search(namespace_regex, namespace) or namespace[0] in ['-', '_']:
    print(f"Error: namespace {namespace} is invalid.", file=sys.stderr)
    sys.exit(1)
  return namespace

def validate_service_name(ctx, param, service_name: str) -> Optional[str]:
  if not service_name:
    return None
  if service_name in CORE_SERVICES:
    print(f"Error: {service_name} is a core service", file=sys.stderr)
    sys.exit(1)
  service_name_regex = re.compile(r'^[a-zA-Z0-9._-]+$')
  if not re.search(service_name_regex, service_name):
    print(f"Error: service name {service_name} is invalid.", file=sys.stderr)
    sys.exit(1)
  return service_name
