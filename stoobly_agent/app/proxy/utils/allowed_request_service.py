import pdb
import re

from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from mitmproxy.http import Request as MitmproxyRequest

from stoobly_agent.app.proxy.intercept_settings import InterceptSettings
from stoobly_agent.app.settings.constants import intercept_mode
from stoobly_agent.app.settings.firewall_rule import FirewallRule
from stoobly_agent.config.constants import mode, intercept_policy, request_origin
from stoobly_agent.lib.logger import bcolors, Logger

LOG_ID = 'Firewall'

def get_active_mode_policy(request: 'MitmproxyRequest', intercept_settings: InterceptSettings, mode = None) -> str:
    if intercept_settings.request_origin == request_origin.CLI:
        return intercept_settings.policy 

    if allowed_request(request, intercept_settings, mode):
        return intercept_settings.policy
    else:
        # If the request path does not match accepted paths, do not intercept
        return intercept_policy.NONE

def allowed_request(request: 'MitmproxyRequest', intercept_settings: InterceptSettings, mode = None) -> bool:
    mode = mode or intercept_settings.mode

    exclude_rules = intercept_settings.exclude_rules_for_mode(mode)

    # If an exclude rule(s) exists, then only requests not matching these pattern(s) are allowed
    if __request_excluded(request, exclude_rules, mode):
        return False

    include_rules = intercept_settings.include_rules_for_mode(mode)

    # If an include rule(s) exists, then only requests matching these pattern(s) are allowed
    if not __request_included(request, include_rules, mode):
        return False

    # If there are no exclude or include patterns, request is allowed
    return True

def __request_excluded(request: 'MitmproxyRequest', exclude_rules: List[FirewallRule], mode: str):
    if exclude_rules:
        method = request.method.upper()
        rules = list(filter(lambda rule: method in rule.methods, exclude_rules))
        patterns = list(map(lambda rule: rule.pattern, rules))
        if __exclude(request, patterns):
            Logger.instance(LOG_ID).info(f"{bcolors.OKCYAN}Ignore (exclude) handling {mode}{bcolors.ENDC} {request.url}")
            return True
    
    return False

def __request_included(request: 'MitmproxyRequest', include_rules: List[FirewallRule], mode: str):
    if not include_rules:
        return True

    method = request.method.upper()
    rules = list(filter(lambda rule: method in rule.methods, include_rules))

    # If there are include rules, but none that match the request's method,
    # then we know that none of the include rules will match the request
    if len(include_rules) > 0 and len(rules) == 0:
        Logger.instance(LOG_ID).info(f"{bcolors.OKCYAN}Ignore (not include) handling {mode}{bcolors.ENDC} {request.url}")
        return False

    patterns = list(map(lambda rule: rule.pattern, rules))
    if not __include(request, patterns):
        Logger.instance(LOG_ID).info(f"{bcolors.OKCYAN}Ignore (not include) handling {mode}{bcolors.ENDC} {request.url}")
        return False

    return True

###
#
# @param patterns [Array<string>]
#
def __include(request: 'MitmproxyRequest', patterns: List[str]) -> bool:
    if not patterns:
        return True

    if len(patterns) == 0:
        return True

    for pattern in patterns:
        try:
            if re.fullmatch(pattern, request.url):
                return True
        except re.error as e:
            Logger.instance(LOG_ID).error(f"RegExp error '{e}' for {pattern}")
            return False

    return False

def __exclude(request: 'MitmproxyRequest', patterns: List[str]) -> bool:
    if not patterns:
        return False

    for pattern in patterns:
        try:
            if re.fullmatch(pattern, request.url):
                return True
        except re.error as e:
            Logger.instance(LOG_ID).error(f"RegExp error '{e}' for {pattern}")
            return True

    return False
