from typing import Literal

NONE = 'none'
FIFO = 'fifo'
LIFO = 'lifo'

AliasResolveStrategy = Literal[NONE, FIFO, LIFO]