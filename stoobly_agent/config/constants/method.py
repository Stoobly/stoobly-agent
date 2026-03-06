from typing import Literal

GET = 'GET'
PATCH = 'PATCH'
POST = 'POST'
PUT = 'PUT'
DELETE = 'DELETE'
OPTIONS = 'OPTIONS'

Method = Literal[GET, PATCH, POST, PUT, DELETE, OPTIONS]