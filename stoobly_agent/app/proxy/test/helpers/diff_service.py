import json
import pdb

from typing import Union
from diff_match_patch import diff_match_patch

green = '\x1b[38;5;16;48;5;2m'
red = '\x1b[38;5;16;48;5;1m'
endgreen = '\x1b[0m'
endred = '\x1b[0m'

error = 'Error: Cannot print diff for binary output'

def diff(a: Union[bytes, str], b: Union[str, bytes], timeout = 30) -> str:

  if not __string_like(a):
    a = json.dumps(a, indent=2)
  else:
    try:
      a = a.decode() if isinstance(a, bytes) else a
    except UnicodeDecodeError:
      return error

  if not __string_like(b):
    b = json.dumps(b, indent=2)
  else:
    try:
      b = b.decode() if isinstance(b, bytes) else b
    except UnicodeDecodeError:
      return error

  output = []
  dmp = diff_match_patch()
  for delta in dmp.diff_lineMode(a, b, timeout):
    opcode = delta[0]
    text = delta[1]

    if opcode == 0:
      output.append(text)
    elif opcode == 1:
      length = len(text)
      if text[length - 1] == "\n":
        output.append(f'{green}{text[0:length - 1]} {endgreen}\n')
      else:
        output.append(f'{green}{text}{endgreen}')
    elif opcode == -1:
      length = len(text)
      if text[length - 1] == "\n":
        output.append(f'{red}{text[0:length - 1]} {endred}\n')
      else:
        output.append(f'{red}{text}{endred}')

  return ''.join(output)

def __string_like(s):
  return isinstance(s, str) or isinstance(s, bytes)