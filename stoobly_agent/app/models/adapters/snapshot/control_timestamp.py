import re
from datetime import datetime, timezone
from typing import Optional, Union

# Request and response control-line timestamps are nanoseconds since epoch.
CONTROL_TIMESTAMP_SCALE = 10 ** 9
# Older response control lines used microseconds. Only coerce plausible epoch µs
# values (not tiny fixture ints like 1).
_LEGACY_US_TIMESTAMP_MIN = 10 ** 12
_LEGACY_US_TIMESTAMP_MAX = 10 ** 16

_ISO_TIMESTAMP_RE = re.compile(
  r'^(\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2})(\.\d+)?(.*)$'
)


def coerce_legacy_us_to_ns(value: Optional[Union[int, float]]) -> int:
  """Upgrade legacy response timestamps stored as microseconds to nanoseconds."""
  if value is None:
    return 0
  total = int(value)
  if _LEGACY_US_TIMESTAMP_MIN <= total < _LEGACY_US_TIMESTAMP_MAX:
    return total * 1000
  return total


def format_control_timestamp(value: Optional[Union[int, float]]) -> Optional[str]:
  """Format a nanosecond control-line epoch int as UTC ISO-8601 (…Z)."""
  if value is None:
    return None
  total = int(value)
  if total < 0:
    total = 0
  seconds, frac = divmod(total, CONTROL_TIMESTAMP_SCALE)
  digits = len(str(CONTROL_TIMESTAMP_SCALE)) - 1
  dt = datetime.fromtimestamp(seconds, tz=timezone.utc)
  if frac == 0:
    return dt.strftime('%Y-%m-%dT%H:%M:%SZ')
  frac_str = f'{frac:0{digits}d}'.rstrip('0')
  return f"{dt.strftime('%Y-%m-%dT%H:%M:%S')}.{frac_str}Z"


def parse_control_timestamp(
  value: Optional[Union[int, float, str, datetime]],
) -> int:
  """
  Parse snapshot entry timestamp back to a nanosecond control-line epoch int.

  Accepts legacy ints/digit-strings, ISO-8601 strings, and datetime values
  (PyYAML SafeLoader may resolve unquoted timestamps).
  """
  if value is None or value == '':
    return 0
  if isinstance(value, bool):
    raise ValueError(f'invalid timestamp: {value!r}')
  if isinstance(value, (int, float)):
    return int(value)
  if isinstance(value, datetime):
    dt = value
    if dt.tzinfo is None:
      dt = dt.replace(tzinfo=timezone.utc)
    else:
      dt = dt.astimezone(timezone.utc)
    seconds = int(dt.timestamp())
    return seconds * CONTROL_TIMESTAMP_SCALE + dt.microsecond * 1000

  text = str(value).strip()
  if not text:
    return 0
  if text.isdigit() or (text[0] == '-' and text[1:].isdigit()):
    return int(text)

  if text.endswith('Z') or text.endswith('z'):
    text = text[:-1] + '+00:00'

  match = _ISO_TIMESTAMP_RE.match(text)
  if not match:
    raise ValueError(f'invalid timestamp: {value!r}')

  base, frac, tz = match.group(1), match.group(2) or '', match.group(3) or ''
  # Replace space separator with T for fromisoformat.
  base = base.replace(' ', 'T', 1)
  try:
    dt = datetime.fromisoformat(base + (tz or '+00:00'))
  except ValueError as exc:
    raise ValueError(f'invalid timestamp: {value!r}') from exc

  if dt.tzinfo is None:
    dt = dt.replace(tzinfo=timezone.utc)
  else:
    dt = dt.astimezone(timezone.utc)

  seconds = int(dt.timestamp())
  digits = len(str(CONTROL_TIMESTAMP_SCALE)) - 1
  if frac:
    frac_digits = frac[1:]
    if len(frac_digits) < digits:
      frac_digits = frac_digits.ljust(digits, '0')
    else:
      frac_digits = frac_digits[:digits]
    frac_int = int(frac_digits)
  else:
    frac_int = 0
  return seconds * CONTROL_TIMESTAMP_SCALE + frac_int
