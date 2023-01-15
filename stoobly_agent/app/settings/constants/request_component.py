from typing import Literal

HEADER = 'Header'
BODY_PARAM = 'Body Param'
QUERY_PARAM = 'Query Param'

RequestComponent = Literal[BODY_PARAM, HEADER, QUERY_PARAM]