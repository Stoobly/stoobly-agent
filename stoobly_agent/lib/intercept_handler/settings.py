from .custom_headers import CUSTOM_HEADERS

def get_proxy_mode(headers, settings):
    access_control_header =  'Access-Control-Request-Headers'
    do_proxy_header = CUSTOM_HEADERS['DO_PROXY']

    if access_control_header in headers and do_proxy_header.lower() in headers[access_control_header]:
        return MODE['NONE']
    elif do_proxy_header in headers:
        return MODE['NONE']
    elif CUSTOM_HEADERS['PROXY_MODE'] in headers:
        return headers[CUSTOM_HEADERS['PROXY_MODE']]
    else:
        return settings.active_mode

def get_mock_policy(headers, settings):
    if CUSTOM_HEADERS['MOCK_POLICY'] in headers:
        return headers[CUSTOM_HEADERS['MOCK_POLICY']]
    else:
        return settings.get('policy')

def get_record_policy(headers, settings):
    if CUSTOM_HEADERS['RECORD_POLICY'] in headers:
        return headers[CUSTOM_HEADERS['RECORD_POLICY']]
    else:
        return settings.get('policy')

def get_service_url(request, settings):
    service_url = request.headers.get(CUSTOM_HEADERS['SERVICE_URL'])

    if service_url:
        return service_url
    else:
        if settings.get('service_url') and len(settings.get('service_url')) > 0:
            return settings.get('service_url')

        return __upstream_url(request)

def __upstream_url(request):
    return f"{request.scheme}://{request.host}:{request.port}"
