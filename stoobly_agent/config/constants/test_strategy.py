from typing import Literal

CONTRACT = 'contract'
CUSTOM = 'custom'
DIFF = 'diff'
FUZZY = 'fuzzy'

TestStrategy = Literal[CONTRACT, CUSTOM, DIFF, FUZZY]