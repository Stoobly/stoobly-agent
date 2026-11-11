import base64
from typing import Any, Optional, TypedDict, Union


FORMAT_JSON = 'json'
FORMAT_TEXT = 'text'
FORMAT_BASE64 = 'base64'


class ExpectedResponseEnvelope(TypedDict):
  format: str
  data: Any


def encode_expected_response(data: Any) -> ExpectedResponseEnvelope:
  """Encode expected response content into a JSON-safe envelope for RequestLog."""
  if data is None:
    return {'format': FORMAT_TEXT, 'data': ''}

  if isinstance(data, (dict, list)):
    return {'format': FORMAT_JSON, 'data': data}

  if isinstance(data, str):
    return {'format': FORMAT_TEXT, 'data': data}

  if isinstance(data, bytes):
    try:
      return {'format': FORMAT_TEXT, 'data': data.decode('utf-8')}
    except UnicodeDecodeError:
      return {
        'format': FORMAT_BASE64,
        'data': base64.b64encode(data).decode('ascii'),
      }

  return {'format': FORMAT_TEXT, 'data': str(data)}


def decode_expected_response(
  envelope: Optional[Union[ExpectedResponseEnvelope, dict]]
) -> Any:
  """Decode an expected response envelope back to its original content shape."""
  if not envelope:
    return None

  fmt = envelope.get('format')
  data = envelope.get('data')

  if fmt == FORMAT_JSON:
    return data

  if fmt == FORMAT_BASE64:
    if data is None:
      return b''
    return base64.b64decode(data)

  return data
