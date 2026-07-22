from typing import Literal

DEVELOP = 'develop'
MOCK = 'mock'
NONE = 'none'
RECORD = 'record'
TEST = 'test'

options = [DEVELOP, MOCK, RECORD, TEST]

AgentMode = Literal[DEVELOP, MOCK, NONE, RECORD, TEST]
