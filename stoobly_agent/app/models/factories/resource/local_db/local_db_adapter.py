import uuid

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mitmproxy.http import Response as MitmproxyResponse

class LocalDBAdapter():

  CONTENT_ENCODING_HEADER = 'content-encoding'
  TRANSFER_ENCODING_HEADER = 'transfer-encoding'

  # Framing / body-coding headers that must stay in sync with stored bytes
  IMMUTABLE_RESPONSE_HEADERS = {
    CONTENT_ENCODING_HEADER: 'Content-Encoding',
    TRANSFER_ENCODING_HEADER: 'Transfer-Encoding',
  }

  def header_value(self, headers, name: str):
    if not headers:
      return None

    lower = name.lower()
    for key, value in headers.items():
      if str(key).lower() == lower:
        return value

    return None

  def normalize_header_value(self, value):
    if value is None:
      return None

    value = str(value).strip()
    if not value:
      return None

    return value.lower()

  def rejected_immutable_header_change(self, new_headers, old_headers):
    for name, display_name in self.IMMUTABLE_RESPONSE_HEADERS.items():
      new_value = self.normalize_header_value(self.header_value(new_headers, name))
      old_value = self.normalize_header_value(self.header_value(old_headers, name))
      if new_value != old_value:
        return self.bad_request(f'Changing {display_name} is not allowed')

    return None

  def encode_body(self, body: str, content_encoding: str):
    # If a content encoding is set in the response headers, encode the body.
    # Assumes 'text' is always provided decoded.

    if content_encoding:
      # Lazy import for runtime usage
      from mitmproxy.http import Response as MitmproxyResponse
      # Use MitmproxyResponse to encode the body
      res = MitmproxyResponse.make(
          200,
          body,
          {'content-encoding': content_encoding}
      )
      return res.raw_content
    else: 
      return body.encode()

  def success(self, d):
    return d, 200

  def bad_request(self, d = ''):
    return d, 400

  def not_found(self, d = 'Not Found'):
    return d, 404

  def conflict(self, d = ''):
    return d, 409

  def internal_error(self, d = 'Internal Error'):
    return d, 500

  def validate_uuid(self, id: str):
    try:
      uuid.UUID(id)
      return True
    except Exception:
      return False