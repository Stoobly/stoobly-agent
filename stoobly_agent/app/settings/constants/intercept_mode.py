from typing import Final, Literal

MOCK: Final = 'mock'
NORMALIZE: Final = 'normalize'
RECORD: Final = 'record'
TEST: Final = 'test'

Mode = Literal[MOCK, NORMALIZE, RECORD, TEST]