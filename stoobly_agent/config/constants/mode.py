from typing import Literal

MOCK = 'mock'
NONE = 'none'
RECORD = 'record'
REPLAY = 'replay'
TEST = 'test'

AgentMode = Literal[MOCK, NONE, RECORD, REPLAY, TEST]