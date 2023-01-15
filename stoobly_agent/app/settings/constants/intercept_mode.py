from typing import Literal

MOCK = 'mock'
RECORD = 'record'
REPLAY = 'replay'
TEST = 'test'

Mode = Literal[MOCK, RECORD, TEST]