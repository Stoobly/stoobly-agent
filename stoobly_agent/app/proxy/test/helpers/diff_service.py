import difflib
import json
import pdb

from typing import Union

green = '\x1b[38;5;16;48;5;2m'
green = '\x1b[42m'
red = '\x1b[38;5;16;48;5;1m'
endgreen = '\x1b[0m'
endgreen = '\033[0m'
endred = '\x1b[0m'

error = 'Error: Cannot print diff for binary output'

def diff(a: Union[bytes, str], b: Union[str, bytes]) -> str:

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
  matcher = difflib.SequenceMatcher(None, a, b)

  for opcode, a0, a1, b0, b1 in matcher.get_opcodes():
    if opcode == 'equal':
      output.append(a[a0:a1])
    elif opcode == 'insert':
      output.append(f'{green}{b[b0:b1]}{endgreen}')
    elif opcode == 'delete':
      output.append(f'{red}{a[a0:a1]}{endred}')
    elif opcode == 'replace':
      output.append(f'{green}{b[b0:b1]}{endgreen}')
      output.append(f'{red}{a[a0:a1]}{endred}')

  return ''.join(output)

def __string_like(s):
  return isinstance(s, str) or isinstance(s, bytes)