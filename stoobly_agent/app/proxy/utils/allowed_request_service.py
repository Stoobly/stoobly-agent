import pdb
import re

from mitmproxy.http import Request as MitmproxyRequest
from typing import List

from stoobly_agent.app.proxy.intercept_settings import InterceptSettings
from stoobly_agent.config.constants import mock_policy, request_origin
from stoobly_agent.lib.logger import bcolors, Logger

def get_active_mode_policy(request: MitmproxyRequest, intercept_settings: InterceptSettings):
    if intercept_settings.request_origin == request_origin.CLI:
        return intercept_settings.policy 

    if intercept_settings.active and allowed_request(request, intercept_settings):
        return intercept_settings.policy
    else:
        # If the request path does not match accepted paths, do not mock
        return mock_policy.NONE

def allowed_request(request: MitmproxyRequest, intercept_settings: InterceptSettings) -> bool:
    # If an exclude rule(s) exists, then only requests not matching these pattern(s) are allowed
    exclude_rules = intercept_settings.exclude_rules
    if exclude_rules:
        method = request.method.upper()
        rules = list(filter(lambda rule: method in rule.methods, exclude_rules))
        patterns = list(map(lambda rule: rule.pattern, rules))
        if __exclude(request, patterns):
            Logger.instance().info(f"{bcolors.OKBLUE}Excluded by firewall rule{bcolors.ENDC}")
            return False

    # If an include rule(s) exists, then only requests matching these pattern(s) are allowed
    include_rules = intercept_settings.include_rules
    if include_rules:
        method = request.method.upper()
        rules = list(filter(lambda rule: method in rule.methods, include_rules))
        patterns = list(map(lambda rule: rule.pattern, rules))
        if not __include(request, patterns):
            Logger.instance().info(f"{bcolors.OKBLUE}Not included by firewall rule{bcolors.ENDC}")
            return False

    # If there are no exclude or include patterns, request is allowed
    return True

###
#
# @param patterns [Array<string>]
#
def __include(request: MitmproxyRequest, patterns: List[str]) -> bool:
    if not patterns:
        return True

    if len(patterns) == 0:
        return True

    for pattern in patterns:
        try:
            if re.match(pattern, request.url):
                return True
        except re.error as e:
            Logger.instance().error(f"RegExp error '{e}' for {pattern}")
            return False

    return False

def __exclude(request: MitmproxyRequest, patterns: List[str]) -> bool:
    if not patterns:
        return False

    for pattern in patterns:
        try:
            if re.match(pattern, request.url):
                return True
        except re.error as e:
            Logger.instance().error(f"RegExp error '{e}' for {pattern}")
            return True

    return False
