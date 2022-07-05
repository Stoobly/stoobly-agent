from typing import Literal

CUSTOM = 'custom'
DIFF = 'diff'
FUZZY = 'fuzzy'

TestStrategy = Literal[CUSTOM, DIFF, FUZZY]