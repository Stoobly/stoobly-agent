from typing import Final, Literal

DEVELOP: Final = 'develop'
MOCK: Final = 'mock'
RECORD: Final = 'record'
TEST: Final = 'test'

Mode = Literal[DEVELOP, MOCK, RECORD, TEST]
