from typing import Final, Literal

MOCK: Final = 'mock'
RECORD: Final = 'record'
REPLAY: Final = 'replay'
TEST: Final = 'test'

Mode = Literal[MOCK, RECORD, REPLAY, TEST]