from typing import Literal

FAILED = 'failed'
PASSED = 'passed'
SKIPPED = 'skipped'

TestOutputLevel = Literal[FAILED, SKIPPED, PASSED]