from typing import Literal

HEADER = 'Header'
BODY_PARAM = 'Body Param'
QUERY_PARAM = 'Query Param'
RESPONSE_HEADER = 'Response Header'
RESPONSE_PARAM = 'Response Param'

REQUEST_COMPONENTS = [BODY_PARAM, HEADER, QUERY_PARAM]
RESPONSE_COMPONENTS = [RESPONSE_HEADER, RESPONSE_PARAM]

RequestComponent = Literal[BODY_PARAM, HEADER, QUERY_PARAM, RESPONSE_HEADER, RESPONSE_PARAM]