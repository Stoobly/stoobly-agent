import re

def allowed_request(active_mode_settings, request):
    exclude_patterns = active_mode_settings.get('exclude_patterns')

    if exclude_patterns:
        if __exclude(request,  exclude_patterns):
            return False

    # If an include pattern is set, then that means only requests
    # matching these pattern(s) are allowed
    include_patterns = active_mode_settings.get('include_patterns')
    if include_patterns:
        if not __include(request, include_patterns):
            return False

    # If there are no exclude or include patterns, request is allowed
    return True

###
#
# @param patterns [Array<string>]
#
def __include(request, patterns):
    if not patterns:
        return True

    if len(patterns) == 0:
        return True

    for pattern in patterns:
        if re.match(pattern, request.url):
            return True

    return False

def __exclude(request, patterns):
    if not patterns:
        return False

    for pattern in patterns:
        if re.match(pattern, request.url):
            return True

    return False
