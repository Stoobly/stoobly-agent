from typing import Literal

MOCK = 'mock'
NONE = 'none'
NORMALIZE = 'normalize'
RECORD = 'record'
TEST = 'test'

options = [MOCK, NORMALIZE, RECORD, TEST]

AgentMode = Literal[MOCK, NONE, NORMALIZE, RECORD, TEST]